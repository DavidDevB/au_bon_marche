# filename: product.py
from dataclasses import dataclass
from typing import ClassVar, List


@dataclass
class Product:
    """
    Classe générique Fruit pouvant retourner la valeur totale d'un fruit restant en stock.
    """

    fruits: ClassVar[List["Product"]] = []

    name: str
    stock: int
    price: float

    def __post_init__(self) -> None:
        Product.fruits.append(self)

    def stock_value(self) -> float:
        return self.stock * self.price
