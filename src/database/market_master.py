import csv
import json
from pathlib import Path

from src.config import DATA_DIR


DATA_PATH = Path(DATA_DIR)
NSE_FILE = DATA_PATH / "nse_companies.csv"
BSE_FILE = DATA_PATH / "bse_companies.csv"
MASTER_FILE = DATA_PATH / "master_company_database.json"


def normalize_row(row):
    """Normalize CSV column names and values."""
    return {
        str(key).strip().upper(): (
            str(value).strip() if value is not None else ""
        )
        for key, value in row.items()
        if key is not None
    }


def first_value(row, *names):
    """Return the first available non-empty field."""
    for name in names:
        value = row.get(name.upper(), "")
        if value:
            return value
    return ""


def read_exchange_csv(file_path, exchange):
    """Read and standardize company records from an exchange CSV."""
    file_path = Path(file_path)
    exchange = exchange.upper()

    if not file_path.exists():
        return []

    companies = []

    with file_path.open("r", encoding="utf-8-sig", newline="") as file:
        reader = csv.DictReader(file)

        if not reader.fieldnames:
            raise ValueError(f"Invalid CSV file: {file_path}")

        for original_row in reader:
            row = normalize_row(original_row)

            if exchange == "NSE":
                symbol = first_value(row, "SYMBOL")
                company_name = first_value(row, "NAME OF COMPANY")
                series = first_value(row, "SERIES")
                security_code = ""

                isin = first_value(row, "ISIN NUMBER", "ISIN NO", "ISIN")
                listing_date = first_value(
                    row, "DATE OF LISTING", "LISTING DATE"
                )
                face_value = first_value(row, "FACE VALUE")
                market_lot = first_value(row, "MARKET LOT")
                status = first_value(row, "STATUS") or "UNKNOWN"

            elif exchange == "BSE":
                symbol = first_value(row, "TCKRSYMB")
                company_name = first_value(row, "FININSTRMNM")
                series = first_value(row, "SCTYSRS")
                security_code = first_value(row, "FININSTRMID")

                isin = first_value(row, "ISIN")
                listing_date = first_value(row, "LISTGDT")
                face_value = first_value(row, "PARVAL")
                market_lot = first_value(
                    row, "NEWBRDLOTQTY", "MINLOT"
                )
                status = first_value(row, "STS") or "UNKNOWN"

            else:
                raise ValueError(f"Unsupported exchange: {exchange}")

            if not symbol or not company_name:
                continue

            company = {
                "company": company_name,
                "symbol": symbol.upper(),
                "exchange": exchange,
                "sector": first_value(row, "INDUSTRY", "SECTOR") or "UNKNOWN",
                "series": series or "UNKNOWN",
                "isin": isin,
                "listing_date": listing_date,
                "face_value": face_value,
                "paid_up_value": first_value(row, "PAID UP VALUE"),
                "market_lot": market_lot,
                "security_code": security_code,
                "status": status,
                "source": exchange
            }

            companies.append(company)

    return companies

def merge_companies(*company_lists):
    """Merge records without duplicate exchange-symbol combinations."""
    merged = {}

    for company_list in company_lists:
        for company in company_list:
            key = (
                company["exchange"].upper(),
                company["symbol"].upper()
            )

            if key not in merged:
                merged[key] = company
            else:
                for field, value in company.items():
                    if value and (
                        not merged[key].get(field)
                        or merged[key][field] == "UNKNOWN"
                    ):
                        merged[key][field] = value

    return sorted(
        merged.values(),
        key=lambda item: (item["exchange"], item["symbol"])
    )


def load_master_database():
    """Load the unified master database."""
    if not MASTER_FILE.exists():
        return []

    with MASTER_FILE.open("r", encoding="utf-8") as file:
        companies = json.load(file)

    if not isinstance(companies, list):
        raise ValueError("Master database must contain a JSON list.")

    return companies


def save_master_database(companies):
    """Save master records safely using a temporary file."""
    if not isinstance(companies, list):
        raise TypeError("Companies must be a list.")

    DATA_PATH.mkdir(parents=True, exist_ok=True)
    temporary_file = MASTER_FILE.with_suffix(".tmp")

    try:
        with temporary_file.open("w", encoding="utf-8") as file:
            json.dump(companies, file, indent=4, ensure_ascii=False)

        temporary_file.replace(MASTER_FILE)
    finally:
        if temporary_file.exists():
            temporary_file.unlink()


def build_master_database(
    nse_file=NSE_FILE,
    bse_file=BSE_FILE
):
    """Build the unified database from available exchange CSV files."""
    nse_companies = read_exchange_csv(nse_file, "NSE")
    bse_companies = read_exchange_csv(bse_file, "BSE")

    if not nse_companies and not bse_companies:
        raise ValueError("No valid NSE or BSE company records found.")

    companies = merge_companies(nse_companies, bse_companies)
    save_master_database(companies)

    return {
        "total": len(companies),
        "nse": sum(c["exchange"] == "NSE" for c in companies),
        "bse": sum(c["exchange"] == "BSE" for c in companies),
        "file": str(MASTER_FILE)
    }


if __name__ == "__main__":
    result = build_master_database()
    print("Master database created successfully.")
    print("Total companies:", result["total"])
    print("NSE companies:", result["nse"])
    print("BSE companies:", result["bse"])
    print("Saved to:", result["file"])
