from app.csv_loader import load_monthly_sales_csv
from app.master_loader import load_tax_rate_master, load_cost_master
from app.aggregator import aggregate_store_data


def main():
    target_month = "202606"

    monthly_sales_df = load_monthly_sales_csv(target_month)
    tax_rate_master_df = load_tax_rate_master()
    cost_master_df = load_cost_master()

    grouped = monthly_sales_df.groupby("store_code")

    for store_code, store_df in grouped:
        result = aggregate_store_data(store_df, tax_rate_master_df, cost_master_df)

        print(f"店舗コード: {store_code}")
        print(result)
        print("_" * 30)

if __name__ == "__main__":
    main()
