import pandas as pd
import pytest

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
    validate_duplicate_data_check,
    validate_tax_rate_period,
    validate_cost_master_check,
)

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

def test_validate_business_date_complete_success():
    target_month = "202606"

    start_date = pd.to_datetime(target_month + "01")
    end_date = start_date + pd.offsets.MonthEnd(0)
    expected_dates = set(pd.date_range(start=start_date, end=end_date))

    records = []

    for date in expected_dates:
        records.append({
            "store_code": "001",
            "business_date": date,
        })

    monthly_sales_df = pd.DataFrame(records)

    validate_business_date_complete(monthly_sales_df, target_month)

def test_validate_business_date_complete_error_missing_date():
    target_month = "202606"

    start_date = pd.to_datetime(target_month + "01")
    end_date = start_date + pd.offsets.MonthEnd(0)
    expected_dates = pd.date_range(start=start_date, end=end_date)

    records = []

    missing_date = pd.to_datetime("2026-06-15")
    for date in expected_dates:
        if date == missing_date:
            continue
        records.append({
            "store_code": "001",
            "business_date": date,
        })

    monthly_sales_df = pd.DataFrame(records)

    with pytest.raises(ValueError):
        validate_business_date_complete(monthly_sales_df, target_month)

def test_validate_area_codes_success():
    monthly_sales_df = pd.DataFrame([
        {"area_code": "A"},
        {"area_code": "B"},
        {"area_code": "C"},
    ])

    area_master_df = pd.DataFrame([
        {"area_code": "A", "is_active": True},
        {"area_code": "B", "is_active": True},
        {"area_code": "C", "is_active": True},
    ])

    validate_area_codes(monthly_sales_df, area_master_df)

def test_validate_area_codes_error_inactive():
    monthly_sales_df = pd.DataFrame([
        {"area_code": "A"},
        {"area_code": "B"},
        {"area_code": "C"},
    ])

    area_master_df = pd.DataFrame([
        {"area_code": "A", "is_active": True},
        {"area_code": "B", "is_active": True},
        {"area_code": "C", "is_active": False},
    ])

    with pytest.raises(ValueError):
        validate_area_codes(monthly_sales_df, area_master_df)

def test_validate_area_codes_error_not_found():
    monthly_sales_df = pd.DataFrame([
        {"area_code": "A"},
        {"area_code": "B"},
        {"area_code": "C"},
    ])

    area_master_df = pd.DataFrame([
        {"area_code": "A", "is_active": True},
        {"area_code": "B", "is_active": True},
    ])

    with pytest.raises(ValueError):
        validate_area_codes(monthly_sales_df, area_master_df)

def test_validate_area_count_success():
    store_master_df = pd.DataFrame([
        {"store_code": "001", "area_code": "A"},
        {"store_code": "002", "area_code": "B"},
        {"store_code": "003", "area_code": "C"},
        {"store_code": "004", "area_code": "D"}
    ])

    area_master_df = pd.DataFrame([
        {"area_code": "A", "is_active": True},
        {"area_code": "B", "is_active": True},
        {"area_code": "C", "is_active": True},
        {"area_code": "D", "is_active": True},
    ])

    validate_area_count(area_master_df, store_master_df)

def test_validate_area_count_error():
    store_master_df = pd.DataFrame([
        {"store_code": "001", "area_code": "A"},
        {"store_code": "002", "area_code": "B"},
        {"store_code": "003", "area_code": "C"},
        {"store_code": "004", "area_code": "D"}
    ])

    area_master_df = pd.DataFrame([
        {"area_code": "A", "is_active": True},
        {"area_code": "B", "is_active": True},
        {"area_code": "C", "is_active": True},
    ])

    with pytest.raises(ValueError):
        validate_area_count(area_master_df, store_master_df)

def test_validate_null_check_success():
    monthly_sales_df = pd.DataFrame([
        {"store_code": "001",
        "business_date": "2026-07-05",
        "sales_amount_tax_ex": 1000000,
        "customer_count": 500}
    ])

    validate_null_check(monthly_sales_df)

def test_validate_null_check_error():
    monthly_sales_df = pd.DataFrame([
        {"store_code": "001",
        "business_date": "2026-07-05",
        "sales_amount_tax_ex": 1000000,
        "customer_count": pd.NA}
    ])

    with pytest.raises(ValueError):
        validate_null_check(monthly_sales_df)

def test_validate_numeric_check_success():
    monthly_sales_df = pd.DataFrame([
        {"sales_amount_tax_ex": 1000000, "customer_count": 500},
    ])

    validate_numeric_check(monthly_sales_df)

def test_validate_numeric_check_error():
    monthly_sales_df = pd.DataFrame([
        {"sales_amount_tax_ex": 1000000, "customer_count": "五百"},
    ])

    with pytest.raises(ValueError, match="数値項目 customer_count に不正な値が存在します。"):
        validate_numeric_check(monthly_sales_df)

def test_validate_duplicate_check_success():
    monthly_sales_df = pd.DataFrame([
        {"store_code": "001", "business_date": "2026-06-05"},
        {"store_code": "001", "business_date": "2026-06-06"},
        {"store_code": "002", "business_date": "2026-06-05"},
        {"store_code": "002", "business_date": "2026-06-06"}
    ])

    validate_duplicate_data_check(monthly_sales_df)

def test_validate_duplicate_check_error():
    monthly_sales_df = pd.DataFrame([
        {"store_code": "001", "business_date": "2026-06-05"},
        {"store_code": "001", "business_date": "2026-06-05"},
        {"store_code": "002", "business_date": "2026-06-05"},
        {"store_code": "002", "business_date": "2026-06-05"}
    ])

    with pytest.raises(ValueError, match="同一店舗・同一営業日の重複データが存在します。"):
        validate_duplicate_data_check(monthly_sales_df)

def test_validate_tax_rate_period_success():
    target_month = "202606"

    tax_rate_master_df = pd.DataFrame([
        {
            "tax_rate": "0.08",
            "valid_from": "2014-04-01",
            "valid_to": "2019-09-30"
        },
        {
            "tax_rate": "0.10",
            "valid_from": "2019-10-01",
            "valid_to": "2099-12-31"
        }
    ])

    validate_tax_rate_period(tax_rate_master_df, target_month)

def test_validate_tax_rate_period_error():
    target_month = "202606"

    tax_rate_master_df = pd.DataFrame([
        {
            "tax_rate": "0.08",
            "valid_from": "2014-04-01",
            "valid_to": "2019-09-30"
        },
        {
            "tax_rate": "0.10",
            "valid_from": "2019-10-01",
            "valid_to": "2025-09-30"
        }
    ])

    with pytest.raises(ValueError, match="対象月に適用できる税率を取得できません"):
        validate_tax_rate_period(tax_rate_master_df, target_month)

def test_validate_tax_rate_period_error_overlapping():
    target_month = "202606"

    tax_rate_master_df = pd.DataFrame([
        {
            "tax_rate": "0.08",
            "valid_from": "2019-10-01",
            "valid_to": "2026-09-30"
        },
        {
            "tax_rate": "0.10",
            "valid_from": "2019-10-01",
            "valid_to": "2026-09-30"
        }
    ])

    with pytest.raises(ValueError, match="対象月に適用できる税率を取得できません"):
        validate_tax_rate_period(tax_rate_master_df, target_month)

def test_validate_cost_master_check():
    store_master_df = pd.DataFrame([
        {"store_code": "001"},
        {"store_code": "002"},
        {"store_code": "003"},
    ])

    cost_master_df = pd.DataFrame([
        {"store_code": "001"},
        {"store_code": "002"},
        {"store_code": "003"},
    ])

    validate_cost_master_check(store_master_df, cost_master_df)