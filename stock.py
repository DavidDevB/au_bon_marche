# filename: stock.py
from dataclasses import dataclass
from typing import ClassVar, List

from types_ import StockRow


@dataclass
class Stock:
    """
    Classe Stock représentant le stock restant de légumes et fruits.
    """

    stock: ClassVar[List[StockRow]] = [
        {
            "type": "fruit",
            "name": "Clementine",
            "stock": 6,
            "unit": "kg",
            "price": 2.90,
        },
        {"type": "fruit", "name": "Date", "stock": 4, "unit": "kg", "price": 7.00},
        {"type": "fruit", "name": "Grenade", "stock": 3, "unit": "kg", "price": 3.50},
        {"type": "fruit", "name": "Persimmon", "stock": 3, "unit": "kg", "price": 4.50},
        {"type": "fruit", "name": "Kiwi", "stock": 5, "unit": "kg", "price": 3.50},
        {"type": "fruit", "name": "Mandarin", "stock": 6, "unit": "kg", "price": 2.80},
        {"type": "fruit", "name": "Orange", "stock": 8, "unit": "kg", "price": 1.50},
        {
            "type": "fruit",
            "name": "Grapefruit",
            "stock": 8,
            "unit": "piece",
            "price": 2.00,
        },
        {"type": "fruit", "name": "Pear", "stock": 5, "unit": "kg", "price": 2.50},
        {"type": "fruit", "name": "Apple", "stock": 8, "unit": "kg", "price": 1.50},
        {
            "type": "vegetable",
            "name": "Carrot",
            "stock": 7,
            "unit": "kg",
            "price": 1.30,
        },
        {
            "type": "vegetable",
            "name": "Brussels sprouts",
            "stock": 4,
            "unit": "kg",
            "price": 4.00,
        },
        {
            "type": "vegetable",
            "name": "Green cabbage",
            "stock": 12,
            "unit": "piece",
            "price": 2.50,
        },
        {
            "type": "vegetable",
            "name": "Butternut squash",
            "stock": 6,
            "unit": "piece",
            "price": 2.50,
        },
        {
            "type": "vegetable",
            "name": "Endive",
            "stock": 5,
            "unit": "kg",
            "price": 2.50,
        },
        {
            "type": "vegetable",
            "name": "Spinach",
            "stock": 4,
            "unit": "kg",
            "price": 2.60,
        },
        {"type": "vegetable", "name": "Leek", "stock": 5, "unit": "kg", "price": 1.20},
        {
            "type": "vegetable",
            "name": "Pumpkin",
            "stock": 6,
            "unit": "piece",
            "price": 2.50,
        },
        {
            "type": "vegetable",
            "name": "Black radish",
            "stock": 10,
            "unit": "piece",
            "price": 5.00,
        },
        {
            "type": "vegetable",
            "name": "Salsify",
            "stock": 3,
            "unit": "kg",
            "price": 2.50,
        },
    ]

    @classmethod
    def find(cls, name: str) -> StockRow | None:
        name_norm = name.strip().lower()
        return next((d for d in cls.stock if d["name"].lower() == name_norm), None)

    @classmethod
    def decrease(cls, name: str, qty: float) -> float:
        item = cls.find(name)
        if not item:
            raise ValueError("Item not found")
        if qty <= 0:
            raise ValueError("Quantity must be > 0")
        if qty > float(item["stock"]):
            raise ValueError(f"Not enough stock. Max = {item['stock']} {item['unit']}")
        item["stock"] = float(item["stock"]) - float(qty)
        return float(item["stock"])

    @classmethod
    def restock(cls, name: str, qty: float) -> float:
        item = cls.find(name)
        if not item:
            raise ValueError("Item not found")
        if qty <= 0:
            raise ValueError("Quantity must be > 0")
        item["stock"] = float(item["stock"]) + float(qty)
        return float(item["stock"])
