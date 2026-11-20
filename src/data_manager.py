
import os
import json
from config import DATA_DIR

# Create data folders
RAW_DATA_DIR = os.path.join(DATA_DIR, "raw")
PROCESSED_DATA_DIR = os.path.join(DATA_DIR, "processed")

os.makedirs(RAW_DATA_DIR, exist_ok=True)
os.makedirs(PROCESSED_DATA_DIR, exist_ok=True)


def save_data(filename, data):
    file_path = os.path.join(RAW_DATA_DIR, filename)

    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)

    print("Data saved successfully:", filename)


def load_data(filename):
    file_path = os.path.join(RAW_DATA_DIR, filename)

    if not os.path.exists(file_path):
        print("File not found:", filename)
        return None

    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)
