from dataclasses import dataclass, field
from typing import List
from product import Product


@dataclass
class CartItem:
    """
    Une ligne du panier : produit & quantité.
    Pas de modification du stock à ce moment.
    """

    product: Product
    quantity: float

    def normalized(self) -> float:
        """
        Normalisation de la quantité
            pièces → entier min 1
            kg → 1 décimale min 0.1
        """
        return self.product.normalize_qty(self.quantity)

    def subtotal(self) -> float:
        """
        Calcul du prix de cette ligne.
        """
        return self.product.price_for(self.quantity)


@dataclass
class Cart:
    """
    Panier d'achat.
    """

    # field(default_factory=list) : crée une NOUVELLE liste pour CHAQUE panier.
    # Sans ça la liste serait partagée entre paniers.
    # Exemple :
    # c1 = Cart(); c2 = Cart()
    # c1.items.append(CartItem(product=some_product, quantity=1))
    # len(c1.items)  -> 1
    # len(c2.items)  -> 0
    # avec items = [] les deux auraient -> 1

    items: List[CartItem] = field(default_factory=list)

    def add(self, product: Product, qty: float) -> CartItem:
        """
        Ajout d'un produit au panier.
        """
        q = product.reserve_possible(qty)  # quantité normalisée & plafonnée au stock
        if q <= 0:
            raise ValueError(f"No available stock for {product.name}.")
        item = CartItem(product=product, quantity=q)
        self.items.append(item)
        return item

    def total(self) -> float:
        """
        Total du panier.
        """
        return round(sum(i.subtotal() for i in self.items), 2)

    def is_empty(self) -> bool:
        """Vérifie si le panier est vide."""
        return len(self.items) == 0

    def receipt_text(self) -> str:
        """
        Ticket de caisse.
        """
        lines: list[str] = ["===== Ticket de caisse ====="]
        for it in self.items:
            q = it.normalized()
            unit = it.product.unit
            price = it.product.price
            subtotal = it.subtotal()
            lines.append(
                f"- {it.product.name:<20} {q:g} {unit:<5} x {price:.2f} €  =  {subtotal:.2f} €"
            )
        lines.append("----------------------------")
        lines.append(f"TOTAL: {self.total():.2f} €")
        lines.append("============================")
        return "\n".join(lines)

    def checkout(self) -> float:
        """
        Validation du panier
        - Verification des stocks.
        - Mise à jour du stock.
        - Prix total.
        """
        # Verif stock
        for it in self.items:
            q = it.normalized()
            if not it.product.can_sell(q):
                raise ValueError(
                    f"Insufficient stock for {it.product.name} at checkout."
                )

        # MAJ stock
        for it in self.items:
            q = it.normalized()
            it.product.remove_stock(q)

        # Total panier
        return self.total()
