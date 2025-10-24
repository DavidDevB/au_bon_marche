# filename: summary.py
from dataclasses import dataclass
from typing import List, Dict, Any, ClassVar

from sales_log import SaleRow


@dataclass
class Summary:
    """
    Day summary aggregator. Takes raw purchase rows and provides totals by client.
    Expected rows: {"firstname": str, "lastname": str, "total": float, ...}
    """

    summaries: ClassVar[List["Summary"]] = []

    summary: List[SaleRow]

    def __post_init__(self) -> None:
        Summary.summaries.append(self)

    def by_client(self) -> List[Dict[str, Any]]:
        agg: Dict[tuple[str, str], float] = {}
        for row in self.summary:
            fn = str(row.get("firstname", "")).strip()
            ln = str(row.get("lastname", "")).strip()
            total = float(row.get("total", 0.0))
            key = (fn, ln)
            agg[key] = agg.get(key, 0.0) + total
        return [
            {"firstname": k[0], "lastname": k[1], "total": round(v, 2)}
            for k, v in agg.items()
        ]

    def __repr__(self) -> str:
        lines = ["Summary of the day:"]
        for rec in self.by_client():
            lines.append(
                f"- {rec['firstname']} {rec['lastname']}: {rec['total']:.2f} €"
            )
        return "\n".join(lines)

    def by_client_detailed(self) -> List[Dict[str, Any]]:
        """
        Detailed per-client summary with merged lines per product:
        returns [{"firstname","lastname","total","lines":[{"name","quantity","subtotal","price"}]}]
        :return List[Dict[str, Any]]: detailed summary for client
        """
        clients: Dict[tuple[str, str], Dict[str, Any]] = {}

        for row in self.summary:
            fn = str(row.get("firstname", "")).strip()
            ln = str(row.get("lastname", "")).strip()
            items = row.get("items", []) or []
            total = float(row.get("total", 0.0))
            key = (fn, ln)

            entry = clients.setdefault(
                key, {"firstname": fn, "lastname": ln, "total": 0.0, "lines": {}}
            )
            entry["total"] = round(entry["total"] + total, 2)

            for it in items:
                name = str(it.get("name", ""))
                qty = float(it.get("quantity", 0.0))
                sub = float(it.get("subtotal", 0.0))
                price = float(it.get("price", 0.0))
                line = entry["lines"].setdefault(
                    name,
                    {"name": name, "quantity": 0.0, "subtotal": 0.0, "price": price},
                )
                line["quantity"] = round(line["quantity"] + qty, 3)
                line["subtotal"] = round(line["subtotal"] + sub, 2)

        result: List[Dict[str, Any]] = []
        for (_fn, _ln), data in clients.items():
            result.append(
                {
                    "firstname": data["firstname"],
                    "lastname": data["lastname"],
                    "total": data["total"],
                    "lines": list(data["lines"].values()),
                }
            )
        return result

    def pretty_owner_report(self) -> str:
        """
        Owner-friendly detailed report string.
        """
        blocks: List[str] = ["=== OWNER DAY SUMMARY ==="]
        detailed = self.by_client_detailed()
        if not detailed:
            blocks.append("No validated purchases yet.")
            return "\n".join(blocks)

        detailed.sort(key=lambda d: (d["lastname"].lower(), d["firstname"].lower()))
        day_total = round(sum(float(rec["total"]) for rec in detailed), 2)

        for rec in detailed:
            blocks.append(
                f"\n{rec['firstname']} {rec['lastname']} — TOTAL: {rec['total']:.2f} €"
            )
            for line in rec["lines"]:
                blocks.append(
                    f"  - {line['name']}: {line['quantity']} x @ {line['price']:.2f}€ = {line['subtotal']:.2f}€"
                )

        blocks.append(f"\n=== DAY TOTAL : {day_total:.2f} €")
        return "\n".join(blocks)

    @classmethod
    def nb_summaries(cls) -> int:
        return len(cls.summaries)
