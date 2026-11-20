


import csv
from unittest.mock import Mock

from src import nse_importer


def test_successful_download(tmp_path, monkeypatch):
    importer = nse_importer.NSEImporter()
    importer.output_file = str(tmp_path / "nse_companies.csv")

    csv_data = (
        "SYMBOL,NAME OF COMPANY, SERIES\n"
        "RELIANCE,Reliance Industries,EQ\n"
        "INFY,Infosys Limited,EQ\n"
    )

    response = Mock()
    response.content = csv_data.encode("utf-8-sig")

    monkeypatch.setattr(
        nse_importer.requests,
        "get",
        lambda *args, **kwargs: response
    )

    result = importer.download_company_list()

    assert len(result) == 2
    assert result[0]["SYMBOL"] == "RELIANCE"
    assert result[1]["SYMBOL"] == "INFY"

    with open(importer.output_file, encoding="utf-8") as file:
        saved_data = list(csv.DictReader(file))

    assert len(saved_data) == 2


def test_empty_response(tmp_path, monkeypatch):
    importer = nse_importer.NSEImporter()
    importer.output_file = str(tmp_path / "empty.csv")

    response = Mock()
    response.content = b""

    monkeypatch.setattr(
        nse_importer.requests,
        "get",
        lambda *args, **kwargs: response
    )

    result = importer.download_company_list()

    assert result == []


def test_invalid_csv_columns(tmp_path, monkeypatch):
    importer = nse_importer.NSEImporter()
    importer.output_file = str(tmp_path / "invalid.csv")

    response = Mock()
    response.content = b"CODE,COMPANY\nABC,Example Ltd\n"

    monkeypatch.setattr(
        nse_importer.requests,
        "get",
        lambda *args, **kwargs: response
    )

    result = importer.download_company_list()

    assert result == []


def test_no_company_records(tmp_path, monkeypatch):
    importer = nse_importer.NSEImporter()
    importer.output_file = str(tmp_path / "no_records.csv")

    response = Mock()
    response.content = b"SYMBOL,NAME OF COMPANY\n"

    monkeypatch.setattr(
        nse_importer.requests,
        "get",
        lambda *args, **kwargs: response
    )

    result = importer.download_company_list()

    assert result == []
