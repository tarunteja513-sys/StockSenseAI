import json
from src import data_manager


def test_save_data(tmp_path, monkeypatch):
    raw_folder = tmp_path / "raw"
    raw_folder.mkdir()

    monkeypatch.setattr(data_manager, "RAW_DATA_DIR", str(raw_folder))

    sample = {
        "symbol": "RELIANCE",
        "price": 1500
    }

    data_manager.save_data("test.json", sample)

    file_path = raw_folder / "test.json"

    assert file_path.exists()

    with open(file_path, "r", encoding="utf-8") as file:
        saved_data = json.load(file)

    assert saved_data == sample


def test_load_data(tmp_path, monkeypatch):
    raw_folder = tmp_path / "raw"
    raw_folder.mkdir()

    monkeypatch.setattr(data_manager, "RAW_DATA_DIR", str(raw_folder))

    sample = {"symbol": "INFY", "price": 1800}

    file_path = raw_folder / "test.json"
    file_path.write_text(json.dumps(sample), encoding="utf-8")

    result = data_manager.load_data("test.json")

    assert result == sample


def test_load_missing_file(tmp_path, monkeypatch):
    raw_folder = tmp_path / "raw"
    raw_folder.mkdir()

    monkeypatch.setattr(data_manager, "RAW_DATA_DIR", str(raw_folder))

    result = data_manager.load_data("missing.json")

    assert result is None