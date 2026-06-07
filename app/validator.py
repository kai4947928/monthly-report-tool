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
