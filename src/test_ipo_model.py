
from stock_model import Stock

ipo_company = Stock(
    company="Example Technologies Limited",
    symbol="EXAMPLE",
    exchange="NSE",
    sector="Technology",
    price=0.0,
    volume=0,
    isin="",
    listing_date="2026-11-19",
    status="NEWLY_LISTED",
    segment="SME"
)

print("IPO COMPANY INFORMATION")
print("=======================")

ipo_company.display()
