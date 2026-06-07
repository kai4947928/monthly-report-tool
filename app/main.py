from app.csv_loader import load_monthly_sales_csv


def main():
    target_month = "202606"

    monthly_sales_df = load_monthly_sales_csv(target_month)

    print(monthly_sales_df.head())
    print(monthly_sales_df.shape)


if __name__ == "__main__":
    main()
