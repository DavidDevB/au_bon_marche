# filename: types_.py
# shared TypedDict for stock rows

from typing import TypedDict


class StockRow(TypedDict):
    type: str
    name: str
    stock: float
    unit: str
    price: float


class ClientInfo(TypedDict):
    firstname: str
    lastname: str
