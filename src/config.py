
import os

# Project information
APP_NAME = "StockSense AI"
VERSION = "1.0.0"
ENVIRONMENT = "Development"

# Project directories
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
MODEL_DIR = os.path.join(BASE_DIR, "models")
LOG_DIR = os.path.join(BASE_DIR, "logs")

# Application settings
DEFAULT_LANGUAGE = "English"
SUPPORTED_LANGUAGES = [
    "English",
    "Hindi",
    "Telugu",
    "Tamil",
    "Kannada",
    "Malayalam"
]

# Create required directories
for directory in [DATA_DIR, MODEL_DIR, LOG_DIR]:
    os.makedirs(directory, exist_ok=True)
