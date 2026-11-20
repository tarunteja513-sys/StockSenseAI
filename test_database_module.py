from src.database.company_database import (
    load_companies,
    search_company,
    get_all_companies
)

print("===== STOCKSENSE AI DATABASE TEST =====")

# Test 1: Load companies
companies = load_companies()
print("\n1. Total companies:", len(companies))

# Test 2: Get all companies
print("\n2. Available companies:")
for company in get_all_companies():
    print(company["symbol"], "-", company["company"])

# Test 3: Search existing company
print("\n3. Search TCS:")
print(search_company("TCS"))

# Test 4: Search unavailable company
print("\n4. Search invalid symbol:")
print(search_company("INVALID"))

print("\n===== ALL TESTS COMPLETED =====")
