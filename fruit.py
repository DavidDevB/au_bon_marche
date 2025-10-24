# filename: fruit.py
from dataclasses import dataclass
from typing import ClassVar, List


@dataclass
class Fruit:
    """
    Classe générique Fruit pouvant retourner la valeur totale d'un fruit restant en stock.
    """

    fruits: ClassVar[List["Fruit"]] = []

    name: str
    stock: int
    price: float

    def __post_init__(self) -> None:
        Fruit.fruits.append(self)

    def stock_value(self) -> float:
        return self.stock * self.price
