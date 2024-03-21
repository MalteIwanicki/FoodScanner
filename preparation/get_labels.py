import pandas as pd
import json
from pathlib import Path
from PIL import Image
# \labels_other\index_class.csv"
# \labels_other\annotations.json"

IMAGE_FOLDER = Path(
    r"datasets/UNIMIB2016/images"
)



def get_yolo_bb(row):
    def convert(size, box):
        dw = 1./size[0]
        dh = 1./size[1]
        x = (box[0] + box[1])/2.0
        y = (box[2] + box[3])/2.0
        w = box[1] - box[0]
        h = box[3] - box[2]
        x = x*dw
        w = w*dw
        y = y*dh
        h = h*dh
        return (x,y,w,h)
    im=Image.open(row.image_path)
    w= int(im.size[0])
    h= int(im.size[1])
    return convert((w,h), row.bounding_box)

def normalize_boundary_points(row):
    def convert(size, boundary_points):
        dw = 1./size[0]
        dh = 1./size[1]
        def get_factor(n):
            is_x = n%2==0
            return dw if is_x else dh
        
        coordinates = [coordinate*get_factor(i) for i, coordinate in enumerate(boundary_points)]
        return coordinates
    
    im=Image.open(row.image_path)
    w= int(im.size[0])
    h= int(im.size[1])
    
    return convert((w,h), row.boundary_points)

class Label:
    def __init__(self, image_name, values):
        self.name = image_name
        self.image_path = Path(
            r"C:\Users\malte.iwanicki\Documents\bachelor\BachelorInformatikAbschlussarbeit\src\datasets\UNIMIB2016\images"
        ) / (image_name + ".jpg")

        self.table = self.get_df(values)
        self.table["image"] = image_name

    def __repr__(self):
        return f"image: {self.name}; rows: {len(self.table)}"

    def get_df(self, values):
        for n, value in enumerate(values):
            if value != "cibo":
                rows = n
                break
        chunks = [values[i : i + rows] for i in range(0, len(values), rows)]
        chunks.pop(3)
        category, class_, name, boundary_points, bounding_box = chunks
        return pd.DataFrame(
            dict(
                class_=class_,
                name=name,
                boundary_points=boundary_points,
                bounding_box=bounding_box,
            )
        )


def get_labels():
    with open(ANNOTATIONS_MAP, "r") as f:
        data = json.load(f)
    individual_labels = [Label(key, values) for key, values in data.items()]
    labels = pd.concat([label.table for label in individual_labels])
    labels["image_path"] = IMAGE_FOLDER / (
        labels["image"] + ".jpg"
    )
    labels.drop(columns="name", inplace=True)
    labels.bounding_box = labels.bounding_box.apply(
        lambda l: ((min(l[0], l[4]), max(l[0], l[4]), min(l[1], l[5]), max(l[1], l[5])))
    )
    labels["bounding_box"]=labels.apply(get_yolo_bb, axis=1)
    labels["boundary_points"]=labels.apply(normalize_boundary_points, axis=1)
    
    return labels



