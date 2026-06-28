import pandas as pd
import pytest

from app.validator import validate_required_columns, validate_target_month, validate_store_count, validate_store_codes, validate_csv_count

def test_validate_required_columns_success():

    required_columns = {
        "store_code",
        "sales_amount_tax_ex",
        "customer_count",
    }

    df = pd.DataFrame([
        {
            "store_code": "001",
            "sales_amount_tax_ex": 100000,
            "customer_count": 100,
        }
    ])

    validate_required_columns(
        df, required_columns
    )

def test_validate_required_columns_error():

    required_columns = {
        "store_code",
        "sales_amount_tax_ex",
        "customer_count",
    }

    df = pd.DataFrame([
        {
            "store_code": "001",
            "sales_amount_tax_ex": 100000,
        }
    ])

    with pytest.raises(ValueError):
        validate_required_columns(df, required_columns)

def test_validate_target_month_success():
    target_month = "202606"

    df = pd.DataFrame([
        {"business_date": "2026-06-01"},
        {"business_date": "2026-06-02"},
        {"business_date": "2026-06-03"},
        {"business_date": "2026-06-04"},
    ])

    validate_target_month(df, target_month)

def test_validate_target_month_error_mixed():
    target_month = "202606"

    df = pd.DataFrame([
        {"business_date": "2026-06-01"},
        {"business_date": "2026-07-01"},
    ])

    with pytest.raises(ValueError):
        validate_target_month(df, target_month)

def test_validate_target_month_error_wrong():
    target_month = "202606"

    df = pd.DataFrame([
        {"business_date": "2026-07-01"},
        {"business_date": "2026-07-02"},
    ])

    with pytest.raises(ValueError):
        validate_target_month(df, target_month)

def test_validate_store_count_success():
    monthly_sales_df = pd.DataFrame([
        {"store_code": "001"},
        {"store_code": "002"},
        {"store_code": "003"},
        {"store_code": "004"},
        {"store_code": "005"},
        {"store_code": "006"},
        {"store_code": "007"},
        {"store_code": "008"},
        {"store_code": "009"},
    ])

    store_master_df = pd.DataFrame([
        {"store_code": "001", "is_active": True},
        {"store_code": "002", "is_active": True},
        {"store_code": "003", "is_active": True},
        {"store_code": "004", "is_active": True},
        {"store_code": "005", "is_active": True},
        {"store_code": "006", "is_active": True},
        {"store_code": "007", "is_active": True},
        {"store_code": "008", "is_active": True},
        {"store_code": "009", "is_active": True},
    ])


    validate_store_count(monthly_sales_df, store_master_df)

def test_validate_store_count_error_more():
    monthly_sales_df = pd.DataFrame([
        {"store_code": "001"},
        {"store_code": "002"},
        {"store_code": "003"},
        {"store_code": "004"},
        {"store_code": "005"},
    ])

    store_master_df = pd.DataFrame([
        {"store_code": "001", "is_active": True},
        {"store_code": "002", "is_active": True},
        {"store_code": "003", "is_active": True},
        {"store_code": "004", "is_active": True},
    ])

    with pytest.raises(ValueError):
        validate_store_count(monthly_sales_df, store_master_df)

def test_validate_store_count_error_less():
    monthly_sales_df = pd.DataFrame([
        {"store_code": "001"},
        {"store_code": "002"},
        {"store_code": "003"},
        {"store_code": "004"},
        {"store_code": "005"},
        {"store_code": "006"},
    ])

    store_master_df = pd.DataFrame([
        {"store_code": "001", "is_active": True},
        {"store_code": "002", "is_active": True},
        {"store_code": "003", "is_active": True},
        {"store_code": "004", "is_active": True},
        {"store_code": "005", "is_active": True},
        {"store_code": "006", "is_active": True},
        {"store_code": "007", "is_active": True},
    ])

    with pytest.raises(ValueError):
        validate_store_count(monthly_sales_df, store_master_df)

def test_validate_store_codes_success():
    monthly_sales_df = pd.DataFrame([
        {"store_code": "001"},
        {"store_code": "002"},
        {"store_code": "003"},
        {"store_code": "004"},
        {"store_code": "005"},
    ])

    store_master_df = pd.DataFrame([
        {"store_code": "001", "is_active": True},
        {"store_code": "002", "is_active": True},
        {"store_code": "003", "is_active": True},
        {"store_code": "004", "is_active": True},
        {"store_code": "005", "is_active": True},
    ])

    validate_store_codes(monthly_sales_df, store_master_df)

def test_validate_store_codes_error():
    monthly_sales_df = pd.DataFrame([
        {"store_code": "001"},
        {"store_code": "002"},
        {"store_code": "003"},
        {"store_code": "004"},
        {"store_code": "005"},
        {"store_code": "999"},
    ])

    store_master_df = pd.DataFrame([
        {"store_code": "001", "is_active": True},
        {"store_code": "002", "is_active": True},
        {"store_code": "003", "is_active": True},
        {"store_code": "004", "is_active": True},
        {"store_code": "005", "is_active": True},
    ])

    with pytest.raises(ValueError):
        validate_store_codes(monthly_sales_df, store_master_df)

def test_validate_csv_count_success():
    csv_files = [
        "001.csv",
        "002.csv",
        "003.csv",
    ]

    store_master_df = pd.DataFrame([
        {"store_code": "001", "is_active": True},
        {"store_code": "002", "is_active": True},
        {"store_code": "003", "is_active": True},
    ])

    validate_csv_count(csv_files, store_master_df)

def test_validate_csv_count_error_more():
    csv_files = [
        "001.csv",
        "002.csv",
        "003.csv",
        "004.csv",
    ]

    store_master_df = pd.DataFrame([
        {"store_code": "001", "is_active": True},
        {"store_code": "002", "is_active": True},
        {"store_code": "003", "is_active": True},
    ])

    with pytest.raises(ValueError):
        validate_csv_count(csv_files, store_master_df)

def test_validate_csv_count_error_less():
    csv_files = [
        "001.csv",
        "002.csv",
        "003.csv",
    ]

    store_master_df = pd.DataFrame([
        {"store_code": "001", "is_active": True},
        {"store_code": "002", "is_active": True},
        {"store_code": "003", "is_active": True},
        {"store_code": "004", "is_active": True},
    ])

    with pytest.raises(ValueError):
        validate_csv_count(csv_files, store_master_df)
