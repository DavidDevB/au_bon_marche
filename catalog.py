from dataclasses import dataclass, field
from typing import Dict, Iterable, ClassVar
from product import Product, Fruit, Vegetable


@dataclass
class Catalog:
    """
    Catalogue

    - Stock des produits : key = nom du produit en minuscules.
    - Méthodes : ajouter, récupérer par nom, lister, filtrer par catégorie.
    """

    catalogs: ClassVar[list["Catalog"]] = []

    # field(default_factory=dict) : crée un NOUVEAU dict pour CHAQUE Catalog()
    _products: Dict[str, Product] = field(default_factory=dict)

    def __post_init__(self) -> None:
        """
        Ajout de l'objet après la création à 'catalogs: ClassVar[list["Catalog"]] = []'
        """
        Catalog.catalogs.append(self)

    # ------------------ Helpers  ---------------------------------------------------------

    @staticmethod
    def _key(name: str) -> str:
        """Normalisation de la clef."""
        return name.strip().lower()

    # ------------------ API  -------------------------------------------------------------

    def add(self, product: Product) -> None:
        """
        Ajout d'un produit.
        """
        key = self._key(product.name)
        self._products[key] = product

    def get(self, name: str) -> Product | None:
        """
        Recherche d'un produit par nom (insensible à la casse & aux espaces).
        """
        return self._products.get(self._key(name))

    def all(self) -> Iterable[Product]:
        """
        Tous les produits du catalogue.
        """
        return self._products.values()

    # ------------------ Données par défaut ------------------

    def load_default(self) -> None:
        """
        Jeu de données fruits et légumes
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
        # Fruits (pièce)
        self.add(Fruit("Pamplemousse", "piece", 2.00, 8.0))

        # Légumes (kg)
        self.add(Vegetable("Carotte", "kg", 1.30, 7.0))
        self.add(Vegetable("Choux de Bruxelles", "kg", 4.00, 4.0))
        self.add(Vegetable("Endive", "kg", 2.50, 5.0))
        self.add(Vegetable("Épinard", "kg", 2.60, 4.0))
        self.add(Vegetable("Poireau", "kg", 1.20, 5.0))
        self.add(Vegetable("Salsifis", "kg", 2.50, 3.0))

        # Légumes (pièce)
        self.add(Vegetable("Chou vert", "piece", 2.50, 12.0))
        self.add(Vegetable("Courge butternut", "piece", 2.50, 6.0))
        self.add(Vegetable("Potiron", "piece", 2.50, 6.0))
        self.add(Vegetable("Radis noir", "piece", 5.00, 10.0))
