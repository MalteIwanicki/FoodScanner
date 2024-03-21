from argparse import ArgumentParser
import pathlib

class FoodScannerArgparser(ArgumentParser):
    def __init__(self):
        super().__init__()
        self.add_argument(
            "--model_path",
            type=pathlib.Path,
            required=True,
            help=" Path to image recognition model. ",
        )
        self.add_argument(
            "--image_to_predict",
            type=pathlib.Path,
            help=" Path to image to predict. ",
        )