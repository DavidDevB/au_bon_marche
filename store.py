from typing import List
from catalog import Catalog
from client import Client
from cart import Cart


class Store:
    """Catalog, customers & interactive CLI."""

    def __init__(self, catalog: Catalog):
        self.catalog = catalog
        self.clients: List[Client] = []

    # ---------- I/O ----------

    def run(self) -> None:
        """
        Role :
        - 'Client' routes to the shopping flow
        - 'Gérant' routes to management views (sales, stock, catalog)
        """
        while True:
            print("\n=== AU BON MARCHÉ ===")
            print("Qui es-tu ?")
            print("[1] Client")
            print("[2] Gérant")
            print("[3] Quitter")
            role_choice = input("> ").strip()

            if role_choice == "1":
                self._serve_new_client()
            elif role_choice == "2":
                self._manager_menu()
            elif role_choice == "3":
                print("Au revoir !")
                return
            else:
                print("Choix invalide.")

    # ---------- Manager area ----------

    def _manager_menu(self) -> None:
        """
        Manager menu :
        - Sales report: totals per customer (no stock lines)
        - Stock: remaining quantities only (no prices)
        - Catalog: prices + stock (read-only)
        """
        while True:
            print("\n=== Espace Gérant ===")
            print("[1] Bilan de la journée (ventes)")
            print("[2] Stock restant")
            print("[3] Catalogue (prix + stock)")
            print("[4] Retour")
            choice = input("> ").strip()

            if choice == "1":
                self.print_sales_report()
            elif choice == "2":
                self.print_stock_overview()
            elif choice == "3":
                self.print_catalog()
            elif choice == "4":
                return
            else:
                print("Choix invalide.")

    # ---------- Customer helpers----------

    def _find_client(self, firstname: str, lastname: str) -> Client | None:
        """Return existing client matching names (case-insensitive)."""
        fn = firstname.strip().lower()
        ln = lastname.strip().lower()
        for c in self.clients:
            if c.firstname.strip().lower() == fn and c.lastname.strip().lower() == ln:
                return c
        return None

    def _get_or_create_client(self, firstname: str, lastname: str) -> Client:
        """Find existing client or create a new one."""
        existing = self._find_client(firstname, lastname)
        if existing:
            return existing
        new_client = Client(firstname=firstname, lastname=lastname)
        self.clients.append(new_client)
        return new_client

    # ---------- Customer flow ----------

    def _serve_new_client(self) -> None:
        """
        Create or reuse client identity, open a new cart
        and checkout only upon confirmation (stock's updated at checkout).
        """
        print("\n=== Espace Client ===")
        firstname = input("Prénom : ").strip()
        lastname = input("Nom : ").strip()

        # Detect known or new customer
        existing = self._find_client(firstname, lastname)
        client = self._get_or_create_client(firstname, lastname)
        cart = Cart()

        if existing:
            commands = len(client.orders)

            if commands == 0:
                print(
                    f"Heureux de te revoir {client.full_name()} — prêt·e à commencer ?"
                )
            else:
                print(
                    f"Heureux de te revoir {client.full_name()} — {commands} visite(s) validée(s)."
                )
        else:
            print(f"Bienvenue {client.full_name()} !")

        self._shopping_menu(cart)

        if cart.is_empty():
            print("Panier vide, au revoir.")
            return

        print("\nAperçu du ticket :")
        print(cart.receipt_text())

        confirm = input("Valider et payer ? (o/n) ").strip().lower()
        if confirm == "o":
            total = cart.checkout()
            client.add_order(cart)  # Record this command only after successful checkout
            print("\nTicket final:")
            print(cart.receipt_text())
            print(f"Montant encaissé: {total:.2f} €")
        else:
            print("Achat annulé, aucun stock déduit.")

    def _shopping_menu(self, cart: Cart) -> None:
        """
        Loop to add products to cart:
        - Show catalog (price + stock)
        - Ask for product name and quantity
        - Add to cart
        """
        while True:
            print("\n--- Catalogue ---")
            for p in self.catalog.all():
                print(
                    f"- {p.name:<20} {p.price:.2f} €/ {p.unit:<5} | stock: {p.stock:g} {p.unit}"
                )

            print("\nActions: ")
            print("[1] Ajouter un produit")
            print("[2] Terminer")
            choice = input("> ").strip()

            if choice == "1":
                name = input("Nom du produit (exact) : ").strip()
                product = self.catalog.get(name)
                if not product:
                    print("Produit introuvable.")
                    continue
                try:
                    qty_text = (
                        input(f"Quantité ({product.unit}) : ").strip().replace(",", ".")
                    )
                    qty = float(qty_text)
                except ValueError:
                    print("Quantité invalide.")
                    continue

                try:
                    item = cart.add(product, qty)
                    print(
                        f"Ajouté: {product.name} x {item.normalized():g} {product.unit}"
                    )
                    print(f"Total panier: {cart.total():.2f} €")
                except ValueError as e:
                    print(str(e))
            elif choice == "2":
                return
            else:
                print("Choix invalide.")

    # ---------- Manager reports ----------

    def print_sales_report(self) -> None:
        """Show aggregated sales by customer"""
        print("\n=== Bilan ===")
        if not self.clients or all(len(c.orders) == 0 for c in self.clients):
            print("Aucun achat validé aujourd'hui.")
            return

        grand_total = 0.0
        idx = 1
        for c in self.clients:
            if len(c.orders) == 0:
                continue
            total = c.total_spent()
            grand_total += total
            commands = len(c.orders)
            print(
                f"{idx:02d}. {c.full_name():<30} Visites: {commands:<2} Total: {total:.2f} €"
            )
            idx += 1

        print(f"\nTotal encaissé : {grand_total:.2f} €")

    def print_stock_overview(self) -> None:
        """Display remaining stock only."""
        print("\n--- Stock restant ---")
        has_any = False
        for p in self.catalog.all():
            has_any = True
            print(f"- {p.name:<20} {p.stock:g} {p.unit}")
        if not has_any:
            print("Catalogue vide.")

    def print_catalog(self) -> None:
        """Display current catalog with prices & stock."""
        print("\n--- Catalogue ---")
        for p in self.catalog.all():
            print(
                f"- {p.name:<20} {p.price:.2f} €/ {p.unit:<5} | stock: {p.stock:g} {p.unit}"
            )
