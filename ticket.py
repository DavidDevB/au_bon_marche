

class Ticket:
    def __init__(self, content: list[dict]):
        self.content = content

    def __repr__(self):
        total = 0
        print(f"You bought :")
        for el in self.content:
            total += el.price
            print(f"{el.quantity} {el.name}(s)")
        print(f"Your total is {total}€")