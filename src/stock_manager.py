
from stock_model import Stock


class StockManager:

    def __init__(self):
        self.stocks = []

    def add_stock(self, stock):
        self.stocks.append(stock)
        print(stock.symbol, "added successfully")

    def display_all_stocks(self):
        if not self.stocks:
            print("No stocks available")
            return

        print("\n STOCK DATABASE")
        print("------------------------")

        for stock in self.stocks:
            stock.display()
            print("------------------------")

    def search_stock(self, symbol):
        for stock in self.stocks:
            if stock.symbol.upper() == symbol.upper():
                return stock

        return None
