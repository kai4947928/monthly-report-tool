from app.config import INPUT_DIR, MASTER_DIR
from app.csv_loader import load_csv
from app.aggregator import aggregate_store_data


target_month = "202606"
csv_path = INPUT_DIR / target_month / "sales_001_202606_20260524_091533.csv"
csv_tax_rate_master_path = MASTER_DIR / "tax_rate_master_20260529.csv"
cost_master_path = MASTER_DIR / "cost_master_20260529.csv"

sales_df = load_csv(csv_path)
tax_rate_master_df = load_csv(csv_tax_rate_master_path)
cost_master_df = load_csv(cost_master_path)

result = aggregate_store_data(sales_df, tax_rate_master_df, cost_master_df)

print(result)

