from src.database.company_database import (
    load_companies,
    search_company,
    get_all_companies,
    add_company,
)


def test_load_companies():
    companies = load_companies()
    assert isinstance(companies, list)
    assert len(companies) > 0


def test_get_all_companies():
    companies = get_all_companies()
    assert len(companies) == 4


def test_search_existing_company():
    results = search_company("TCS")
    assert len(results) == 1
    assert results[0]["company"] == "Tata Consultancy Services"


def test_search_company_name():
    results = search_company("Infosys")
    assert len(results) == 1


def test_search_invalid_company():
    assert search_company("INVALID") == []


def test_search_case_insensitive():
    results = search_company("tcs")
    assert len(results) == 1


def test_add_duplicate_company():
    company = {
        "company": "Tata Consultancy Services",
        "symbol": "TCS",
        "exchange": "NSE",
        "sector": "IT"
    }

    assert add_company(company) is False
