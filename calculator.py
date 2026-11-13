"""Core logic for CloudCost: storage cost calculation and comparison.

Prices are illustrative (USD per GB per month), NOT live provider quotes.
"""
from __future__ import annotations

from dataclasses import dataclass
from datetime import date

GB_PER_TB = 1024

# Illustrative prices in USD per GB per month.
PRICING: dict[str, float] = {
    "AWS S3": 0.023,
    "Google Cloud": 0.020,
    "Microsoft Azure": 0.019,
}


@dataclass(frozen=True)
class Result:
    provider: str
    price_per_gb: float
    monthly_cost: float
    yearly_cost: float


def to_gb(amount: float, unit: str) -> float:
    """Convert an amount in GB or TB to GB."""
    unit = unit.strip().upper()
    if unit not in ("GB", "TB"):
        raise ValueError("Unit must be 'GB' or 'TB'.")
    if isinstance(amount, bool) or not isinstance(amount, (int, float)):
        raise ValueError("Storage amount must be a number.")
    if amount <= 0:
        raise ValueError("Storage amount must be greater than zero.")
    return float(amount) * (GB_PER_TB if unit == "TB" else 1)


def monthly_cost(storage_gb: float, price_per_gb: float) -> float:
    """Monthly cost, rounded to cents."""
    if storage_gb <= 0:
        raise ValueError("Storage must be greater than zero.")
    return round(storage_gb * price_per_gb, 2)


def compare(storage_gb: float, pricing: dict[str, float] | None = None) -> list[Result]:
    """Return results for every provider, cheapest first."""
    pricing = pricing or PRICING
    results = [
        Result(p, price, monthly_cost(storage_gb, price),
               round(monthly_cost(storage_gb, price) * 12, 2))
        for p, price in pricing.items()
    ]
    return sorted(results, key=lambda r: (r.monthly_cost, r.provider))


def cheapest(results: list[Result]) -> Result:
    if not results:
        raise ValueError("No results to compare.")
    return min(results, key=lambda r: r.monthly_cost)


def generate_report(storage_gb: float, results: list[Result]) -> str:
    """Plain-text cost comparison report."""
    best = cheapest(results)
    worst = max(results, key=lambda r: r.monthly_cost)
    saving = round(worst.monthly_cost - best.monthly_cost, 2)
    lines = [
        "CloudCost - Cloud Storage Cost Comparison Report",
        f"Date: {date.today().isoformat()}",
        f"Storage required: {storage_gb:,.2f} GB ({storage_gb / GB_PER_TB:,.3f} TB)",
        "",
        f"{'Provider':<18}{'Price/GB':>10}{'Monthly':>12}{'Yearly':>12}",
        "-" * 52,
    ]
    for r in results:
        lines.append(
            f"{r.provider:<18}{'$' + format(r.price_per_gb, '.3f'):>10}"
            f"{'$' + format(r.monthly_cost, ',.2f'):>12}"
            f"{'$' + format(r.yearly_cost, ',.2f'):>12}"
        )
    lines += [
        "",
        f"Result: {best.provider} is the cheapest at ${best.monthly_cost:,.2f}/month.",
        f"Saving vs most expensive ({worst.provider}): "
        f"${saving:,.2f}/month (${saving * 12:,.2f}/year).",
        "",
        "Note: Illustrative prices only, not live provider quotes.",
    ]
    return "\n".join(lines)


def results_to_csv(results: list[Result]) -> str:
    rows = ["Provider,Price per GB (USD),Monthly Cost (USD),Yearly Cost (USD)"]
    rows += [f"{r.provider},{r.price_per_gb:.3f},{r.monthly_cost:.2f},{r.yearly_cost:.2f}"
             for r in results]
    return "\n".join(rows) + "\n"
