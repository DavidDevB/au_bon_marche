

def client_or_owner() -> str | None:

    """
    Retourne soit 'client' soit 'owner' selon le choix de l'utilisateur
    :return: str
    """

    while True:
        answer = input("Are you a client or the owner?: ").lower()
        if answer != "client" and answer != "owner":
            print("Please choose between 'client' and 'owner'.")
            continue
        return answer


def get_client_infos() -> dict | None:

    """
    Retourne le prénom et le nom du client
    :return: dict
    """

    while True:
        firstname = input("Please enter your firstname: ")
        if firstname.isdigit() or None:
            print("Please enter a valid firstname.")
            continue
        lastname = input("Please enter your lastname: ")
        if lastname.isdigit() or None:
            print("Please enter a valid lastname.")
            continue
        return {"firstname": firstname, "lastname": lastname}




