import pandas as pd
import pytest

from app.validator import validate_required_columns, validate_target_month

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
