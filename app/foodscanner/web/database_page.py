from pathlib import Path
from fastapi import FastAPI, Request, File, UploadFile, Form, APIRouter
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from foodscanner.image_recognition import ImageRecognition
from foodscanner.dbms import FoodDB
from foodscanner.utils import Food
from nutri_score_calculator import NutriScoreCalculator, NutriScoreCategory


BASE_DIR = Path(__file__).resolve().parent
templates = Jinja2Templates(directory=str(Path(BASE_DIR, "templates")))
food_db = FoodDB()


router = APIRouter()


@router.get("/food_db")
def read_foods(request: Request):
    """ Returns the database page. """
    foods = food_db.get_all_foods()
    return templates.TemplateResponse(
        "database.html", {"request": request, "foods": foods}
    )


@router.post("/food_db")
def insert_or_update_food(
    name: str = Form(...),
    preis: float = Form(...),
    kategorie: str = Form(...),
    energie: float = Form(...),
    fett: float = Form(...),
    gesaettigte_fettsaeuren: float = Form(...),
    kohlenhydrate: float = Form(...),
    zucker: float = Form(...),
    eiweis: float = Form(...),
    salz: float = Form(...),
    ballaststoffe: float = Form(...),
    obgenu: float = Form(...),
):
    """ Inserts Entry to DB. The Name is the index. If the name already exists it overrides the entry. """
    food = {
        "Name": name,
        "Preis": preis,
        "Kategorie":kategorie,
        "Nährstoffe": {
            "Energie": energie,
            "Fett": fett,
            "gesättigte Fettsäuren": gesaettigte_fettsaeuren,
            "Kohlenhydrate": kohlenhydrate,
            "Zucker": zucker,
            "Eiweis": eiweis,
            "Salz": salz,
            "Ballaststoffe": ballaststoffe,
            "Obst, Gemüse, Nüsse": obgenu,
        },
    }
    category = NutriScoreCategory[kategorie]
    n = food["Nährstoffe"]
    food["Nutri-Score"] = NutriScoreCalculator.calculate_nutri_score(
        category=category,
        kilokalorien=n["Energie"],
        gesaettigte_fettsaeuren=n["gesättigte Fettsäuren"],
        zucker=n["Zucker"],
        proteine=n["Eiweis"],
        ballaststoffe=n["Ballaststoffe"],
        anteil_obst_gemuese_huelsen_schalen_raps_walnuss_und_olivenoele=n[
            "Obst, Gemüse, Nüsse"
        ],
        salz=n["Salz"],
        natrium=None,
        gesamtfett=n["Fett"],
    )[0]
    answer = food_db.insert_food(food)
    return {"message": answer, "food": food}


@router.delete("/food_db/{name}")
def delete_food(name: str):
    """ Deletes the Entry in the DB with the name `name`. """
    food_db.delete_food(name)
    return {"message": "Food deleted successfully"}
