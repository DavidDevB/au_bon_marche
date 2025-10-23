
from client import Client
from stock import Stock
from basket import Basket
from ticket import Ticket
from summary import Summary


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



def buy_items():
    """
    Demande au client de choisir un article et sa quantité
    :return: list[str, float]
    """

    new_client = Client()
    client_infos = new_client.get_client_infos()
    client_id = client_infos["client_id"]
    new_basket = Basket(client_id)
    new_summary = Summary()

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
    want_to_buy = True
    while want_to_buy:
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
            Stock.decrease(item["name"], qty)

            break

        print(f"You add: {item['name']} x {qty} {item['unit']} to your basket")
        item_price = Stock.find(item["name"])["price"]
        new_basket.add(item["name"], qty, item_price)
        while True:
            buy_more = input("Do you want to buy some more? Y/n: ").lower()
            if buy_more not in ["y", "n"]:
                continue
            if buy_more == "n":
                want_to_buy = False
                break
            else:
                break

    new_ticket = Ticket(client_id)
    print(f"new_basket content: {new_basket.content}")
    new_ticket.add(new_basket.content)
    print(f"Your ticket: {new_ticket.content}")
    new_summary.add_each_client_summary(client_id, new_ticket)





