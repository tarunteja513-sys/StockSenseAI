from src.stock_model import Stock


def test_stock_creation():
    stock = Stock(
        "Reliance Industries",
        "RELIANCE",
        "NSE",
        "Energy",
        1450.50,
        100000
    )

    assert stock.company == "Reliance Industries"
    assert stock.symbol == "RELIANCE"
    assert stock.exchange == "NSE"
    assert stock.price == 1450.50
    assert stock.volume == 100000


def test_stock_to_dict():
    stock = Stock(
        "Infosys",
        "INFY",
        "NSE",
        "IT",
        1500.00
    )

    data = stock.to_dict()

    assert data["symbol"] == "INFY"
    assert data["company"] == "Infosys"
    assert data["price"] == 1500.00


def test_stock_default_values():
    stock = Stock(
        "TCS",
        "TCS",
        "NSE",
        "IT"
    )

    assert stock.price == 0.0
    assert stock.volume == 0
    assert stock.status == "ACTIVE"
    assert stock.segment == "MAIN"
