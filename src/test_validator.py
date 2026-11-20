
from data_validator import validate_stock_data

stock = {
    "company": "Reliance Industries",
    "symbol": "RELIANCE",
    "exchange": "NSE",
    "sector": "Energy"
}

result, message = validate_stock_data(stock)

print("Validation Result:", result)
print("Message:", message)
