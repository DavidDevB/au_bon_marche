from dataclasses import dataclass, field
from typing import List, ClassVar
from catalog import Catalog
from client import Client
from cart import Cart


@dataclass
class Store:
    """
    Classe du "magasin"
    """

    stores: ClassVar[list["Store"]] = []

    catalog: Catalog

    # Liste des clients connus
    # field(default_factory=list) : crée une nouvelle liste vide pour chaque instanciation.
    # Si on faisait items = [], toutes les instances partageraient la même liste.
    # Sans default_factory, la liste serait créée une seule fois au chargement de la classe et PARTAGÉE par toutes les instances.
    # Exemple :
    # s1 = Store(catalog); s2 = Store(catalog)
    # s1.clients.append(Client("Alice", "Dupont"))
    # len(s1.clients)  -> 1
    # len(s2.clients)  -> 0
    # avec clients = [] les deux auraient -> 1

    clients: List[Client] = field(default_factory=list)

    def __post_init__(self) -> None:
        """Ajout de l'objet après la création à 'stores : ClassVar[list["Store"]] = []'"""
        Store.stores.append(self)

    # ---------- I/O ------------------------------------------------------------------------

    def run(self) -> None:
        """
        Menu principal :
        - "Client" : parcours d'achat.
        - "Gérant" : ventes, stock, catalogue.
        - "Quitter"
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

    # ---------- Espace Gérant ----------------------------------------------------

    def _manager_menu(self) -> None:
        """
        Menu gérant
        - Total par client.
        - Stock restant.
        - Catalogue.
        """
        while True:
            print("\n=== Espace Gérant ===")
            print("[1] Bilan de la journée")
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

    # ---------- Espace Client -------------------------------------------------------------------

    def _find_client(self, firstname: str, lastname: str) -> Client | None:
        """
        Recherche client par prénom/nom (insensible à la casse & aux espaces).
        """
        fn = firstname.strip().lower()
        ln = lastname.strip().lower()
        for c in self.clients:
            if c.firstname.strip().lower() == fn and c.lastname.strip().lower() == ln:
                return c
        return None

    def _get_or_create_client(self, firstname: str, lastname: str) -> Client:
        """
        Recherche d'un client existant ou en création le cas échéant.
        Ajout du nouveau client à la liste self.clients.
        """
        existing = self._find_client(firstname, lastname)
        if existing:
            return existing
        new_client = Client(firstname=firstname, lastname=lastname)
        self.clients.append(new_client)
        return new_client

    # ---------- Parcours Client (achat) -----------------------------------------------------------

    def _serve_new_client(self) -> None:
        """
        Gestion d'une vente :
        - Identification du client.
        - Création du panier.
        - Ajout des produits au panier.
        - Déduction du stock & enregistrement de la commande à la validation de l'achat.
        """
        print("\n=== Espace Client ===")
        firstname = input("Prénom : ").strip()
        lastname = input("Nom : ").strip()

        existing = self._find_client(firstname, lastname)
        client = self._get_or_create_client(firstname, lastname)

        # Nouveau panier
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

        # Ajout de produits au panier
        self._shopping_menu(cart)

        # Si panier vide
        if cart.is_empty():
            print("Panier vide, au revoir.")
            return

        # Aperçu du ticket avant confirmation
        print("\nAperçu du ticket :")
        print(cart.receipt_text())

        # Confirmation d'achat
        confirm = input("Valider et payer ? (o/n) ").strip().lower()
        if confirm == "o":
            total = cart.checkout()  # déduction du stock
            client.add_order(cart)  # enregistrement de la commande validée
            print("\nTicket final:")
            print(cart.receipt_text())
            print(f"Montant encaissé: {total:.2f} €")
        else:
            # Annulation
            print("Achat annulé, aucun stock déduit.")

    def _shopping_menu(self, cart: Cart) -> None:
        """
        Boucle pour remplir le panier
        - Affichage du catalogue.
        - Saisie du produit et de la quantité.
        - Ajout de la ligne au panier (avec bornage au stock si nécessaire).
        """
        while True:
            # Affichage du catalogue courant
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

                # Saisie de la quantité (on accepte la virgule pour les décimales)
                try:
                    qty_text = (
                        input(f"Quantité ({product.unit}) : ").strip().replace(",", ".")
                    )
                    qty = float(qty_text)
                except ValueError:
                    print("Quantité invalide.")
                    continue

                # Quantité "voulue" après normalisation
                # ex: 0.04 kg -> 0.1 kg ; 1.6 pièces -> 2
                desired = product.normalize_qty(qty)

                # Ajout au panier
                try:
                    item = cart.add(product, qty)

                    # Si quantité servie < quantité voulue : stock insuffisant
                    served = item.normalized()
                    if served < desired:
                        print(
                            f"⚠️ Stock insuffisant pour : {product.name} : "
                            f"Demandé {desired:g} {product.unit}, servi {served:g} {product.unit}."
                        )

                    print(f"Ajouté : {product.name} x {served:g} {product.unit}")
                    print(f"Total panier : {cart.total():.2f} €")

                except ValueError as err:
                    print(str(err))

            elif choice == "2":
                return
            else:
                print("Choix invalide.")

    # ---------- Rapports gérant -------------------------------------------------------------------

    def print_sales_report(self) -> None:
        """
        Affichage du bilan des ventes.
        - Pour chaque client avec au moins un achat validé.
        - Caisse de la journée.
        """
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
        """
        Affichage des quantités restantes par produit.
        """
        print("\n--- Stock restant ---")
        has_any = False
        for p in self.catalog.all():
            has_any = True
            print(f"- {p.name:<20} {p.stock:g} {p.unit}")
        if not has_any:
            print("Catalogue vide.")

    def print_catalog(self) -> None:
        """
        Affichage du catalogue complet.
        """
        print("\n--- Catalogue ---")
        for p in self.catalog.all():
            print(
                f"- {p.name:<20} {p.price:.2f} €/ {p.unit:<5} | stock: {p.stock:g} {p.unit}"
            )
