
from data_manager import save_data, load_data

sample_stock = {
    "company": "Reliance Industries",
    "symbol": "RELIANCE",
    "exchange": "NSE",
    "sector": "Energy"
}

save_data("sample_stock.json", sample_stock)

loaded_data = load_data("sample_stock.json")

print("\nRetrieved Stock Information:")
print(loaded_data)
