import pandas as pd
import openpyxl
from app.config import INPUT_DIR, MASTER_DIR

def validate_input_files(target_month):
    input_dir = INPUT_DIR / target_month
    csv_files = list(input_dir.glob("*.csv"))

    if not input_dir.exists():
        raise FileNotFoundError(f"入力フォルダが存在しません: {input_dir}")

    if not csv_files:
        raise FileNotFoundError(f"CSVファイルが存在しません: {input_dir}")

    return csv_files

def validate_master_files():
    required_files = [
        "store_master.csv",
        "area_master.csv",
        "cost_master.csv",
        "tax_rate_master.csv",
    ]

    for file_name in required_files:
        file_path = MASTER_DIR / file_name

        if not file_path.exists():
            raise FileNotFoundError(f"マスタファイルが存在しません: {file_path}")

    return True

def validate_required_columns(df, required_columns):
    missing_columns = (
        required_columns - set(df.columns)
    )

    if missing_columns:
        raise ValueError(
            f"必須カラム不足: {missing_columns}"
        )

def validate_target_month(df, target_month):
    business_dates = pd.to_datetime(df["business_date"])

    actual_months = business_dates.dt.strftime("%Y%m").unique()

    if actual_months[0] != target_month or len(actual_months) != 1:
        raise ValueError(
            f"対象月不一致: target_month={target_month}, actual_months={actual_months}"
        )

def validate_store_count(monthly_sales_df, store_master_df):
    sales_store_count = len(monthly_sales_df["store_code"].unique())

    active_store_df = store_master_df[store_master_df["is_active"] == True]

    master_store_count = len(active_store_df)

    if sales_store_count != master_store_count:
        raise ValueError(
            f"店舗数不一致: sales_store_count={sales_store_count}, master_store_count{master_store_count}"
        )

def validate_store_codes(monthly_sales_df, store_master_df):
    sales_store_codes = (
        monthly_sales_df["store_code"].unique()
    )

    active_store_df = store_master_df[
        store_master_df["is_active"] == True
    ]

    active_store_codes = (
        active_store_df["store_code"].unique()
    )

    invalid_store_codes = []

    for code in sales_store_codes:
        if code not in active_store_codes:
            invalid_store_codes.append(code)

    if invalid_store_codes:
        raise ValueError(
            f"存在しない店舗コードがあります: {invalid_store_codes}"
        )

def validate_csv_count(csv_files, store_master_df):
    active_store_df = store_master_df[
        store_master_df["is_active"] == True
    ]

    master_store_count = len(active_store_df)

    csv_count = len(csv_files)

    if csv_count != master_store_count:
        raise ValueError(
            f"CSVファイル数不一致: "
            f"csv_count={csv_count},"
            f"master_store_count={master_store_count}"
        )

def validate_business_date_complete(monthly_sales_df, target_month):
    start_date = pd.to_datetime(target_month + "01")
    end_date = start_date + pd.offsets.MonthEnd(0)
    expected_dates = set(pd.date_range(start=start_date, end=end_date))

    validation_errors = []

    for store_code, store_df in monthly_sales_df.groupby("store_code"):
        actual_dates = set(
            pd.to_datetime(store_df["business_date"])
        )

        missing_dates = expected_dates - actual_dates
        if missing_dates:
            validation_errors.append(
                {
                    "store_code": store_code,
                    "missing_dates": sorted(missing_dates)
                }
            )

    if validation_errors:
        raise ValueError(
            f"日付不一致: {validation_errors}"
        )

def validate_area_codes(store_master_df, area_master_df):
    csv_area_codes = set(store_master_df["area_code"])

    active_area_df = area_master_df[
        area_master_df["is_active"] == True
    ]
    master_area_codes = set(active_area_df["area_code"])

    invalid_area_codes = csv_area_codes - master_area_codes

    if invalid_area_codes:
        raise ValueError(
            f"エリアコード不一致: {sorted(invalid_area_codes)}"
        )

def validate_area_count(area_master_df, store_master_df):
    active_area_count = area_master_df.loc[area_master_df["is_active"] == True, "area_code"].nunique()

    used_area_count = store_master_df["area_code"].nunique()

    if active_area_count != used_area_count:
        raise ValueError(
            f"エリア数が一致しません: "
            f"有効エリア数={active_area_count}, "
            f"使用エリア数={used_area_count}"
        )

def validate_null_check(monthly_sales_df):
    required_not_null_columns = [
        "store_code",
        "business_date",
        "sales_amount_tax_ex",
        "customer_count"
    ]

    if monthly_sales_df[required_not_null_columns].isnull().any().any():
        raise ValueError(
            "必須項目にNULLが存在します"
        )

def validate_numeric_check(monthly_sales_df):
    numeric_columns = [
        "sales_amount_tax_ex",
        "customer_count"
    ]

    for column in numeric_columns:
        try:
            pd.to_numeric(
                monthly_sales_df[column],
                errors="raise"
            )
        except ValueError:
            raise ValueError(
                f"数値項目 {column} に不正な値が存在します。"
            )

def validate_duplicate_data_check(monthly_sales_df):
    if monthly_sales_df.duplicated(
        subset=["store_code", "business_date"]
    ).any():
        raise ValueError(
            "同一店舗・同一営業日の重複データが存在します。"
        )

def validate_tax_rate_period(tax_rate_master_df, target_month):
    target_date = pd.to_datetime(target_month + "01")

    tax_rate_master_df["valid_from"] = pd.to_datetime(
        tax_rate_master_df["valid_from"]
    )

    tax_rate_master_df["valid_to"] = pd.to_datetime(
        tax_rate_master_df["valid_to"]
    )

    valid_tax_rate_df = tax_rate_master_df[
        (tax_rate_master_df["valid_from"] <= target_date) & (tax_rate_master_df["valid_to"] >= target_date)
    ]

    if len(valid_tax_rate_df) != 1:
        raise ValueError(
            "対象月に適用できる税率を取得できません"
        )

def validate_cost_master_check(store_master_df, cost_master_df):
    store_codes = set(store_master_df["store_code"])
    cost_store_codes = set(cost_master_df["store_code"])

    if store_codes != cost_store_codes:
        raise ValueError(
            "店舗マスタと原価マスタの店舗コードが一致しません"
        )

def validate_report_output_cells(output_path, aggregation_result):
    workbook = openpyxl.load_workbook(output_path)
    worksheet = workbook.active

    cell_mapping = {
        "sales_amount_tax_ex": "B6",
        "tax_amount": "D6",
        "sales_amount_tax_in": "F6",
        "customer_count": "B9",
        "average_customer_spend": "D9",
        "tax_rate": "F9",
        "cost_amount": "B12",
        "labor_cost_amount": "D12",
        "rent_cost": "F12",
        "utility_cost": "B15",
        "other_expense_cost": "D15",
        "operating_cost": "F15",
        "operating_profit": "B18",
        "cost_rate": "D18",
        "labor_cost_rate": "F18",
        "operating_profit_rate": "B21",
    }

    for key, cell in cell_mapping.items():
        expected_value = aggregation_result[key]
        actual_value = worksheet[cell].value

        if round(expected_value, 2) != round(actual_value, 2):
            raise ValueError(
                f"出力セル {cell} の値が集計結果と一致しません"
            )
