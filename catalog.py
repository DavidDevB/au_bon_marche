from typing import Dict, Iterable
from product import Product, Fruit, Vegetable


class Catalog:
    """Catalog storing all available products keyed by name."""

    def __init__(self) -> None:
        self._products: Dict[str, Product] = {}

    def add(self, product: Product) -> None:
        """Insert or replace a product in the catalog by its name."""
        key = product.name.lower()
        self._products[key] = product

    def get(self, name: str) -> Product | None:
        """Retrieve a product by name (case-insensitive)."""
        return self._products.get(name.lower())

    def all(self) -> Iterable[Product]:
        """Iterate over all products."""
        return self._products.values()

    def by_category(self, category: str) -> list[Product]:
        """Return products filtered by category."""
        return [p for p in self._products.values() if p.category == category]

    def __len__(self) -> int:
        return len(self._products)

    # ---------- Data ----------

    def load_default(self) -> None:
        """
        Load catalog :
        """
        # Fruits (kg)
        self.add(Fruit("Clémentine", "kg", 2.90, 6.0))
        self.add(Fruit("Datte", "kg", 7.00, 4.0))
        self.add(Fruit("Grenade", "kg", 3.50, 3.0))
        self.add(Fruit("Kaki", "kg", 4.50, 3.0))
        self.add(Fruit("Kiwi", "kg", 3.50, 5.0))
        self.add(Fruit("Mandarine", "kg", 2.80, 6.0))
        self.add(Fruit("Orange", "kg", 1.50, 8.0))
        self.add(Fruit("Poire", "kg", 2.50, 5.0))
        self.add(Fruit("Pomme", "kg", 1.50, 8.0))
        # Fruits (piece)
        self.add(Fruit("Pamplemousse", "piece", 2.00, 8.0))

        # Vegetables (kg)
        self.add(Vegetable("Carotte", "kg", 1.30, 7.0))
        self.add(Vegetable("Choux de Bruxelles", "kg", 4.00, 4.0))
        self.add(Vegetable("Endive", "kg", 2.50, 5.0))
        self.add(Vegetable("Épinard", "kg", 2.60, 4.0))
        self.add(Vegetable("Poireau", "kg", 1.20, 5.0))
        self.add(Vegetable("Salsifis", "kg", 2.50, 3.0))

        # Vegetables (piece)
        self.add(Vegetable("Chou vert", "piece", 2.50, 12.0))
        self.add(Vegetable("Courge butternut", "piece", 2.50, 6.0))
        self.add(Vegetable("Potiron", "piece", 2.50, 6.0))
        self.add(Vegetable("Radis noir", "piece", 5.00, 10.0))
