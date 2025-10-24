import re


class Ticket:
    """
    Classe Ticket représentant un ticket de caisse d'un client. Peut retourner la liste des achats et le total achetés par le client.
    """

    def __init__(self, client_id: str, content: list[dict]):
        self.client_id = client_id
        self.content = content

    def add(self, name, quantity, price):
        self.content.append(
            {
                "name": name,
                "quantity": quantity,
                "price": price,
                "subtotal": round(price * quantity, 2),
            }
        )

    def total(self) -> float:
        return round(sum(d["subtotal"] for d in self.content), 2)

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
