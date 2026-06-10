from app.csv_loader import load_monthly_sales_csv
from app.master_loader import load_store_master, load_tax_rate_master, load_cost_master
from app.aggregator import aggregate_area_data


def main():
    target_month = "202606"

    monthly_sales_df = load_monthly_sales_csv(target_month)
    store_master_df = load_store_master()
    tax_rate_master_df = load_tax_rate_master()
    cost_master_df = load_cost_master()

    sales_with_store_df = monthly_sales_df.merge(
        store_master_df,
        on="store_code",
        how="left",
    )

    grouped = sales_with_store_df.groupby("area_code")

    for area_code, area_df in grouped:
        result = aggregate_area_data(
            area_df,
            tax_rate_master_df,
            cost_master_df,
        )

        print(f"エリアコード: {area_code}")
        print(result)
        print("_" * 30)

if __name__ == "__main__":
    main()
