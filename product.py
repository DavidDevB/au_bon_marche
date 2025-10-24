# filename: product.py
from dataclasses import dataclass
from typing import ClassVar, List


@dataclass
class Product:
    """
    Classe générique Product pouvant retourner la valeur totale d'un produit restant en stock.
    """

    products: ClassVar[List["Product"]] = []

    name: str
    stock: int
    price: float

    def __post_init__(self) -> None:
        Product.products.append(self)

    def stock_value(self) -> float:
        return self.stock * self.price
