# filename: au_bon_marche.py
from sales_log import DAY_SALES
from stock import Stock
from basket import Basket
from ticket import Ticket


def client_or_owner() -> str:
    """
    Retourne soit 'client' soit 'owner' selon le choix de l'utilisateur
    :return: str
    """
    while True:
        answer = (
            input("Are you a client or the owner? (type 'q' to quit): ").strip().lower()
        )
        if answer in ("client", "owner", "q", "quit"):
            return "quit" if answer in ("q", "quit") else answer
        print("Please choose between 'client', 'owner', or 'q' to quit.")


def get_client_infos() -> dict[str, str] | None:
    """
    Retourne le prénom et le nom du client
    :return: dict
    """
    while True:
        firstname = input("Please enter your firstname: ").strip()
        if not firstname or any(ch.isdigit() for ch in firstname):
            print("Please enter a valid firstname.")
            continue
        lastname = input("Please enter your lastname: ").strip()
        if not lastname or any(ch.isdigit() for ch in lastname):
            print("Please enter a valid lastname.")
            continue
        return {"firstname": firstname, "lastname": lastname}


def _print_catalog_lines(stock_list: list[dict]) -> None:
    """Affiche le catalogue regroupé en fruit & légumes"""
    print("\n=== FRUITS ===")
    for el in stock_list:
        if el["type"] == "fruit":
            unit = el["unit"]
            print(
                f"{el['name']} | Price: {el['price']:.2f}€/{unit} | Stock: {el['stock']} {unit}"
            )

    print("\n=== VEGETABLES ===")
    for el in stock_list:
        if el["type"] == "vegetable":
            unit = el["unit"]
            print(
                f"{el['name']} | Price: {el['price']:.2f}€/{unit} | Stock: {el['stock']} {unit}"
            )
    print()


def _normalize_qty(unit: str, qty_raw: float) -> float:
    """Normalise la quantité :
    piece -> int>=1
    kg -> 1 decimal >= 0.1
    """
    if unit == "piece":
        q = int(round(qty_raw))
        return float(max(1, q))
    # unit == "kg"
    q = round(float(qty_raw), 1)
    return 0.1 if q < 0.1 else q


def choose_your_items() -> None:
    """
    Demande au client de choisir un article et sa quantité
    :return: list[str, float]
    """
    stock = Stock.stock
    _print_catalog_lines(stock)

    items_by_name = {d["name"].strip().lower(): d for d in stock}

    client_info = get_client_infos()
    client_id = f"{client_info['firstname']} {client_info['lastname']}"
    basket = Basket(client_id)

    want_to_buy = True
    while want_to_buy:
        while True:
            name = input("Choose an item by name: ").strip().lower()
            item = items_by_name.get(name)
            if not item:
                print("Choose an item from the stock.")
                continue
            break

        unit = item["unit"]
        qty: float | None = None

        while True:
            qty_text = (
                input(f"Choose quantity (available={item['stock']} {unit}): ")
                .strip()
                .replace(",", ".")
            )
            try:
                qty_tmp = float(qty_text) if unit == "kg" else int(qty_text)
            except ValueError:
                print("Please enter a valid number.")
                continue

            if qty_tmp <= 0:
                print("Quantity must be > 0.")
                continue

            qty = _normalize_qty(unit, qty_tmp)
            if qty > item["stock"]:
                print(f"Quantity must be <= {item['stock']} {unit}.")
                continue

            break

        Stock.decrease(item["name"], qty)
        basket.add(item["name"], qty, item["price"])
        print(f"You add: {item['name']} x {qty} {unit} to your basket")

        again = input("Do you want to add another item? (y/n): ").strip().lower()
        want_to_buy = again == "y"

    if not basket.content:
        print("\nNo items selected. Returning to role menu.")
        return

    # --- final ticket ---
    ticket = Ticket(client_id, basket.content)
    print("\n--- Ticket ---")
    print(ticket)

    DAY_SALES.append(
        {
            "firstname": client_info["firstname"],
            "lastname": client_info["lastname"],
            "items": list(basket.content),
            "total": ticket.total(),
        }
    )
