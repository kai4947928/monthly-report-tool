from app.config import TEMPLATE_DIR, OUTPUT_DIR
from app.csv_loader import load_monthly_sales_csv
from app.master_loader import load_tax_rate_master, load_cost_master
from app.aggregator import aggregate_overall_data
from app.report_writer import write_overall_report


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

    template_path = TEMPLATE_DIR / "monthly_report_format_20260529.xlsx"

    output_dir = OUTPUT_DIR / target_month / "all"
    output_dir.mkdir(parents=True, exist_ok=True)

    output_path = output_dir / f"{target_month}_全体月次報告書.xlsx"

    write_overall_report(
        result,
        target_month,
        template_path,
        output_path,
    )


if __name__ == "__main__":
    main()