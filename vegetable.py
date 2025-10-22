
from dataclasses import dataclass

@dataclass
class Vegetable:
    name: str
    stock: int
    price: int

    def stock_value(self) -> float:
        return self.stock * self.price