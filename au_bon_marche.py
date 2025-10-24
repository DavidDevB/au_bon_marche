# filename: au_bon_marche.py
from typing import Dict, List, cast
from sales_log import DAY_SALES
from stock import Stock
from basket import Basket
from ticket import Ticket
from types_ import StockRow, ClientInfo, Unit


def ask_yes_no(prompt: str, default: bool | None = None) -> bool:
    """
    Fonction utilitaire pour les inputs de type "oui ou non"
    :param prompt:
    :param default:
    :return:
    """
    while True:
        ans = input(prompt).strip().lower()
        if ans in ("y", "yes", "o", "oui"):
            return True
        if ans in ("n", "no", "non"):
            return False
        if ans == "" and default is not None:
            return default
        print("Please answer with 'y' or 'n'.")


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


def get_client_infos() -> ClientInfo:
    """
    Retourne le prénom et le nom du client
    :return: ClientInfo
    """
    firstname = ""
    lastname = ""
    while True:
        fn = input("Please enter your firstname: ").strip()
        if not fn or any(ch.isdigit() for ch in fn):
            print("Please enter a valid firstname.")
            continue
        ln = input("Please enter your lastname: ").strip()
        if not ln or any(ch.isdigit() for ch in ln):
            print("Please enter a valid lastname.")
            continue
        firstname, lastname = fn.capitalize(), ln.upper()
        break
    return {"firstname": firstname, "lastname": lastname}


def _print_catalog_lines(stock_list: List[StockRow]) -> None:
    """Affiche le catalogue regroupé en fruit & légumes
    :param stock_list List[StockRow] : stock list
    :return: None
    """
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


def _normalize_qty(unit: Unit, qty_raw: float) -> float:
    """Normalise la quantité :
    piece -> int>=1
    kg -> 1 decimal >= 0.1
    :param unit:
    :param qty_raw:
    :return: normalized quantity
    """
    if unit == "piece":
        q_piece: int = int(round(qty_raw))
        return float(max(1, q_piece))

    q_kg: float = round(float(qty_raw), 1)
    return 0.1 if q_kg < 0.1 else q_kg


def choose_your_items() -> None:
    """
    Demande au client de choisir un article et sa quantité
    :return: list[str, float]
    """
    stock: List[StockRow] = cast(List[StockRow], Stock.stock)
    _print_catalog_lines(stock)

    items_by_name: Dict[str, StockRow] = {
        d["name"].strip().casefold(): d for d in stock
    }
    client_info: ClientInfo = get_client_infos()
    client_id = f"{client_info['firstname']} {client_info['lastname']}"
    basket = Basket(client_id)
    want_to_buy = True
    while want_to_buy:
        item: StockRow | None = None
        while True:
            name = (
                input("Choose an item by name (or 'n' to finish): ").strip().casefold()
            )
            if name in ("n", "no", "q", "quit"):
                want_to_buy = False
                break
            item = items_by_name.get(name)
            if not item:
                print("Choose an item from the stock.")
                continue
            break

        if not want_to_buy:
            break

        assert item is not None
        unit = item["unit"]

        qty: float | None = None
        desired: float | None = None

        while True:
            qty_text = (
                input(f"Choose quantity (available={item['stock']} {unit}): ")
                .strip()
                .replace(",", ".")
            )
            try:
                qty_num = float(qty_text)
            except ValueError:
                print("Please enter a valid number.")
                continue

            if qty_num <= 0:
                print("Quantity must be > 0.")
                continue

            if unit == "piece" and not qty_num.is_integer():
                print("Please enter an integer for pieces.")
                continue

            desired = float(int(qty_num)) if unit == "piece" else float(qty_num)
            qn = _normalize_qty(unit, desired)
            if qn > item["stock"]:
                print(f"Quantity must be <= {item['stock']} {unit}.")
                continue

            qty = qn
            break

        assert qty is not None
        Stock.decrease(item["name"], qty)
        basket.add(item["name"], qty, item["price"])
        if qty != desired:
            print(f"(normalized from {desired:g} to {qty:g} {unit})")
        print(f"You add: {item['name']} x {qty:g} {unit} to your basket")

        want_to_buy = ask_yes_no(
            "Do you want to add another item? (y/n): ", default=None
        )

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
