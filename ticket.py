
import re

# Ajouter une instance de client ici ? au lieu de faire client_id directement ?

class Ticket:

    """
    Classe Ticket représentant un ticket de caisse d'un client. Peut retourner la liste des achats et le total achetés par le client.
    """

    def __init__(self, client_id: str):
        self.client_id = client_id
        self.content = []


    def add(self, basket: list[dict]):
        print(basket)
        self.content.extend(basket)


    def total(self):
        return round(sum(d["subtotal"] for d in self.content), 2)


    def get_ticket(self) -> list:
        return list(self.content)


    @staticmethod
    def split_lower_upper(s: str):
        return re.split(r'(?<=[a-z])(?=[A-Z])', s)


    def client_name(self):
        firstname = self.split_lower_upper(self.client_id)[0]
        lastname = self.split_lower_upper(self.client_id)[1]
        return (firstname + " " + lastname).strip()


    def _as_string(self) -> str:
        lines = [f"{self.client_name()}, you bought: "]
        if not self.content:
            lines.append("nothing")
        else:
            for el in self.content:
                qty = el.get("quantity", 1)
                name = el.get("name", "item")
                price = el.get("price", 0.0)
                subtotal = el.get("subtotal", round(qty * price, 2))
                lines.append(f"{qty} {name}(s) @ {price} for {subtotal}")
            lines.append(f"Total: {self.total()}")
        return "\n".join(lines)


    def __str__(self):
        return self._as_string()

    def __repr__(self):
        return self._as_string()