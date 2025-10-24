# filename: sales_log.py
from typing import TypedDict, List, Dict, Any


class SaleRow(TypedDict, total=False):
    firstname: str
    lastname: str
    items: List[Dict[str, Any]]
    total: float


DAY_SALES: List[dict] = []
