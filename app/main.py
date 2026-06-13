from app.csv_loader import load_monthly_sales_csv
from app.master_loader import load_store_master, load_tax_rate_master, load_cost_master
from app.aggregator import aggregate_overall_data


def main():
    target_month = "202606"

    monthly_sales_df = load_monthly_sales_csv(target_month)
    tax_rate_master_df = load_tax_rate_master()
    cost_master_df = load_cost_master()

    result = aggregate_overall_data(
        monthly_sales_df,
        tax_rate_master_df,
        cost_master_df,
    )

    print(result)


if __name__ == "__main__":
    main()
