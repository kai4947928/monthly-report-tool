MONTHLY_SALES_REQUIRED_COLUMNS = {
    "store_code",
    "business_date",
    "sales_amount_tax_ex",
    "customer_count",
}

STORE_MASTER_REQUIRED_COLUMNS = {
    "store_code",
    "store_name",
    "area_code",
    "area_name",
    "is_active",
}

COST_MASTER_REQUIRED_COLUMNS = {
    "store_code",
    "cost_rate",
    "labor_cost_rate",
    "rent_cost",
    "utility_cost",
    "other_expense_cost",
}

TAX_RATE_MASTER_REQUIRED_COLUMNS = {
    "tax_rate",
    "valid_from",
    "valid_to",
    "is_active",
}
