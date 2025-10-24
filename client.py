class Client:
    """
    Classe générique Client pouvant retourner le prénom, le nom et/ou le total dépensé
    par le client pendant la journée.
    """

    def __init__(
        self, firstname: str, lastname: str, purchases: list[dict] | None = None
    ):
        self.firstname = firstname
        self.lastname = lastname
        self.purchases = purchases or []

    def get_firstname(self) -> str:
        return self.firstname

    def get_lastname(self) -> str:
        return self.lastname

    def total_spent(self) -> float:
        return round(sum(p.get("total", 0.0) for p in self.purchases), 2)
