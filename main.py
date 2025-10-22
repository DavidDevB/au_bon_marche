from catalog import Catalog
from store import Store


def main() -> None:
    """Load catalog & start CLI."""
    catalog = Catalog()
    catalog.load_default()
    store = Store(catalog)
    store.run()


if __name__ == "__main__":
    main()
