from app.config import TEMPLATE_DIR, OUTPUT_DIR, INPUT_DIR
from app.csv_loader import load_monthly_sales_csv
from app.master_loader import (
    load_tax_rate_master,
    load_cost_master,
    load_store_master,
    load_area_master
)

from app.aggregator import (
    aggregate_overall_data,
    aggregate_store_data,
    aggregate_area_data
)

from app.report_writer import (
    write_overall_report,
    write_store_report,
    write_area_report
)

from app.validator import (
    validate_required_columns,
    validate_target_month,
    validate_store_count,
    validate_store_codes,
    validate_csv_count,
    validate_business_date_complete,
    validate_area_codes,
    validate_area_count,
    validate_null_check,
    validate_numeric_check,
    validate_duplicate_data_check
)

from app.validation_rules import (
    MONTHLY_SALES_REQUIRED_COLUMNS,
    STORE_MASTER_REQUIRED_COLUMNS,
    COST_MASTER_REQUIRED_COLUMNS,
    TAX_RATE_MASTER_REQUIRED_COLUMNS
)

def main():
    target_month = "202606"

    input_dir = INPUT_DIR / target_month

    csv_files = list(input_dir.glob("*.csv"))

    monthly_sales_df = load_monthly_sales_csv(target_month)
    tax_rate_master_df = load_tax_rate_master()
    cost_master_df = load_cost_master()
    store_master_df = load_store_master()
    area_master_df = load_area_master()

    # =====================
    # バリデーション
    # =====================

    validate_required_columns(monthly_sales_df, MONTHLY_SALES_REQUIRED_COLUMNS)

    validate_required_columns(store_master_df, STORE_MASTER_REQUIRED_COLUMNS)

    validate_required_columns(cost_master_df, COST_MASTER_REQUIRED_COLUMNS)

    validate_required_columns(tax_rate_master_df, TAX_RATE_MASTER_REQUIRED_COLUMNS)

    template_path = (TEMPLATE_DIR / "monthly_report_format_20260529.xlsx")

    validate_target_month(monthly_sales_df, target_month)

    validate_store_count(monthly_sales_df, store_master_df)

    validate_store_codes(monthly_sales_df, store_master_df)

    validate_csv_count(csv_files, store_master_df)

    validate_business_date_complete(monthly_sales_df, target_month)

    validate_area_codes(store_master_df, area_master_df)

    validate_area_count(area_master_df, store_master_df)

    validate_null_check(monthly_sales_df)

    validate_numeric_check(monthly_sales_df)

    validate_duplicate_data_check(monthly_sales_df)

    # =====================
    # 全体報告書
    # =====================

    overall_result = aggregate_overall_data(monthly_sales_df, tax_rate_master_df, cost_master_df)

    overall_output_dir = (OUTPUT_DIR / target_month / "all")

    overall_output_dir.mkdir(parents=True, exist_ok=True)

    overall_output_path = (overall_output_dir / f"{target_month}_全体月次報告書.xlsx")

    write_overall_report(overall_result, target_month, template_path, overall_output_path)

    # =====================
    # 店舗報告書
    # =====================

    grouped = monthly_sales_df.groupby("store_code")

    for store_code, store_df in grouped:
        result = aggregate_store_data(store_df, tax_rate_master_df, cost_master_df)

        store_info = store_master_df.loc[store_master_df["store_code"] == store_code]

        store_name = store_info["store_name"].iloc[0]

        store_output_dir = (OUTPUT_DIR / target_month / "stores" / f"{store_code}_{store_name}")

        store_output_dir.mkdir(parents=True, exist_ok=True)

        output_path = (store_output_dir / f"{target_month}_{store_code}_{store_name}_月次報告書.xlsx")

        write_store_report(result, target_month, store_code, store_name, template_path, output_path)

    # =====================
    # エリア報告書
    # =====================

    sales_with_store_df = monthly_sales_df.merge(store_master_df, on="store_code", how="left")

    grouped = sales_with_store_df.groupby("area_code")

    for area_code, area_df in grouped:
        result = aggregate_area_data(area_df, tax_rate_master_df, cost_master_df)

        area_name = area_df["area_name"].iloc[0]

        area_output_dir = (OUTPUT_DIR / target_month / "areas" / f"{area_name}エリア_{target_month}_月次報告書")

        area_output_dir.mkdir(parents=True, exist_ok=True)

        output_path = (area_output_dir / f"{area_name}エリア_{target_month}_月次報告書.xlsx")

        write_area_report(result, target_month, area_code, area_name, template_path, output_path)

    print(f"{target_month}の月次報告書作成が正常に完了しました。")

if __name__ == "__main__":
    main()
