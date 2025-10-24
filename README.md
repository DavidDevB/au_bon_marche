# Au bon marché

Logiciel de simulation de vente/achat de fruits et légumes

## Installation

- Installer Python 3 sur votre machine
- Télécharger l'ensemble des fichiers
- Lancer le script main.py dans un terminal
- Suivre les indications

## Fonctionnalités

- Entrée des noms et prénoms du client de la boutique
- Choix de l'article à acheter
- Choix de la quantité
- Impression du ticket de caisse client
- Impression du bilan de la journée de la boutique côté vendeur

## Structure

Le logiciel est principalement codé en POO (programmation orienté objet) et utilise des classes pour chaque fonctionnalité:

- au_bon_marché.py:
  - client_or_owner()
  - buy_items()

- basket.py:
  - Basket:
    - __init__()
    - remove()
    - total()
    - validate()
  
  - BasketStore:
    - __init__()
    - get_basket()
    - remove_basket()

- client.py:
  - Client:
    - __init__()
    - get_client_infos()
  
- fruit.py:
  - @dataclass Fruit

- main.py:
  - programme principal

- stock.py:
  - dataclass Stock
  - @classmethod find()
  - @classmethod decrease()
  - @classmethod restock()

- summary.py
  - __init__()
  - add_each_client_summary()
  - __repr__()

- ticket.py
  - __init__()
  - add()
  - total()
  - get_ticket()
  - @staticmethod split_lower_upper()
  - client_name()
  - _as_string()
  - __str__()
  - __repr__()