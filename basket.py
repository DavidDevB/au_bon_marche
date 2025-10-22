

class Basket:

    """
    Classe Basket représentant le panier et pouvant retourner un booléen selon si le panier est valide ou non.
    """

    def __init__(self, client: list[str], content: list[dict]):
        self.client = client
        self.content = content

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