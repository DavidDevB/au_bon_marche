#!/usr/bin/env python
# -*- coding: utf-8 -*-
# filename: main.py
from au_bon_marche import client_or_owner, choose_your_items
from sales_log import DAY_SALES
from stock import Stock
from summary import Summary


def main() -> None:
    """Boucle pour le choix du rôle jusqu'à ce que l'utilisateur quitte"""
    while True:
        role = client_or_owner()
        if role == "quit":
            print("Goodbye!")
            break

        if role == "client":
            choose_your_items()
        else:
            print("\n=== STOCK OVERVIEW ===")
            for el in Stock.stock:
                unit = el["unit"]
                print(
                    f"- {el['name']:<20} {el['stock']} {unit} @ {el['price']:.2f}€/{unit}"
                )

            print()
            print(Summary(DAY_SALES).pretty_owner_report())


if __name__ == "__main__":
    main()
