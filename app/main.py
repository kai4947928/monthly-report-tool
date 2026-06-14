from app.config import TEMPLATE_DIR, OUTPUT_DIR
from app.csv_loader import load_monthly_sales_csv
from app.master_loader import load_tax_rate_master, load_cost_master, load_store_master
from app.aggregator import aggregate_overall_data, aggregate_store_data
from app.report_writer import write_overall_report, write_store_report


def main():
    target_month = "202606"

    monthly_sales_df = load_monthly_sales_csv(target_month)
    tax_rate_master_df = load_tax_rate_master()
    cost_master_df = load_cost_master()
    store_master_df = load_store_master()

    template_path = (
        TEMPLATE_DIR
        / "monthly_report_format_20260529.xlsx"
    )

    # =====================
    # 全体報告書
    # =====================

    overall_result = aggregate_overall_data(
        monthly_sales_df,
        tax_rate_master_df,
        cost_master_df,
    )

    overall_output_dir = (
        OUTPUT_DIR
        / target_month
        / "all"
    )

    overall_output_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    overall_output_path = (
        overall_output_dir
        / f"{target_month}_全体月次報告書.xlsx"
    )

    write_overall_report(
        overall_result,
        target_month,
        template_path,
        overall_output_path,
    )

    # =====================
    # 店舗報告書
    # =====================

    grouped = monthly_sales_df.groupby("store_code")

    for store_code, store_df in grouped:

        result = aggregate_store_data(
            store_df,
            tax_rate_master_df,
            cost_master_df,
        )

        store_info = store_master_df.loc[
            store_master_df["store_code"] == store_code
        ]

        store_name = (
            store_info["store_name"]
            .iloc[0]
        )

        store_output_dir = (
            OUTPUT_DIR / target_month / "stores" / f"{store_code}_{store_name}"
        )

        store_output_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

        output_path = (
            store_output_dir / f"{target_month}_{store_code}_{store_name}_月次報告書.xlsx"
        )

        write_store_report(
            result,
            target_month,
            store_code,
            store_name,
            template_path,
            output_path,
        )

        print(store_code)
        print(type(store_code))

if __name__ == "__main__":
    main()