from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

DATA_DIR = BASE_DIR / "data"

INPUT_DIR = DATA_DIR / "input"
MASTER_DIR = DATA_DIR / "master"
TEMPLATE_DIR = DATA_DIR / "templates"
OUTPUT_DIR = DATA_DIR / "output"
SHARED_DIR = DATA_DIR / "shared"
LOG_DIR = DATA_DIR / "logs"
