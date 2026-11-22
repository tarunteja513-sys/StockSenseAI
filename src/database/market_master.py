import csv
import json
import re
from pathlib import Path

from src.config import DATA_DIR


DATA_PATH = Path(DATA_DIR)
NSE_FILE = DATA_PATH / "nse_companies.csv"
BSE_FILE = DATA_PATH / "bse_companies.csv"
MASTER_FILE = DATA_PATH / "master_company_database.json"
BSE_EQUITY_GROUPS_FILE = DATA_PATH / "bse_equity_groups.json"

# Checks the basic 12-character ISIN format.
ISIN_PATTERN = re.compile(r"^[A-Z]{2}[A-Z0-9]{9}[0-9]$")


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


def is_valid_isin(isin):
    """Check the basic format of an ISIN."""
    isin = (isin or "").strip().upper()
    return bool(ISIN_PATTERN.fullmatch(isin))


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
                security_type = ""

                isin = first_value(
                    row, "ISIN NUMBER", "ISIN NO", "ISIN"
                )
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
                security_type = first_value(row, "SCTYTPFLG")

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
                "sector": first_value(
                    row, "INDUSTRY", "SECTOR"
                ) or "UNKNOWN",
                "series": series or "UNKNOWN",
                "isin": isin,
                "listing_date": listing_date,
                "face_value": face_value,
                "paid_up_value": first_value(row, "PAID UP VALUE"),
                "market_lot": market_lot,
                "security_code": security_code,
                "security_type": security_type,
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


def group_bse_equities(companies):
    """
    Group BSE equity records by valid ISIN.

    Records without a valid ISIN remain separate and use their
    security code as the unique grouping key.
    """
    groups = {}

    for company in companies:
        if company.get("exchange") != "BSE":
            continue

        if company.get("security_type", "").strip().upper() != "EQ":
            continue

        isin = (company.get("isin") or "").strip().upper()
        security_code = (company.get("security_code") or "").strip()
        symbol = (company.get("symbol") or "").strip()

        if is_valid_isin(isin):
            group_key = ("ISIN", isin)
            group_id = f"ISIN:{isin}"
            group_isin = isin
        else:
            # Do not combine records with missing or invalid ISINs.
            unique_code = security_code or symbol

            group_key = ("SECURITY_CODE", unique_code)
            group_id = f"NO_ISIN:{unique_code}"
            group_isin = ""

        if group_key not in groups:
            groups[group_key] = {
                "group_id": group_id,
                "isin": group_isin,
                "records": []
            }

        groups[group_key]["records"].append(company)

    return sorted(
        groups.values(),
        key=lambda group: group["group_id"]
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


def save_json_safely(file_path, data):
    """Save JSON data safely using a temporary file."""
    file_path = Path(file_path)
    file_path.parent.mkdir(parents=True, exist_ok=True)

    temporary_file = file_path.with_suffix(".tmp")

    try:
        with temporary_file.open("w", encoding="utf-8") as file:
            json.dump(data, file, indent=4, ensure_ascii=False)

        temporary_file.replace(file_path)

    finally:
        if temporary_file.exists():
            temporary_file.unlink()


def save_master_database(companies):
    """Save the complete exchange master."""
    if not isinstance(companies, list):
        raise TypeError("Companies must be a list.")

    save_json_safely(MASTER_FILE, companies)


def save_bse_equity_groups(groups):
    """Save the separate BSE equity grouping database."""
    if not isinstance(groups, list):
        raise TypeError("Groups must be a list.")

    save_json_safely(BSE_EQUITY_GROUPS_FILE, groups)


def build_master_database(
    nse_file=NSE_FILE,
    bse_file=BSE_FILE
):
    """Build the complete master and separate BSE equity groups."""
    nse_companies = read_exchange_csv(nse_file, "NSE")
    bse_companies = read_exchange_csv(bse_file, "BSE")

    if not nse_companies and not bse_companies:
        raise ValueError("No valid NSE or BSE company records found.")

    companies = merge_companies(nse_companies, bse_companies)

    bse_equity_records = [
        company for company in companies
        if company["exchange"] == "BSE"
        and company.get("security_type", "").upper() == "EQ"
    ]

    bse_equity_groups = group_bse_equities(companies)

    save_master_database(companies)
    save_bse_equity_groups(bse_equity_groups)

    valid_isin_groups = sum(
        bool(group["isin"]) for group in bse_equity_groups
    )

    return {
        "total": len(companies),
        "nse": sum(
            company["exchange"] == "NSE" for company in companies
        ),
        "bse": sum(
            company["exchange"] == "BSE" for company in companies
        ),
        "bse_equity_records": len(bse_equity_records),
        "bse_equity_groups": len(bse_equity_groups),
        "bse_valid_isin_groups": valid_isin_groups,
        "bse_missing_isin_groups": (
            len(bse_equity_groups) - valid_isin_groups
        ),
        "file": str(MASTER_FILE),
        "equity_groups_file": str(BSE_EQUITY_GROUPS_FILE)
    }


if __name__ == "__main__":
    result = build_master_database()

    print("Master database created successfully.")
    print("Total exchange records:", result["total"])
    print("NSE records:", result["nse"])
    print("BSE records:", result["bse"])
    print("BSE equity records:", result["bse_equity_records"])
    print("BSE equity groups:", result["bse_equity_groups"])
    print("Valid ISIN groups:", result["bse_valid_isin_groups"])
    print("Missing/invalid ISIN groups:", result["bse_missing_isin_groups"])
    print("Master database:", result["file"])
    print("Equity groups:", result["equity_groups_file"])
