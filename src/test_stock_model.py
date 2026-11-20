
from src.stock_model import Stock

stock = Stock(
    "Reliance Industries",
    "RELIANCE",
    "NSE",
    "Energy",
    1450.50,
    100000
)

stock.display()

print("\nDictionary Format:")
print(stock.to_dict())
