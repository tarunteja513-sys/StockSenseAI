import json

with open("data/company_database.json", encoding="utf-8") as file:
    companies = json.load(file)

required_fields = [
    "company", "symbol", "exchange", "sector",
    "price", "volume", "isin", "listing_date",
    "status", "segment"
]

symbols = []

for company in companies:
    missing = [field for field in required_fields if field not in company]

    if missing:
        print(company.get("company"), "Missing:", missing)
    else:
        print(company["symbol"], "- All fields present")

    symbols.append(company["symbol"])

if len(symbols) == len(set(symbols)):
    print("\nNo duplicate stock symbols found.")
else:
    print("\nDuplicate stock symbols found.")

print("Validation completed.")
