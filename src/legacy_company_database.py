
from company_database import CompanyDatabase
from stock_model import Stock

database = CompanyDatabase()

companies = [
    Stock(
        "Reliance Industries",
        "RELIANCE",
        "NSE",
        "Energy",
        1450.50
    ),
    Stock(
        "Tata Consultancy Services",
        "TCS",
        "NSE",
        "IT",
        3200.00
    ),
    Stock(
        "Infosys",
        "INFY",
        "NSE",
        "IT",
        1500.00
    ),
    Stock(
        "HDFC Bank",
        "HDFCBANK",
        "NSE",
        "Banking",
        1700.00
    )
]

for stock in companies:
    database.add_company(stock.to_dict())

database.display_all()

print("\nSEARCHING FOR INFOSYS")

results = database.search_company("INFY")

for result in results:
    print(result)
