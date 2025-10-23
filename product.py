from dataclasses import dataclass
from typing import Literal, ClassVar
from abc import ABC

# Unités possibles :
# - "kg" : on vend au kilo (avec des dixièmes)
# - "piece" : on vend à la pièce (entier)
Unit = Literal["kg", "piece"]

# Catégories possibles
Category = Literal["fruit", "vegetable"]


@dataclass
class Product(ABC):
    """
    Classe de base pour tous les produits (fruit & légume).

    - Normaliser les quantités (kg/pièce).
    - Centraliser les contrôles et mises à jour du stock.
    - Calculer le prix par défaut.
    - Stocker les instances créées.
    """

    products: ClassVar[list["Product"]] = []

    # Data produits
    name: str  # Nom affiché
    unit: Unit  # Unité : "kg" ou "piece"
    price: float  # Prix unitaire
    stock: float  # Stock : "kg" ou "piece"
    category: Category  # "fruit" ou "légume"

    def __post_init__(self) -> None:
        """
        Ajout de l'objet après la création à 'products : ClassVar[list["Product"]]'
        """
        Product.products.append(self)

    # ---------------- Helpers quantités & stock ----------------

    def normalize_qty(self, qty: float) -> float:
        """
        Normalisation de la quantité saisie par le client.
        - "piece" : arrondi à l'entier le plus proche, minimum 1.
        - "kg" : arrondi à 1 décimale, minimum 0.1 kg.
        """
        # "pièce"
        if self.unit == "piece":
            q = max(1, int(round(qty)))  # mini 1 pièce
            return float(q)
        # "kg"
        q = round(qty, 1)  # arrondir à 1 décimale
        return 0.1 if q < 0.1 else q  # mini 0.1 kg

    def can_sell(self, qty: float) -> bool:
        """
        Validation de la disponibilité après normalisation : 0 < quantité normalisée <= stock.
        """
        q = self.normalize_qty(qty)
        return 0 < q <= self.stock

    def reserve_possible(self, qty: float) -> float:
        """
        Quantité disponible, sans toucher au stock : min(quantité normalisée, stock).
        """
        q = self.normalize_qty(qty)
        if q <= 0:
            return 0.0
        return min(q, self.stock)

    def remove_stock(self, qty: float) -> None:
        """
        Déduction de la quantité du stock.
        """
        q = self.normalize_qty(qty)
        if q <= 0 or q > self.stock:
            raise ValueError(
                f"Pas assez de stock pour {self.name}. Demandé={q}, Stock={self.stock}"
            )
        self.stock = round(self.stock - q, 3)

    # ---------------- Prix ----------------

    def price_for(self, qty: float) -> float:
        """
        Calcul du prix total pour une quantité donnée.
        """
        q = self.normalize_qty(qty)
        return round(q * self.price, 2)


# ---------------- Catégories concrètes ----------------


@dataclass
class Fruit(Product):
    """
    Catégorie Fruit.
    """

    def __init__(self, name: str, unit: Unit, price: float, stock: float):
        super().__init__(
            name=name, unit=unit, price=price, stock=stock, category="fruit"
        )


@dataclass
class Vegetable(Product):
    """
    Catégorie Légume.
    """

    def __init__(self, name: str, unit: Unit, price: float, stock: float):
        super().__init__(
            name=name, unit=unit, price=price, stock=stock, category="vegetable"
        )
