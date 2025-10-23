

class Basket:

    """
    Classe Basket représentant le panier et pouvant retourner un booléen selon si le panier est valide ou non.
    """

    def __init__(self, client: list[str]):
        self.client = client
        self.content = []


    def add(self, name, quantity, price):
        self.content.append({"name": name, "quantity": quantity, "price": price, "subtotal": round(price * quantity, 2)})


    def remove(self, name):
        item = next((d for d in self.content if d["name"].lower() == name.lower()), None)
        if item is None:
            raise ValueError(f"Item '{name}' not found")
        self.content.remove(item)
        return item

    @staticmethod
    def validate(items: list) -> bool:
        if not items:
            print("Basket is empty.")
            return False
        elif any(item.stock <= 0 for item in items):
            print("One or more item's stock is empty.")
            return False
        else:
            return True