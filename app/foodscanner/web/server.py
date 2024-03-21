#  this server can be startet with: `uvicorn foodscanner.web.server:app --reload`
import uvicorn

import shutil
import os
from pathlib import Path

from fastapi import FastAPI, Request, File, UploadFile, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from foodscanner.utils.argparser import FoodScannerArgparser as Argparser

from foodscanner.image_recognition import ImageRecognition
from foodscanner.dbms import FoodDB
from foodscanner.utils import Food
from foodscanner.web.database_page import router as database_router

import time

BASE_DIR = Path(__file__).resolve().parent
IMAGE_DIR = BASE_DIR/"images"
templates = Jinja2Templates(directory=str(Path(BASE_DIR, "templates")))

args = Argparser().parse_args()

MODELL_PATH = args.model_path
food_recognition = ImageRecognition(MODELL_PATH)

food_db = FoodDB()

app = FastAPI()
app.include_router(database_router)
app.mount(
    "/images", StaticFiles(directory=str(Path(BASE_DIR, "images"))), name="images"
)
app.mount(
    "/static", StaticFiles(directory=str(Path(BASE_DIR, "static"))), name="static"
)

last_id = 0

id_image_map={}
def get_details(image_path):
    """ Predict classes of image at `image_path` and return their details. """
    start_time = time.time()
    prediction = food_recognition.predict(image_path)
    end_time = time.time()
    prediction_time = end_time - start_time
    start_time = time.time()
    meals_prediction = prediction["meals"]
    names = {meal["name"] for meal in meals_prediction}
    counts={key:0 for key in names}
    for meal in meals_prediction:
        counts[meal["name"]]+=1
    meals = food_db.get_foods(names)
    for meal in meals:
        meal["Anzahl"]=counts[meal["Gericht"]]
    total_meals = sum([meal["Anzahl"] for meal in meals])
    total_price = round(sum([meal["Anzahl"]*meal["Preis"] for meal in meals]),2)
    meals = sorted(meals, key=lambda x: x['Preis'])
    end_time = time.time()
    db_time = end_time - start_time
    details = dict(total_meals=total_meals, total_price=total_price, meals=meals, predicted_img="/".join(prediction["path"].parts[-3:]))
    with open("times.csv","a") as f:
        f.write(f"{prediction_time},{db_time}\n")
    return details

@app.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    """ Uploads `file` to server and triggers the image prediction and DB query. """
    path = IMAGE_DIR/"tmp" / file.filename
    relative_path = Path("/".join(path.parts[-2:]))
    with path.open("wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    details = get_details(path)
    id_image_map[id]=(relative_path, details)
    return {
        "filename": str(relative_path),
        "details": details,
    }

@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    """ Returns the main page. """
    return templates.TemplateResponse("index.html", {"request": request})


def start():
    """ Starts the server """
    uvicorn.run("foodscanner.web.server:app", reload=True)


if __name__ == "__main__":
    start()
