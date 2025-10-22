from dataclasses import dataclass, field
from typing import List
from product import Product


@dataclass
class CartItem:
    """Single line in shopping cart."""

    product: Product
    quantity: float  # Requested quantity (not yet deducted from stock)

    def normalized(self) -> float:
        """Return the product normalized quantity (kg rounded to 0.1, pieces rounded to int)."""
        return self.product.normalize_qty(self.quantity)

    def subtotal(self) -> float:
        """Compute total price for this line without altering stock."""
        return self.product.price_for(self.quantity)


@dataclass
class Cart:
    """Shopping cart. Stock is updated on checkout."""

    items: List[CartItem] = field(default_factory=list)

    def add(self, product: Product, qty: float) -> CartItem:
        """
        Add an item to the cart without mutating stock yet.
        If the requested quantity exceeds stock, it is capped to the available amount.
        """
        q = product.reserve_possible(qty)
        if q <= 0:
            raise ValueError(f"No available stock for {product.name}.")
        item = CartItem(product=product, quantity=q)
        self.items.append(item)
        return item

    def total(self) -> float:
        """Sum of all line subtotals."""
        return round(sum(i.subtotal() for i in self.items), 2)

    def is_empty(self) -> bool:
        return len(self.items) == 0

    def receipt_text(self) -> str:
        """Build a human-readable ticket for console."""
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
        Deduct stock for each item & return total.
        """
        # First pass: validate
        for it in self.items:
            q = it.normalized()
            if not it.product.can_sell(q):
                raise ValueError(
                    f"Insufficient stock for {it.product.name} at checkout."
                )

        # Second pass: update stock
        for it in self.items:
            q = it.normalized()
            it.product.remove_stock(q)

        return self.total()
