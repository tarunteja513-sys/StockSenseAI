from src.stock_model import Stock
from src.stock_manager import StockManager


def create_stock():
    return Stock(
        company="Reliance Industries",
        symbol="RELIANCE",
        exchange="NSE",
        sector="Energy"
    )


def test_add_stock():
    manager = StockManager()
    stock = create_stock()

    manager.add_stock(stock)

    assert len(manager.stocks) == 1
    assert manager.stocks[0] == stock


def test_search_stock():
    manager = StockManager()
    stock = create_stock()
    manager.add_stock(stock)

    result = manager.search_stock("RELIANCE")

    assert result == stock


def test_search_stock_case_insensitive():
    manager = StockManager()
    manager.add_stock(create_stock())

    result = manager.search_stock("reliance")

    assert result is not None
    assert result.symbol == "RELIANCE"


def test_search_missing_stock():
    manager = StockManager()

    result = manager.search_stock("INFY")

    assert result is None


def test_display_empty_stocks(capsys):
    manager = StockManager()

    manager.display_all_stocks()

    captured = capsys.readouterr()

    assert "No stocks available" in captured.out


def test_display_all_stocks(capsys):
    manager = StockManager()
    manager.add_stock(create_stock())

    manager.display_all_stocks()

    captured = capsys.readouterr()

    assert "STOCK DATABASE" in captured.out
    assert "RELIANCE" in captured.out