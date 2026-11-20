from src.data_validator import validate_stock_data


def test_valid_stock_data():
    data = {
        "company": "Reliance Industries",
        "symbol": "RELIANCE",
        "exchange": "NSE",
        "sector": "Energy"
    }

    result = validate_stock_data(data)

    assert result == (True, "Stock data is valid")


def test_invalid_data_format():
    result = validate_stock_data("RELIANCE")

    assert result == (False, "Invalid data format")


def test_missing_field():
    data = {
        "company": "Infosys",
        "symbol": "INFY",
        "exchange": "NSE"
    }

    result = validate_stock_data(data)

    assert result == (False, "Missing field: sector")


def test_invalid_field_type():
    data = {
        "company": "Infosys",
        "symbol": 123,
        "exchange": "NSE",
        "sector": "IT"
    }

    result = validate_stock_data(data)

    assert result == (False, "Invalid field: symbol")


def test_empty_field():
    data = {
        "company": "Infosys",
        "symbol": "INFY",
        "exchange": "NSE",
        "sector": " "
    }

    result = validate_stock_data(data)

    assert result == (False, "Invalid field: sector")