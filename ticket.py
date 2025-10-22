

class Ticket:
    def __init__(self, content: list[dict]):
        self.content = content

    def __repr__(self):
        total = 0
        for el in content:
            total += el.price
        print(f"Votre total est de {total}€")