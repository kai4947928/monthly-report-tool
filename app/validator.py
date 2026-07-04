import pandas as pd
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
        "store_master_20260524.csv",
        "area_master_20260524.csv",
        "cost_master_20260529.csv",
        "tax_rate_master_20260529.csv",
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
