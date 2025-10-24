from dataclasses import dataclass


@dataclass
class Vegetable:
    """
    Classe générique Vegetable pouvant retourner la valeur totale du légume restant en stock.
    """

    name: str
    stock: int
    price: float

    def stock_value(self) -> float:
        return self.stock * self.price
