import pandas as pd
from app.aggregator import aggregate_store_data, aggregate_area_data, aggregate_overall_data

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
    assert result["average_spend"] == 1100

    assert result["operating_profit_rate"] == 33

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

    assert result["average_spend"] == 1100

    assert result["cost_amount"] == 90000
    assert result["labor_cost_amount"] == 60000

    assert result["rent_cost"] == 30000
    assert result["utility_cost"] == 15000
    assert result["other_expense_cost"] == 6000

    assert result["operating_profit"] == 99000

def test_aggregate_overall_data():
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

    result = aggregate_overall_data(sales_df, tax_rate_master_df, cost_master_df)

    assert result["sales_amount_tax_ex"] == 300000
    assert result["tax_amount"] == 30000
    assert result["sales_amount_tax_in"] == 330000

    assert result["customer_count"] == 300
    assert result["average_spend"] == 1100

    assert result["cost_amount"] == 90000
    assert result["labor_cost_amount"] == 60000

    assert result["rent_cost"] == 30000
    assert result["utility_cost"] == 15000
    assert result["other_expense_cost"] == 6000

    assert result["operating_profit"] == 99000
