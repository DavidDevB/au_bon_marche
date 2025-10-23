
class Client:

    """
    Classe générique Client pouvant retourner le prénom, le nom et/ou le total dépensé par le client pendant la journée.
    """

    def __init__(self, firstname, lastname, purchases):
        self.firstname = firstname
        self.lastname = lastname
        self.purchases = purchases


    def firstname(self) -> str:
        return self.firstname


    def lastname(self) -> str:
        return self.lastname


    @staticmethod
    def total_spent() -> float:
        total_spent = 0
        for purchase in purchases:
            total_spent += purchase["total"]
        return total_spent


