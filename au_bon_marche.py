
from client import Client
from stock import Stock


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


def choose_your_items():
    """
    Demande au cliente de choisir un article et sa quantité
    :return: list[str, float]
    """

    stock = Stock.stock

    print("\n")
    print("===FRUITS===")
    for el in stock:
        if el["type"] == "fruit":
            print(f"{el['name']} | Price: {el['price']}€/kg | Stock: {el['stock']}")
    print("\n")
    print("===VEGETABLES===")
    for el in stock:
        if el["type"] == "vegetable":
            print(f"{el['name']} | Price: {el['price']}€/kg | Stock: {el['stock']}")
    print("\n")

    items_by_name = {d["name"].lower(): d for d in stock}

    qty = None
    while True:
        name = input("Choose an item by name: ").strip().lower()
        item = items_by_name.get(name)
        if not item:
            print("Choose an item from the stock.")
            continue
        break
    print()
    while True:
        qty_str = input(f"Choose quantity (available={item['stock']} {item['unit']}): ").strip()
        if not qty_str.isdigit():
            print("Please enter an integer quantity.")
            continue
        qty = int(qty_str)

        if qty < 1:
            print("Quantity must be at least 1.")
            continue

        if qty > item["stock"]:
            print(f"Quantity must be available.")
            continue
        break

    print(f"OK: {item['name']} x {qty} {item['unit']}")
    return [item['name'],item['unit']]


