import pandas as pd
import pytest
from app.aggregator import (
    aggregate_area_data,
    aggregate_overall_data,
    aggregate_store_data,
    calculate_rate,
)


def test_operating_profit_rate_is_calculated_as_decimal():
    assert calculate_rate(300_000, 1_000_000) == pytest.approx(0.3)

def test_aggregate_store_data():
    sales_df = pd.DataFrame([
        {
            "store_code": "001",
            "sales_amount_tax_ex": 100000,
            "customer_count": 100,
        }
    ])

    tax_rate_master_df = pd.DataFrame([
        {
            "tax_rate": 0.1,
            "is_active": 1,
        }
    ])

    cost_master_df = pd.DataFrame([
        {
            "store_code": "001",
            "cost_rate": 0.3,
            "labor_cost_rate": 0.2,
            "rent_cost": 10000,
            "utility_cost": 5000,
            "other_expense_cost": 2000,
        }
    ])

    result = aggregate_store_data(sales_df, tax_rate_master_df, cost_master_df)

    assert result["tax_amount"] == 10000
    assert result["sales_amount_tax_in"] == 110000

    assert result["cost_amount"] == 30000
    assert result["labor_cost_amount"] == 20000

    assert result["rent_cost"] == 10000
    assert result["utility_cost"] == 5000
    assert result["other_expense_cost"] == 2000

    assert result["operating_profit"] == 33000

    assert result["customer_count"] == 100
    assert result["average_customer_spend"] == 1100

    assert result["cost_rate"] == pytest.approx(0.3)
    assert result["labor_cost_rate"] == pytest.approx(0.2)
    assert result["operating_profit_rate"] == pytest.approx(0.33)

def test_aggregate_area_data():
    sales_df = pd.DataFrame([
        {
            "store_code": "001",
            "sales_amount_tax_ex": 100000,
            "customer_count": 100,
        },
        {
            "store_code": "002",
            "sales_amount_tax_ex": 200000,
            "customer_count": 200,
        }
    ])

    tax_rate_master_df = pd.DataFrame([
        {
            "tax_rate": 0.1,
            "is_active": 1,
        }
    ])

    cost_master_df = pd.DataFrame([
        {
            "store_code": "001",
            "cost_rate": 0.3,
            "labor_cost_rate": 0.2,
            "rent_cost": 10000,
            "utility_cost": 5000,
            "other_expense_cost": 2000,
        },
        {
            "store_code": "002",
            "cost_rate": 0.3,
            "labor_cost_rate": 0.2,
            "rent_cost": 20000,
            "utility_cost": 10000,
            "other_expense_cost": 4000,
        }
    ])

    result = aggregate_area_data(sales_df, tax_rate_master_df, cost_master_df)

    assert result["sales_amount_tax_ex"] == 300000
    assert result["tax_amount"] == 30000
    assert result["sales_amount_tax_in"] == 330000
    assert result["customer_count"] == 300

    assert result["average_customer_spend"] == 1100

    assert result["cost_amount"] == 90000
    assert result["labor_cost_amount"] == 60000

    assert result["rent_cost"] == 30000
    assert result["utility_cost"] == 15000
    assert result["other_expense_cost"] == 6000

    assert result["operating_profit"] == 99000

    assert result["cost_rate"] == pytest.approx(0.3)
    assert result["labor_cost_rate"] == pytest.approx(0.2)
    assert result["operating_profit_rate"] == pytest.approx(0.33)

def test_aggregate_overall_data():
    area_summaries = [
        {
            "sales_amount_tax_in": 110000,
            "sales_amount_tax_ex": 100000,
            "tax_amount": 10000,
            "customer_count": 100,
            "cost_amount": 30000,
            "labor_cost_amount": 20000,
            "rent_cost": 10000,
            "utility_cost": 5000,
            "other_expense_cost": 2000,
            "operating_cost": 37000,
            "operating_profit": 33000,
            "tax_rate": 0.1,
        },
        {
            "sales_amount_tax_in": 220000,
            "sales_amount_tax_ex": 200000,
            "tax_amount": 20000,
            "customer_count": 200,
            "cost_amount": 60000,
            "labor_cost_amount": 40000,
            "rent_cost": 20000,
            "utility_cost": 10000,
            "other_expense_cost": 4000,
            "operating_cost": 74000,
            "operating_profit": 66000,
            "tax_rate": 0.1,
        }
    ]

    result = aggregate_overall_data(area_summaries)

    assert result["sales_amount_tax_ex"] == 300000
    assert result["tax_amount"] == 30000
    assert result["sales_amount_tax_in"] == 330000

    assert result["customer_count"] == 300
    assert result["average_customer_spend"] == 1100

    assert result["cost_amount"] == 90000
    assert result["labor_cost_amount"] == 60000

    assert result["rent_cost"] == 30000
    assert result["utility_cost"] == 15000
    assert result["other_expense_cost"] == 6000

    assert result["operating_profit"] == 99000

    assert result["cost_rate"] == pytest.approx(0.3)
    assert result["labor_cost_rate"] == pytest.approx(0.2)
    assert result["operating_profit_rate"] == pytest.approx(0.33)


def test_operating_profit_rate_is_zero_when_sales_are_zero():
    sales_df = pd.DataFrame([
        {
            "store_code": "001",
            "sales_amount_tax_ex": 0,
            "customer_count": 0,
        }
    ])
    tax_rate_master_df = pd.DataFrame([{"tax_rate": 0.1, "is_active": 1}])
    cost_master_df = pd.DataFrame([
        {
            "store_code": "001",
            "cost_rate": 0.3,
            "labor_cost_rate": 0.2,
            "rent_cost": 0,
            "utility_cost": 0,
            "other_expense_cost": 0,
        }
    ])

    result = aggregate_store_data(sales_df, tax_rate_master_df, cost_master_df)

    assert result["cost_rate"] == 0
    assert result["labor_cost_rate"] == 0
    assert result["operating_profit_rate"] == 0


def test_operating_profit_rate_is_negative_when_store_has_a_loss():
    sales_df = pd.DataFrame([
        {
            "store_code": "001",
            "sales_amount_tax_ex": 100000,
            "customer_count": 100,
        }
    ])
    tax_rate_master_df = pd.DataFrame([{"tax_rate": 0.1, "is_active": 1}])
    cost_master_df = pd.DataFrame([
        {
            "store_code": "001",
            "cost_rate": 0.5,
            "labor_cost_rate": 0.4,
            "rent_cost": 20000,
            "utility_cost": 0,
            "other_expense_cost": 0,
        }
    ])

    result = aggregate_store_data(sales_df, tax_rate_master_df, cost_master_df)

    assert result["operating_profit"] == -10000
    assert result["operating_profit_rate"] == pytest.approx(-0.1)


def test_operating_profit_rate_is_zero_when_profit_is_zero():
    area_summaries = [
        {
            "sales_amount_tax_in": 110000,
            "sales_amount_tax_ex": 100000,
            "tax_amount": 10000,
            "customer_count": 100,
            "cost_amount": 30000,
            "labor_cost_amount": 20000,
            "rent_cost": 30000,
            "utility_cost": 10000,
            "other_expense_cost": 10000,
            "operating_cost": 70000,
            "operating_profit": 0,
            "tax_rate": 0.1,
        }
    ]

    result = aggregate_overall_data(area_summaries)

    assert result["operating_profit_rate"] == 0
