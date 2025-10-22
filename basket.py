

class Basket:
    def __init__(self, client: list[str], content: list[dict]):
        self.client = client
        self.content = content

    @staticmethod
    def validate():
        return "validated"