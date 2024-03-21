import sqlite3
from pathlib import Path
from foodscanner.utils import Food

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = "fooddb.db"


def _connect_db(func):
    def wrapper(self, *args, **kwargs):
        self._connect()  # start connection to db
        result = func(self, *args, **kwargs)  # execute myfunc
        self._disconnect()  # end connection to db
        return result

    return wrapper


class FoodDB:
    """ The client for the DB. """
    def __init__(self, db_path=DB_PATH):
        """ `db_path` is where the DB file is located. """
        self.db_path = db_path

    def _connect(self):
        self.conn = sqlite3.connect(self.db_path)
        self.cursor = self.conn.cursor()

    def _disconnect(self):
        self.conn.close()
        self.conn = None

    @_connect_db
    def setup_db(self):
        """ Creates a table in the DB. Execute this when using for the first time. """
        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS Foods (
                name TEXT PRIMARY KEY,
                preis REAL,
                nutri_score TEXT,
                kategorie TEXT,
                energie REAL,
                fett REAL,
                gesaettigte_fettsaeuren REAL,
                kohlenhydrate REAL,
                zucker REAL,
                eiweis REAL,
                salz REAL,
                ballaststoffe REAL,
                obgenu REAL
            );
        """
        )
        self.conn.commit()

    @_connect_db
    def get_foods(self, food_names):
        """ Returns details to the foods with the names givin in the list `food_names`. """
        details = []
        for food_name in food_names:
            self.cursor.execute(f"SELECT * FROM Foods f WHERE f.name='{food_name}'")
            result = self.cursor.fetchone()
            if result is not None:
                details.append(
                    {
                        "Gericht": result[0],
                        "Preis": result[1],
                        "Nutri-Score": result[2],
                        "Kategorie": result[3],
                        "Nährstoffe": {
                            "Energie": result[4],
                            "Fett": result[5],
                            "Gesättigte Fettsäuren": result[6],
                            "Kohlenhydrate": result[7],
                            "Zucker": result[8],
                            "Eiweis": result[9],
                            "Salz": result[10],
                            "Ballaststoffe": result[11],
                            "Obst, Gemüse, Nüsse": result[12],
                        },
                    }
                )
        return details

    @_connect_db
    def insert_food(self, food: Food):
        """ Adds a food-entry to the DB. """
        nu = food["Nährstoffe"]
        self.cursor.execute(
            """
    INSERT OR REPLACE INTO Foods (name, preis, nutri_score, kategorie, energie, fett, gesaettigte_fettsaeuren, kohlenhydrate, zucker, eiweis, salz, ballaststoffe, obgenu)
    VALUES (:name, :preis, :nutri_score, :kategorie, :energie, :fett, :gesaettigte_fettsaeuren, :kohlenhydrate, :zucker, :eiweis, :salz, :ballaststoffe, :obgenu)
""",
            {
                "name": food["Name"],
                "preis": food["Preis"],
                "nutri_score": food["Nutri-Score"],
                "kategorie": food["Kategorie"],
                "energie": nu["Energie"],
                "fett": nu["Fett"],
                "gesaettigte_fettsaeuren": nu["gesättigte Fettsäuren"],
                "kohlenhydrate": nu["Kohlenhydrate"],
                "zucker": nu["Zucker"],
                "eiweis": nu["Eiweis"],
                "salz": nu["Salz"],
                "ballaststoffe": nu["Ballaststoffe"],
                "obgenu": nu["Obst, Gemüse, Nüsse"],
            },
        )
        self.conn.commit()
        return "Food added successfully"

    @_connect_db
    def get_all_foods(self):
        """ Returns all entries in the DB. """
        self.cursor.execute("SELECT * FROM Foods")
        result = self.cursor.fetchall()
        foods = []
        for row in result:
            food = {
                "Name": row[0],
                "Preis": row[1],
                "Nutri-Score": row[2],
                "Kategorie": row[3],
                "Nährstoffe": {
                    "Energie": row[4],
                    "Fett": row[5],
                    "gesättigte Fettsäuren": row[6],
                    "Kohlenhydrate": row[7],
                    "Zucker": row[8],
                    "Eiweis": row[9],
                    "Salz": row[10],
                    "Ballaststoffe": row[11],
                    "Obst, Gemüse, Nüsse": row[12],
                },
            }
            foods.append(food)
        return foods

    @_connect_db
    def delete_food(self, food_name):
        """ Delete entry with name `food_name` from the DB. """
        self.cursor.execute("DELETE FROM Foods WHERE name=?", (food_name,))
        self.conn.commit()
        return f"Food item '{food_name}' removed from database."


if __name__ == "__main__":
    FoodDB().setup_db()
