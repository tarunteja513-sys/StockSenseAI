
class Stock:

    def __init__(
        self,
        company,
        symbol,
        exchange,
        sector,
        price=0.0,
        volume=0,
        isin="",
        listing_date="",
        status="ACTIVE",
        segment="MAIN"
    ):

        self.company = company
        self.symbol = symbol
        self.exchange = exchange
        self.sector = sector
        self.price = price
        self.volume = volume

        # Additional listing information
        self.isin = isin
        self.listing_date = listing_date
        self.status = status
        self.segment = segment

    def display(self):

        print("Company:", self.company)
        print("Symbol:", self.symbol)
        print("Exchange:", self.exchange)
        print("Sector:", self.sector)
        print("Price:", self.price)
        print("Volume:", self.volume)
        print("ISIN:", self.isin)
        print("Listing Date:", self.listing_date)
        print("Status:", self.status)
        print("Segment:", self.segment)

    def to_dict(self):

        return {
            "company": self.company,
            "symbol": self.symbol,
            "exchange": self.exchange,
            "sector": self.sector,
            "price": self.price,
            "volume": self.volume,
            "isin": self.isin,
            "listing_date": self.listing_date,
            "status": self.status,
            "segment": self.segment
        }
