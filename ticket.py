

class Ticket:

    """
    Classe Ticket représentant un ticket de caisse d'un client. Peut retourner la liste des achats et le total achetés par le client.
    """

    def __init__(self, client: dict, content: list[dict]):
        self.client = client
        self.content = content

    def __repr__(self):
        total = 0
        print(f"{self.client["firstname"]} {self.client["lastname"]}, you bought :")
        for el in self.content:
            total += el.price
            print(f"{el.quantity} {el.name}(s)")
        print(f"Your total is {total}€")