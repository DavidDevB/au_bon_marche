
from ticket import Ticket

class Summary:

    """
    Classe Summary représentant le bilan de la journée. Peut retourner la liste des achats faits par tous les clients de la journée.
    """

    def __init__(self):
        self.summaries: list = []

    def add_each_client_summary(self, client_id: str, new_ticket: Ticket) -> None:
        items = new_ticket.get_ticket()
        print(f"Items: {items}") #TODO CORRIGER ERREUR CAR PAS DE CLE "TYPE" dans ITEMS
        fruits = sum(int(d.get("quantity", 0)) for d in items if (d.get("type").lower() == "fruit"))
        vegetables = sum(int(d.get("quantity", 0)) for d in items if (d.get("type").lower() == "vegetable"))
        total = sum(float(d.get("subtotal", 0.0)) for d in items)
        client_summary = {"client": client_id, "total_fruits": fruits, "total_vegetables": vegetables, "total": total}
        self.summaries.append(client_summary)


    def __repr__(self):
        total_fruits = sum(d.get("total_fruits", 0) for d in self.summaries)
        total_vegetables = sum(d.get("total_vegetables", 0) for d in self.summaries)
        total_revenue = sum(d.get("total_revenue", 0) for d in self.summaries)
        return(
        "Summary of the day:\n"
        "You sold:\n"
        f"{total_fruits} fruits\n"
        f"{total_vegetables} vegetables\n"
        f"For {total_revenue}"
        )
