
def validate_stock_data(data):

    required_fields = [
        "company",
        "symbol",
        "exchange",
        "sector"
    ]

    # Check whether data is a dictionary
    if not isinstance(data, dict):
        return False, "Invalid data format"

    # Check required fields
    for field in required_fields:
        if field not in data:
            return False, f"Missing field: {field}"

        if not isinstance(data[field], str) or not data[field].strip():
            return False, f"Invalid field: {field}"

    return True, "Stock data is valid"
