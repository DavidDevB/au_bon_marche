# filename: client.py
from dataclasses import dataclass, field
from typing import List, ClassVar
from cart import Cart


@dataclass
class Client:
    """
    Classe client.
    """

    clients: ClassVar[list["Client"]] = []

    firstname: str
    lastname: str

    # Historique des commandes validées
    # default_factory=list => chaque Client a sa propre liste
    orders: List[Cart] = field(default_factory=list)

    def __post_init__(self) -> None:
        """
        Ajout de l'objet après la création à 'clients : ClassVar[list["Client"]] = []]'
        """
        Client.clients.append(self)

    def full_name(self) -> str:
        """Retourne le nom complet."""
        return f"{self.firstname} {self.lastname}".strip()

    def add_order(self, cart: Cart) -> None:
        """Ajout du panier VALIDÉ à l'historique."""
        self.orders.append(cart)

    def total_spent(self) -> float:
        """
        Calcul du total dépensé par ce client.
        """
        return round(sum(c.total() for c in self.orders), 2)
