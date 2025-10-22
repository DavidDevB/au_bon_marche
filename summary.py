
class Summary:

    """
    Classe Summary représentant le bilan de la journée. Peut retourner la liste des achats faits par tous les clients de la journée.
    """

    def __init__(self, summary: list[dict]):
        self.summary = summary

    summaries_by_client = []
    for el in summary:
        el[firstname] = el.firstname
        el[lastname] = el.lastname
        el[total] = el.total

    def __repr__(self):
        print("Summary of the day:")
