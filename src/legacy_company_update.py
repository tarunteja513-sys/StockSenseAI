
from company_database import CompanyDatabase

database = CompanyDatabase()

database.update_company(
    "INFY",
    {
        "sector": "Information Technology",
        "status": "ACTIVE"
    }
)

print("\nUpdated Company Information:")

results = database.search_company("INFY")

for company in results:
    print(company)
