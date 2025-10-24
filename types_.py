# filename: types_.py
# shared TypedDict for stock rows

from typing import TypedDict, Literal

Unit = Literal["kg", "piece"]


class StockRow(TypedDict):
    type: str
    name: str
    stock: float
    unit: Unit
    price: float


class ClientInfo(TypedDict):
    firstname: str
    lastname: str
