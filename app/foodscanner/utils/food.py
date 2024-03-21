import random


class Food(dict):
    def __init__(self, name):
        super().__init__(
            Name=name, Preis=self.get_price(), Nährstoffe=self.get_nutritions()
        )

    def get_price(self):
        return random.randint(1, 10)

    def get_nutritions(self):
        rnd = lambda: random.randint(0, 100)
        return {
            "Energie": rnd(),
            "Fett": rnd(),
            "gesättigte Fettsäuren": rnd(),
            "Kohlenhydrate": rnd(),
            "Zucker": rnd(),
            "Eiweis": rnd(),
            "Salz": rnd(),
            "Ballaststoffe":rnd(),
            "Nutri-Score":rnd(),
        }

    def to_sql_vals(self):
        nu = nutritons = self["Nährstoffe"]
        vals = [
            self["Name"],
            self["Preis"],
            nu["Energie"],
            nu["Fett"],
            nu["gesättigte Fettsäuren"],
            nu["Kohlenhydrate"],
            nu["Zucker"],
            nu["Eiweis"],
            nu["Salz"],
            nu["Ballaststoffe"],
            nu["Nutri-Score"]
        ]
        vals = [f"{v}" for v in vals]
        return ", ".join(vals)


if __name__ == "__main__":
    pass
    f = Food(
        name="fgh",
        preis=5,
        kohlenhydrate=2,
        fett=1,
        gesaettigte_fettsaeuren=1,
        zucker=4,
        eiweis=5,
        salz=6,
    )
    pass
