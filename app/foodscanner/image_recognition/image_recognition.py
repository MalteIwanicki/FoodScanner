from ultralytics import YOLO
from foodscanner.utils.argparser import FoodScannerArgparser as Argparser
import pandas as pd
import json
from pathlib import Path
from PIL import Image
import random

from foodscanner.utils import Food

ROOT = Path(__file__).resolve().parent.parent
RESULT_FOLDER = ROOT / "web/images"

class ImageRecognition:
    """ Predicts classes in images. """
    def __init__(self, model_path):
        self.model = self._load_model(model_path)

    def _load_model(self, model_path):
        return YOLO(model_path)

    def predict(self, image_path: Path):
        """ Predicts classes from image at `image_path`. """
        image = Image.open(image_path)
        predictions = self.model.predict(
            source=image,
            project=ROOT / "web/images",
            name="predicted",
            save=True,
            exist_ok=True,
        )
        prediction = self._format_prediction(predictions[0])
        return prediction

    def _format_prediction(self, prediction):
        result_path = Path(prediction.save_dir) / Path(prediction.path).name
        class_names = [prediction.names[int(class_)] for class_ in prediction.boxes.cls]
        confidences = [round(float(conf) * 100, 2) for conf in prediction.boxes.conf]
        predicted_cls = [{"name":name,"confidence": confidence} for name, confidence in zip(class_names, confidences)
        ]
        return {"path": result_path, "meals": predicted_cls}


if __name__ == "__main__":
    args = Argparser().parse_args()
    ir = ImageRecognition(model_path=args.model_path)
    result = ir.predict(args.image_to_predict)
    result
    pass
