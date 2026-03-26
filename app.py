from __future__ import annotations

import csv
from datetime import datetime
from pathlib import Path
from uuid import uuid4

from flask import Flask, redirect, render_template, request, url_for

app = Flask(__name__)

BASE_DIR = Path(__file__).resolve().parent
DATA_FILE = BASE_DIR / "dati.csv"
ACCOUNT_OPTIONS = ["Galvenais konts", "Krājkonts", "Skaidra nauda", "Karšu konts"]

dati: list[dict] = []


def parse_amount(value: str) -> float:
    cleaned = value.strip().replace(",", ".")
    amount = float(cleaned)
    if amount <= 0:
        raise ValueError("Summai jābūt lielākai par 0.")
    return round(amount, 2)


def parse_date(value: str) -> str:
    if not value:
        return datetime.today().strftime("%Y-%m-%d")
    datetime.strptime(value, "%Y-%m-%d")
    return value


def parse_account(value: str) -> str:
    account = value.strip()
    if account not in ACCOUNT_OPTIONS:
        raise ValueError("Izvēlies korektu kontu.")
    return account


def default_demo_records() -> list[dict]:
    return [
        {"id": "d1a4e901", "tips": "Ienākums", "summa": 980.00, "apraksts": "Vasaras darbs", "datums": "2022-06-14", "konts": "Galvenais konts"},
        {"id": "d1a4e902", "tips": "Izdevums", "summa": 120.00, "apraksts": "Telefons", "datums": "2022-07-02", "konts": "Karšu konts"},
        {"id": "d1a4e903", "tips": "Izdevums", "summa": 65.40, "apraksts": "Pārtika", "datums": "2022-09-19", "konts": "Skaidra nauda"},
        {"id": "d1a4e904", "tips": "Ienākums", "summa": 140.00, "apraksts": "Privātstundas", "datums": "2022-11-05", "konts": "Krājkonts"},
        {"id": "d1a4e905", "tips": "Izdevums", "summa": 210.00, "apraksts": "Ziemas jaka", "datums": "2022-12-11", "konts": "Karšu konts"},
        {"id": "d1a4e906", "tips": "Ienākums", "summa": 1120.00, "apraksts": "Prakses alga", "datums": "2023-02-03", "konts": "Galvenais konts"},
        {"id": "d1a4e907", "tips": "Izdevums", "summa": 84.50, "apraksts": "Sports", "datums": "2023-03-17", "konts": "Karšu konts"},
        {"id": "d1a4e908", "tips": "Ienākums", "summa": 95.00, "apraksts": "Dzimšanas diena", "datums": "2023-05-21", "konts": "Skaidra nauda"},
        {"id": "d1a4e909", "tips": "Izdevums", "summa": 180.00, "apraksts": "Ceļojums", "datums": "2023-07-08", "konts": "Galvenais konts"},
        {"id": "d1a4e910", "tips": "Ienākums", "summa": 1280.00, "apraksts": "Stipendija + darbs", "datums": "2023-10-01", "konts": "Galvenais konts"},
        {"id": "d1a4e911", "tips": "Izdevums", "summa": 52.30, "apraksts": "Kafejnīca", "datums": "2023-11-22", "konts": "Skaidra nauda"},
        {"id": "d1a4e912", "tips": "Izdevums", "summa": 340.00, "apraksts": "Datorspēļu konsole", "datums": "2023-12-18", "konts": "Karšu konts"},
        {"id": "d1a4e913", "tips": "Ienākums", "summa": 1500.00, "apraksts": "Alga", "datums": "2024-01-31", "konts": "Galvenais konts"},
        {"id": "d1a4e914", "tips": "Izdevums", "summa": 410.00, "apraksts": "Īre", "datums": "2024-02-02", "konts": "Galvenais konts"},
        {"id": "d1a4e915", "tips": "Izdevums", "summa": 72.15, "apraksts": "Abonementi", "datums": "2024-04-10", "konts": "Karšu konts"},
        {"id": "d1a4e916", "tips": "Ienākums", "summa": 260.00, "apraksts": "Blakus projekts", "datums": "2024-06-12", "konts": "Krājkonts"},
        {"id": "d1a4e917", "tips": "Izdevums", "summa": 96.00, "apraksts": "Degviela", "datums": "2024-08-05", "konts": "Galvenais konts"},
        {"id": "d1a4e918", "tips": "Ienākums", "summa": 1320.00, "apraksts": "Alga", "datums": "2024-10-03", "konts": "Galvenais konts"},
        {"id": "d1a4e919", "tips": "Izdevums", "summa": 205.00, "apraksts": "Kursa maksa", "datums": "2024-11-14", "konts": "Krājkonts"},
        {"id": "d1a4e920", "tips": "Ienākums", "summa": 1540.00, "apraksts": "Alga", "datums": "2025-01-06", "konts": "Galvenais konts"},
        {"id": "d1a4e921", "tips": "Izdevums", "summa": 430.00, "apraksts": "Dzīvoklis", "datums": "2025-01-08", "konts": "Galvenais konts"},
        {"id": "d1a4e922", "tips": "Ienākums", "summa": 180.00, "apraksts": "Bonuss", "datums": "2025-03-01", "konts": "Krājkonts"},
        {"id": "d1a4e923", "tips": "Izdevums", "summa": 118.00, "apraksts": "Pārtika", "datums": "2025-05-09", "konts": "Karšu konts"},
        {"id": "d1a4e924", "tips": "Ienākums", "summa": 1620.00, "apraksts": "Alga", "datums": "2025-09-02", "konts": "Galvenais konts"},
        {"id": "d1a4e925", "tips": "Izdevums", "summa": 245.00, "apraksts": "Brīvdienu ceļš", "datums": "2025-10-28", "konts": "Skaidra nauda"},
        {"id": "d1a4e926", "tips": "Izdevums", "summa": 620.00, "apraksts": "Zobārsts", "datums": "2025-11-19", "konts": "Karšu konts"},
        {"id": "d1a4e927", "tips": "Izdevums", "summa": 870.00, "apraksts": "Portatīvais dators", "datums": "2025-12-03", "konts": "Krājkonts"},
        {"id": "d1a4e928", "tips": "Ienākums", "summa": 210.00, "apraksts": "Nodokļu atmaksa", "datums": "2025-12-21", "konts": "Galvenais konts"},
        {"id": "d1a4f001", "tips": "Ienākums", "summa": 1450.00, "apraksts": "Alga", "datums": "2026-03-02", "konts": "Galvenais konts"},
        {"id": "d1a4f002", "tips": "Izdevums", "summa": 420.50, "apraksts": "Dzīvokļa īre", "datums": "2026-03-03", "konts": "Galvenais konts"},
        {"id": "d1a4f003", "tips": "Izdevums", "summa": 89.20, "apraksts": "Pārtika", "datums": "2026-03-05", "konts": "Karšu konts"},
        {"id": "d1a4f004", "tips": "Ienākums", "summa": 120.00, "apraksts": "Freelance darbs", "datums": "2026-03-08", "konts": "Krājkonts"},
        {"id": "d1a4f005", "tips": "Izdevums", "summa": 36.80, "apraksts": "Transports", "datums": "2026-03-10", "konts": "Skaidra nauda"},
        {"id": "d1a4f006", "tips": "Izdevums", "summa": 54.99, "apraksts": "Internets", "datums": "2026-03-11", "konts": "Galvenais konts"},
        {"id": "d1a4f007", "tips": "Ienākums", "summa": 210.00, "apraksts": "Pārdots velosipēds", "datums": "2026-02-18", "konts": "Galvenais konts"},
        {"id": "d1a4f008", "tips": "Izdevums", "summa": 160.00, "apraksts": "Medicīna", "datums": "2026-02-21", "konts": "Karšu konts"},
        {"id": "d1a4f009", "tips": "Ienākums", "summa": 80.00, "apraksts": "Dāvana", "datums": "2026-01-12", "konts": "Skaidra nauda"},
        {"id": "d1a4f010", "tips": "Izdevums", "summa": 240.00, "apraksts": "Komunālie", "datums": "2026-01-15", "konts": "Galvenais konts"},
        {"id": "d1a4f011", "tips": "Izdevums", "summa": 690.00, "apraksts": "Auto remonts", "datums": "2026-02-28", "konts": "Galvenais konts"},
        {"id": "d1a4f012", "tips": "Izdevums", "summa": 305.00, "apraksts": "Apdrošināšana", "datums": "2026-03-06", "konts": "Krājkonts"},
        {"id": "d1a4f013", "tips": "Izdevums", "summa": 145.00, "apraksts": "Elektrība", "datums": "2026-03-07", "konts": "Galvenais konts"},
        {"id": "d1a4f014", "tips": "Izdevums", "summa": 980.00, "apraksts": "Ceļojuma rezervācija", "datums": "2026-03-09", "konts": "Karšu konts"},
        {"id": "d1a4f016", "tips": "Izdevums", "summa": 58.40, "apraksts": "Pārtikas papildinājums", "datums": "2026-03-18", "konts": "Karšu konts"},
        {"id": "d1a4f017", "tips": "Izdevums", "summa": 74.99, "apraksts": "Mobilais sakars", "datums": "2026-03-19", "konts": "Galvenais konts"},
        {"id": "d1a4f018", "tips": "Izdevums", "summa": 129.00, "apraksts": "Apģērbs", "datums": "2026-03-21", "konts": "Karšu konts"},
        {"id": "d1a4f019", "tips": "Izdevums", "summa": 43.60, "apraksts": "Degviela", "datums": "2026-03-22", "konts": "Skaidra nauda"},
        {"id": "d1a4f020", "tips": "Izdevums", "summa": 215.00, "apraksts": "Mēbeļu iemaksa", "datums": "2026-03-24", "konts": "Krājkonts"},
        {"id": "d1a4f015", "tips": "Ienākums", "summa": 340.00, "apraksts": "Projekta avanss", "datums": "2026-03-26", "konts": "Galvenais konts"},
    ]


def ensure_demo_data() -> None:
    demo_records = default_demo_records()
    existing_ids = {item["id"] for item in dati}
    missing_demo = [item for item in demo_records if item["id"] not in existing_ids]
    if missing_demo:
        dati.extend(missing_demo)
        dati.sort(key=lambda item: (item["datums"], item["id"]))
        save_data()


def load_data() -> None:
    dati.clear()
    if not DATA_FILE.exists():
        ensure_demo_data()
        return

    with DATA_FILE.open("r", encoding="utf-8-sig", newline="") as file:
        reader = csv.DictReader(file)
        for row in reader:
            try:
                dati.append(
                    {
                        "id": row["id"],
                        "tips": row["tips"],
                        "summa": round(float(row["summa"]), 2),
                        "apraksts": row["apraksts"],
                        "datums": row["datums"],
                        "konts": row.get("konts", "Galvenais konts") or "Galvenais konts",
                    }
                )
            except (KeyError, ValueError):
                continue

    ensure_demo_data()


def save_data() -> None:
    with DATA_FILE.open("w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(
            file, fieldnames=["id", "tips", "summa", "apraksts", "datums", "konts"]
        )
        writer.writeheader()
        writer.writerows(dati)


def calculate_totals(records: list[dict]) -> dict:
    ienakumi = sum(item["summa"] for item in records if item["tips"] == "Ienākums")
    izdevumi = sum(item["summa"] for item in records if item["tips"] == "Izdevums")
    bilance = ienakumi - izdevumi
    return {
        "ienakumi": round(ienakumi, 2),
        "izdevumi": round(izdevumi, 2),
        "bilance": round(bilance, 2),
    }


def build_dashboard_data(records: list[dict]) -> dict:
    totals = calculate_totals(records)
    total_flow = totals["ienakumi"] + totals["izdevumi"]
    income_share = 0 if total_flow == 0 else round((totals["ienakumi"] / total_flow) * 100)
    expense_share = 0 if total_flow == 0 else 100 - income_share

    month_groups: dict[str, dict[str, float]] = {}
    for item in sorted(records, key=lambda record: record["datums"]):
        month_key = item["datums"][:7]
        bucket = month_groups.setdefault(month_key, {"ienakumi": 0.0, "izdevumi": 0.0})
        if item["tips"] == "Ienākums":
            bucket["ienakumi"] += item["summa"]
        else:
            bucket["izdevumi"] += item["summa"]

    month_chart = []
    for month_key, values in list(month_groups.items())[-6:]:
        month_total = max(values["ienakumi"], values["izdevumi"], 1)
        month_chart.append(
            {
                "label": month_key,
                "income_height": max(14, round((values["ienakumi"] / month_total) * 100)),
                "expense_height": max(14, round((values["izdevumi"] / month_total) * 100)),
            }
        )

    if not month_chart:
        month_chart = [
            {"label": "Nav", "income_height": 14, "expense_height": 14},
            {"label": "datu", "income_height": 14, "expense_height": 14},
            {"label": "šim", "income_height": 14, "expense_height": 14},
            {"label": "skatam", "income_height": 14, "expense_height": 14},
        ]

    recent_count = len([item for item in records if item["datums"] >= datetime.today().strftime("%Y-%m-01")])
    average_value = 0 if not records else round(total_flow / len(records), 2)
    largest_expense = max(
        (item["summa"] for item in records if item["tips"] == "Izdevums"),
        default=0,
    )
    account_totals = []
    for account in ACCOUNT_OPTIONS:
        income = sum(item["summa"] for item in records if item["konts"] == account and item["tips"] == "Ienākums")
        expense = sum(item["summa"] for item in records if item["konts"] == account and item["tips"] == "Izdevums")
        account_totals.append(
            {
                "name": account,
                "balance": round(income - expense, 2),
                "income": round(income, 2),
                "expense": round(expense, 2),
            }
        )

    timeline_source = sorted(records, key=lambda item: item["datums"])[-14:]
    if timeline_source:
        max_value = max((item["summa"] for item in timeline_source), default=1)
        income_points = []
        expense_points = []
        timeline_labels = []
        for index, item in enumerate(timeline_source):
            x = 6 if len(timeline_source) == 1 else round((index / (len(timeline_source) - 1)) * 88 + 6, 2)
            y = round(90 - ((item["summa"] / max_value) * 64), 2)
            if item["tips"] == "Ienākums":
                income_points.append(f"{x},{y}")
                expense_points.append(f"{x},90")
            else:
                income_points.append(f"{x},90")
                expense_points.append(f"{x},{y}")
            timeline_labels.append(
                {"label": item["datums"][5:], "tips": item["tips"], "summa": round(item["summa"], 2)}
            )
    else:
        income_points = ["6,90", "94,90"]
        expense_points = ["6,90", "94,90"]
        timeline_labels = []

    return {
        "income_share": income_share,
        "expense_share": expense_share,
        "month_chart": month_chart,
        "recent_count": recent_count,
        "average_value": average_value,
        "largest_expense": round(largest_expense, 2),
        "account_totals": account_totals,
        "income_line_points": " ".join(income_points),
        "expense_line_points": " ".join(expense_points),
        "timeline_labels": timeline_labels,
    }


def filter_records(
    tips_filter: str = "Visi", month_filter: str = "", account_filter: str = "Visi konti"
) -> list[dict]:
    records = dati[:]

    if tips_filter in {"Ienākums", "Izdevums"}:
        records = [item for item in records if item["tips"] == tips_filter]

    if month_filter:
        records = [item for item in records if item["datums"].startswith(month_filter)]

    if account_filter in ACCOUNT_OPTIONS:
        records = [item for item in records if item["konts"] == account_filter]

    return sorted(records, key=lambda item: (item["datums"], item["id"]), reverse=True)


def build_history_preview(records: list[dict], limit: int = 6) -> tuple[list[dict], list[dict]]:
    if len(records) <= limit:
        return records, []

    preview = records[:limit]
    expense_count = sum(1 for item in preview if item["tips"] == "Izdevums")

    if expense_count == 0:
        first_expense = next((item for item in records[limit:] if item["tips"] == "Izdevums"), None)
        if first_expense is not None:
            preview[-1] = first_expense

    seen_ids = {item["id"] for item in preview}
    remaining = [item for item in records if item["id"] not in seen_ids]
    return preview, remaining


@app.route("/")
def index():
    tips_filter = request.args.get("tips", "Visi")
    month_filter = request.args.get("menesis", "")
    account_filter = request.args.get("konts", "Visi konti")
    records = filter_records(tips_filter, month_filter, account_filter)
    preview_records, remaining_records = build_history_preview(records)
    totals = calculate_totals(records)
    dashboard = build_dashboard_data(records)

    return render_template(
        "index.html",
        dati=records,
        preview_records=preview_records,
        remaining_records=remaining_records,
        totals=totals,
        dashboard=dashboard,
        tips_filter=tips_filter,
        month_filter=month_filter,
        account_filter=account_filter,
        account_options=ACCOUNT_OPTIONS,
        today=datetime.today().strftime("%Y-%m-%d"),
        error=request.args.get("error", ""),
    )


@app.route("/pievienot", methods=["POST"])
def pievienot():
    tips = request.form.get("tips", "").strip()
    summa_raw = request.form.get("summa", "")
    apraksts = request.form.get("apraksts", "").strip()
    datums_raw = request.form.get("datums", "").strip()
    konts_raw = request.form.get("konts", "").strip()

    try:
        if tips not in {"Ienākums", "Izdevums"}:
            raise ValueError("Norādi korektu ieraksta tipu.")
        if not apraksts:
            raise ValueError("Apraksts nedrīkst būt tukšs.")

        ieraksts = {
            "id": str(uuid4())[:8],
            "tips": tips,
            "summa": parse_amount(summa_raw),
            "apraksts": apraksts,
            "datums": parse_date(datums_raw),
            "konts": parse_account(konts_raw),
        }
        dati.append(ieraksts)
        save_data()
    except ValueError as error:
        return redirect(url_for("index", error=str(error)))

    return redirect(url_for("index"))


@app.route("/dzest/<entry_id>", methods=["POST"])
def dzest(entry_id: str):
    index_to_remove = next(
        (idx for idx, item in enumerate(dati) if item["id"] == entry_id), None
    )

    if index_to_remove is not None:
        dati.pop(index_to_remove)
        save_data()

    return redirect(url_for("index"))


@app.route("/bilance")
def bilance():
    totals = calculate_totals(dati)
    records = sorted(dati, key=lambda item: (item["datums"], item["id"]), reverse=True)
    dashboard = build_dashboard_data(dati)
    return render_template("balance.html", totals=totals, dati=records, dashboard=dashboard)


load_data()


if __name__ == "__main__":
    app.run(debug=True)
