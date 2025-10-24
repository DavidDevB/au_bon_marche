# filename: client.py
from dataclasses import dataclass, field
from typing import ClassVar


@dataclass
class Client:
    """
    Classe générique Client pouvant retourner le prénom, le nom et/ou le total dépensé par le client pendant la journée.
    """

    clients: ClassVar[list["Client"]] = []

    firstname: str
    lastname: str
    purchases: list[dict] = field(default_factory=list)

    def __post_init__(self) -> None:
        Client.clients.append(self)

    def get_firstname(self) -> str:
        return self.firstname

    def get_lastname(self) -> str:
        return self.lastname

    def total_spent(self) -> float:
        return round(sum(float(p.get("total", 0.0)) for p in self.purchases), 2)

    @classmethod
    def nb_clients(cls) -> int:
        return len(cls.clients)
