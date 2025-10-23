

class Basket:

    """
    Classe Basket représentant le panier et pouvant retourner un booléen selon si le panier est valide ou non.
    """

    def __init__(self, client_id: str):
        self.client_id = client_id
        self.content = []


    def add(self, name: str, quantity: int, price: float) -> None:
        self.content.append({"name": name, "quantity": quantity, "subtotal": round(price * quantity, 2)})
        print(f"Your basket contains:")
        for el in self.content:
            print(el)


    def remove(self, name):
        item = next((d for d in self.content if d["name"].lower() == name.lower()), None)
        if item is None:
            raise ValueError(f"Item '{name}' not found")
        self.content.remove(item)
        return item


    def total(self):
        return round(sum(d["subtotal"] for d in self.content), 2)


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


class BasketStore:
    """
    Classe BasketStore enregistrant les baskets des clients, pour pouvoir les retrouver ensuite selon le client_id.
    """

    def __init__(self):
        self._baskets: dict[str, Basket] = {}

    def get_basket(self, client_id: str) -> Basket:
        if client_id not in self._baskets:
            self_baskets[client_id] = Basket(client_id)
        return self._baskets[client_id]

    def remove_basket(self, client_id: str) -> None:
        self._baskets.pop(client_id, None)