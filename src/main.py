
import csv
import os

from config import DATA_DIR

DATA_FILE = os.path.join(DATA_DIR, "nse_companies.csv")


def analyze_database():

    # Check whether NSE database exists
    if not os.path.exists(DATA_FILE):
        print("NSE database not found:", DATA_FILE)
        print("Please download the NSE company list first.")
        return

    try:
        with open(DATA_FILE, "r", encoding="utf-8-sig") as file:
            reader = csv.DictReader(file)

            required_columns = {
                "SYMBOL",
                "NAME OF COMPANY",
                " SERIES"
            }

            if not reader.fieldnames or not required_columns.issubset(
                set(reader.fieldnames)
            ):
                print("Invalid NSE CSV format.")
                return

            companies = list(reader)

    except (OSError, UnicodeError, csv.Error) as error:
        print("Unable to read NSE database:", error)
        return

    # Extract stock symbols
    symbols = [
        row.get("SYMBOL", "").strip().upper()
        for row in companies
    ]

    # Separate equity and trade-to-trade companies
    equity = [
        row for row in companies
        if row.get(" SERIES", "").strip() == "EQ"
    ]

    trade_to_trade = [
        row for row in companies
        if row.get(" SERIES", "").strip() == "BE"
    ]

    # Calculate database statistics
    duplicates = len(symbols) - len(set(symbols))

    missing = sum(
        1 for row in companies
        if not row.get("SYMBOL", "").strip()
        or not row.get("NAME OF COMPANY", "").strip()
    )

    # Display report
    print("\n===== STOCKSENSE AI =====")
    print("NSE DATABASE ANALYZER")
    print("-------------------------")
    print("Total companies:", len(companies))
    print("EQ companies:", len(equity))
    print("BE companies:", len(trade_to_trade))
    print("Other series:", len(companies) - len(equity) - len(trade_to_trade))
    print("Duplicate symbols:", duplicates)
    print("Missing information:", missing)
    print("-------------------------")


if __name__ == "__main__":
    analyze_database()
