from app.config import INPUT_DIR
from app.csv_loader import load_csv

csv_path = INPUT_DIR / "sales_001_202606_20260524_091533.csv"

df = load_csv(csv_path)

print(df.head())
