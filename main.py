from catalog import Catalog
from store import Store


def main() -> None:
    """Charge le catalogue et lance l'interaction"""
    catalog = Catalog()
    catalog.load_default()
    store = Store(catalog)
    store.run()


if __name__ == "__main__":
    main()
