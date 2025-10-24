# filename: basket.py
from dataclasses import dataclass, field
from typing import ClassVar, Dict, List


@dataclass
class Basket:
    """
    Classe Basket représentant le panier et pouvant retourner un booléen selon si le panier est valide ou non.
    """

    baskets: ClassVar[List["Basket"]] = []

    client_id: str
    content: List[Dict[str, float | str]] = field(default_factory=list)

    def __post_init__(self) -> None:
        Basket.baskets.append(self)

    def add(self, name: str, quantity: float, price: float) -> None:
        """
        Add product to basket.
        :param name:
        :param quantity:
        :param price:
        """
        self.content.append(
            {
                "name": name,
                "quantity": quantity,
                "price": price,
                "subtotal": round(price * quantity, 2),
            }
        )

    def remove(self, name: str) -> Dict[str, float | str]:
        """
        Remove product from basket.
        :param name:
        :return:
        """
        item = next(
            (d for d in self.content if str(d["name"]).lower() == name.lower()), None
        )
        if item is None:
            raise ValueError(f"Item '{name}' not found")
        self.content.remove(item)
        return item

    def total(self) -> float:
        return round(sum(float(d["subtotal"]) for d in self.content), 2)

    @staticmethod
    def validate(items: List[Dict[str, float | str]]) -> bool:
        """
        Validate basket : not empty & quantity is valid
        :param items:
        :return:
        """
        if not items:
            print("Basket is empty.")
            return False
        if any(float(d.get("quantity", 0.0)) <= 0 for d in items):
            print("One or more items has non-positive quantity.")
            return False
        return True

    @classmethod
    def count(cls) -> int:
        return len(cls.baskets)


@dataclass
class BasketStore:
    """
    Classe BasketStore enregistrant les baskets des clients, pour pouvoir les retrouver ensuite selon le client_id.
    """

    _baskets: Dict[str, Basket] = field(default_factory=dict)

    def get_basket(self, client_id: str) -> Basket:
        """
        Get basket by client_id.
        :param client_id:
        :return basket:
        """
        if client_id not in self._baskets:
            self._baskets[client_id] = Basket(client_id)
        return self._baskets[client_id]

    def remove_basket(self, client_id: str) -> None:
        """
        Remove basket by client_id.
        :param client_id:
        :return None:
        """
        self._baskets.pop(client_id, None)

    @staticmethod
    def validate(items: List[Dict[str, float | str]]) -> bool:
        """
        Validate basket : not empty & quantity is valid
        :param items:
        :return:
        """
        if not items:
            print("Basket is empty.")
            return False
        if any(float(d.get("quantity", 0.0)) <= 0 for d in items):
            print("One or more items has non-positive quantity.")
            return False
        return True

