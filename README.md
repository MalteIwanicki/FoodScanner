# FoodScanner
This programm was developed 2024 as a prototype for my bachelor's thesis *Prototyp eines Food Scanners zur automatischen Erkennung von Speisen und Ermittlung ihrer Nährwerte*. It consists of some Jupyter Notebooks for preparing an image recognition model and a webapp. The webapp was developed to identify images of food in real-time and display it's Nutri-Score.
The Nutri-Score is calculated in [this repository](https://github.com/MalteIwanicki/NutriScoreCalculator).
The [evaluate.ipynb](evaluation/evaluate.ipynb) notebook was used to generate some graphics regarding the evaluation and to measure the speed of the webserver.
# Setup
With a python 3.10 environment installed and activated execute:
> `pip install -r app/requirements.txt`

Then initialize the DB with:
> `python app/foodscanner/dbms/dbms.py`

Now fill the database with your food data e.g.:
> [fill_webapps_database_with_example_data.ipynb](preparation/fill_webapps_database_with_example_data.ipynb)


# Run
Start the webserver with :
>python app/foodscanner/web/server.py --model_path=< path to your model's weights file>

The server should now run under the [local url](http://127.0.0.1:8000).
To test different layout variations try one of:
1. [Layout A](http://127.0.0.1:8000/?layout=a)
2. [Layout B](http://127.0.0.1:8000/?layout=b)
3. [Layout C](http://127.0.0.1:8000/?layout=c)


## Example
Download the datasets with:
> [dataset_loader.ipynb](prepare/dataset_loader.ipynb)

Train a model with:
> [train_a_example_model.ipynb](preparation/train_a_example_model.ipynb)

Start the Webapp as described in Run.



