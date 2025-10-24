# filename: sales_log.py
from typing import TypedDict, Any


class SaleRow(TypedDict, total=False):
    firstname: str
    lastname: str
    items: list[dict[str, Any]]
    total: float


DAY_SALES: list[SaleRow] = []
