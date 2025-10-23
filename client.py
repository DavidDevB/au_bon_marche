import re

class Client:

    """
    Classe générique Client pouvant retourner le prénom, le nom et/ou le total dépensé par le client pendant la journée.
    """


    def __init__(self):
        self.firstname: str = ""
        self.lastname: str= ""
        self.client_id: str = ""

    def get_client_infos(self) -> dict:

        """
        Retourne le prénom et le nom du client
        :return: dict
        """

        name_re = re.compile(r"^[A-Za-zÀ-ÖØ-öø-ÿ' -]{2,50}$")

        while True:
            firstname = input("Please enter your firstname: ")
            if not firstname or not name_re.match(firstname):
                print("Please enter a valid firstname.")
                continue

            lastname = input("Please enter your lastname: ").upper()
            if not lastname or not name_re.match(lastname):
                print("Please enter a valid lastname.")
                continue

            self.firstname = firstname
            self.lastname = lastname
            self.client_id = "".join([firstname, lastname])

        return {
            "firstname": self.firstname,
            "lastname": self.lastname,
            "client_id": self.client_id,
    }






