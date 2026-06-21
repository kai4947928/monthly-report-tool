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

