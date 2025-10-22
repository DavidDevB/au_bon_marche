from dataclasses import dataclass, field
from typing import List
from cart import Cart


@dataclass
class Client:
    """Customer identity with all carts."""

    firstname: str
    lastname: str
    orders: List[Cart] = field(default_factory=list)  # keeps all validated carts

    def full_name(self) -> str:
        """Return full name."""
        return f"{self.firstname} {self.lastname}".strip()

    def add_order(self, cart: Cart) -> None:
        """Append a validated cart to customer."""
        self.orders.append(cart)

    def total_spent(self) -> float:
        """Compute amount paid across all validated carts."""
        return round(sum(c.total() for c in self.orders), 2)
