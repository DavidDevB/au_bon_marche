from dataclasses import dataclass
from typing import Literal
from abc import ABC

Unit = Literal["kg", "piece"]
Category = Literal["fruit", "vegetable"]


@dataclass
class Product(ABC):
    """Base class for all products in the store."""

    name: str  # Display name for receipts & catalog
    unit: Unit  # "kg" or "piece"
    price: float  # Unit price in euros
    stock: float  # Current stock: kg or number of pieces
    category: Category  # "fruit" or "vegetable"

    # ---------- Core API  ----------

    def normalize_qty(self, qty: float) -> float:
        """
        Normalize quantity to valid step for this product.
        - "piece": integer, minimum 1
        - "kg": one decimal precision, minimum 0.1 kg
        """
        if self.unit == "piece":
            q = max(1, int(round(qty)))
            return float(q)
        # unit == "kg"
        q = round(qty, 1)
        return 0.1 if q < 0.1 else q

    def can_sell(self, qty: float) -> bool:
        """Return True if quantity can be served."""
        q = self.normalize_qty(qty)
        return 0 < q <= self.stock

    def reserve_possible(self, qty: float) -> float:
        """
        Return quantity that can be served.
        """
        q = self.normalize_qty(qty)
        if q <= 0:
            return 0.0
        return min(q, self.stock)

    def remove_stock(self, qty: float) -> None:
        """Decrease stock"""
        q = self.normalize_qty(qty)
        if q <= 0 or q > self.stock:
            raise ValueError(
                f"Not enough stock for {self.name}. Requested={q}, Stock={self.stock}"
            )
        self.stock = round(self.stock - q, 3)

    def price_for(self, qty: float) -> float:
        """
        Compute total price for given quantity.
        """
        q = self.normalize_qty(qty)
        return round(q * self.price, 2)


# ---------- Categories ----------


@dataclass
class Fruit(Product):
    """Fruit category."""

    def __init__(self, name: str, unit: Unit, price: float, stock: float):
        super().__init__(
            name=name, unit=unit, price=price, stock=stock, category="fruit"
        )


@dataclass
class Vegetable(Product):
    """Vegetable category."""

    def __init__(self, name: str, unit: Unit, price: float, stock: float):
        super().__init__(
            name=name, unit=unit, price=price, stock=stock, category="vegetable"
        )
