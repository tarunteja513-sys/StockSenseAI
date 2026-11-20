import json
from pathlib import Path

from src.config import DATA_DIR


DATABASE_PATH = Path(DATA_DIR) / "company_database.json"


def load_companies():
    if not DATABASE_PATH.exists():
        return []

    try:
        with DATABASE_PATH.open("r", encoding="utf-8") as file:
            companies = json.load(file)

        if not isinstance(companies, list):
            raise ValueError("Database must contain a JSON list.")

        return companies

    except json.JSONDecodeError as error:
        raise ValueError("Company database contains invalid JSON.") from error


def save_companies(companies):
    if not isinstance(companies, list):
        raise TypeError("Companies must be a list.")

    DATABASE_PATH.parent.mkdir(parents=True, exist_ok=True)

    with DATABASE_PATH.open("w", encoding="utf-8") as file:
        json.dump(companies, file, indent=4, ensure_ascii=False)


def search_company(keyword):
    keyword = keyword.strip().lower()

    if not keyword:
        return []

    return [
        company for company in load_companies()
        if keyword in company.get("symbol", "").lower()
        or keyword in company.get("company", "").lower()
    ]


def add_company(company):
    required_fields = ["company", "symbol", "exchange", "sector"]

    if not isinstance(company, dict):
        return False

    for field in required_fields:
        if not isinstance(company.get(field), str) or not company[field].strip():
            return False

    companies = load_companies()

    for existing in companies:
        if (
            existing.get("symbol", "").upper() == company["symbol"].upper()
            and existing.get("exchange", "").upper() == company["exchange"].upper()
        ):
            return False

    companies.append(company)
    save_companies(companies)
    return True


def update_company(symbol, updated_data, exchange="NSE"):
    if not isinstance(updated_data, dict):
        return False

    companies = load_companies()

    for company in companies:
        if (
            company.get("symbol", "").upper() == symbol.upper()
            and company.get("exchange", "").upper() == exchange.upper()
        ):
            company.update(updated_data)
            save_companies(companies)
            return True

    return False


def get_all_companies():
    return load_companies()


def display_all():
    companies = load_companies()

    print("\nTOTAL COMPANIES:", len(companies))

    for company in companies:
        print(
            company.get("company", ""),
            "|",
            company.get("symbol", ""),
            "|",
            company.get("exchange", "")
        )
