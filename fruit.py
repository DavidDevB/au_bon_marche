from dataclasses import dataclass


@dataclass
class Fruit:
    """
    Classe générique Fruit pouvant retourner la valeur totale d'un fruit restant en stock.
    """

    name: str
    stock: int
    price: float

    def stock_value(self) -> float:
        return self.stock * self.price
