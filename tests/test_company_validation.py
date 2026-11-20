from src.database.company_database import get_all_companies


def test_all_companies_have_required_fields():
    required_fields = [
        "company", "symbol", "exchange", "sector",
        "price", "volume", "isin", "listing_date",
        "status", "segment"
    ]

    companies = get_all_companies()

    assert len(companies) > 0

    for company in companies:
        for field in required_fields:
            assert field in company, (
                f"{company.get('company')} is missing {field}"
            )


def test_no_duplicate_exchange_symbols():
    companies = get_all_companies()

    identifiers = [
        (
            company["exchange"].upper(),
            company["symbol"].upper()
        )
        for company in companies
    ]

    assert len(identifiers) == len(set(identifiers))
