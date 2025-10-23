
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
            {"name": name, "quantity": quantity, "price": price, "subtotal": round(price * quantity, 2)})


    def total(self):
        return round(sum(d["subtotal"] for d in self.content), 2)


    def __repr__(self):

        def split_lower_upper(s: str):
            return re.split(r'(?<=[a-z])(?=[A-Z])', s)

        firstname = split_lower_upper(client_id)[0]
        lastname = split_lower_upper(client_id)[1]
        total = 0

        print(f"{firstname} {lastname}, you bought :")
        for el in self.content:
            total += el.price
            print(f"{el.quantity} {el.name}(s)")
        print(f"Your total is {total}€")