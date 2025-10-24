# filename: ticket.py
from dataclasses import dataclass, field
from typing import List, Dict, Any, ClassVar


@dataclass
class Ticket:
    """
    Classe Ticket représentant un ticket de caisse d'un client. Peut retourner la liste des achats et le total achetés par le client.
    """

    tickets: ClassVar[List["Ticket"]] = []

    client_id: str
    content: List[Dict[str, Any]] = field(default_factory=list)

    def __post_init__(self) -> None:
        Ticket.tickets.append(self)

    def add(self, name, quantity, price) -> None:
        self.content.append(
            {
                "name": name,
                "quantity": quantity,
                "price": price,
                "subtotal": round(price * quantity, 2),
            }
        )

    def total(self) -> float:
        return round(sum(float(d["subtotal"]) for d in self.content), 2)

    def __repr__(self) -> str:
        parts = str(self.client_id).replace("_", " ").split()
        firstname = parts[0] if parts else str(self.client_id)
        lastname = parts[1] if len(parts) > 1 else ""

        lines = [f"{firstname} {lastname}, you bought:"]
        for el in self.content:
            lines.append(
                f"- {el['quantity']} x {el['name']} @ {el['price']:.2f}€ = {el['subtotal']:.2f}€"
            )
        lines.append(f"TOTAL: {self.total():.2f}€")
        return "\n".join(lines)

    @classmethod
    def nb_tickets(cls) -> int:
        return len(cls.tickets)
