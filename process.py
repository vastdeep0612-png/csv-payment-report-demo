"""DEMO PROJECT. Self-initiated sample. Not a client file.

Read a CSV of orders and write the paid rows, a total, an error list,
and a short report. Refunded rows are excluded. Invalid amounts are
excluded. A repeated order id is kept once.
"""

import csv
from decimal import Decimal, InvalidOperation
from pathlib import Path


def parse_amount(raw):
    text = (raw or "").strip()
    if text == "":
        raise ValueError("empty_amount")
    if any(mark in text for mark in ("$", "€", "£")):
        raise ValueError("currency_symbol")
    try:
        amount = Decimal(text)
    except InvalidOperation as exc:
        raise ValueError("not_a_number") from exc
    return amount.quantize(Decimal("0.01"))


def build_report(rows):
    paid = []
    errors = []
    skipped = []
    seen = set()
    for row in rows:
        order_id = (row.get("order_id") or "").strip()
        status = (row.get("status") or "").strip().lower()
        amount_raw = row.get("amount") or ""
        record = {"order_id": order_id, "status": status, "amount": amount_raw.strip()}
        if status != "paid":
            skipped.append({**record, "reason": "status_not_paid"})
            continue
        if order_id in seen:
            errors.append({**record, "reason": "duplicate_order_id"})
            continue
        try:
            amount = parse_amount(amount_raw)
        except ValueError as exc:
            errors.append({**record, "reason": str(exc)})
            continue
        seen.add(order_id)
        paid.append({"order_id": order_id, "amount": f"{amount:.2f}"})
    total = sum((Decimal(item["amount"]) for item in paid), Decimal("0.00"))
    return {
        "paid": paid,
        "errors": errors,
        "skipped": skipped,
        "total": f"{total:.2f}",
    }


def read_csv(path):
    with Path(path).open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_outputs(result, output_dir):
    folder = Path(output_dir)
    folder.mkdir(parents=True, exist_ok=True)
    paid_path = folder / "sample_output.csv"
    error_path = folder / "sample_errors.csv"
    report_path = folder / "sample_report.txt"
    with paid_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=["order_id", "amount"])
        writer.writeheader()
        writer.writerows(result["paid"])
        writer.writerow({"order_id": "TOTAL", "amount": result["total"]})
    with error_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=["order_id", "status", "amount", "reason"])
        writer.writeheader()
        writer.writerows(result["errors"])
    lines = [
        "DEMO PROJECT. Self-initiated sample. Not a client file.",
        f"valid_paid_rows: {len(result['paid'])}",
        f"valid_payments_total: {result['total']}",
        f"excluded_not_paid: {len(result['skipped'])}",
        f"invalid_or_duplicate_rows: {len(result['errors'])}",
    ]
    report_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return paid_path, error_path, report_path


def main():
    here = Path(__file__).resolve().parent
    result = build_report(read_csv(here / "sample.csv"))
    write_outputs(result, here)
    print(f"DEMO valid payments total {result['total']}")


if __name__ == "__main__":
    main()
