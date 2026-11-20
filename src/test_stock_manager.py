
from stock_model import Stock
from stock_manager import StockManager

manager = StockManager()

manager.add_stock(
    Stock("Reliance Industries", "RELIANCE", "NSE", "Energy", 1450.50)
)

manager.add_stock(
    Stock("Tata Consultancy Services", "TCS", "NSE", "IT", 3200.00)
)

manager.add_stock(
    Stock("Infosys", "INFY", "NSE", "IT", 1500.00)
)

manager.add_stock(
    Stock("HDFC Bank", "HDFCBANK", "NSE", "Banking", 1700.00)
)

manager.display_all_stocks()

result = manager.search_stock("INFY")

if result:
    print("\nSearch Result:")
    result.display()
else:
    print("Stock not found")
