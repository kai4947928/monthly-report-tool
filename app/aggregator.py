def aggregate_store_data(sales_df, tax_rate_master_df, cost_master_df):

    #1ヶ月の税抜売上
    sales_amount_tax_ex = sales_df["sales_amount_tax_ex"].sum()

    #1ヶ月の来客数
    customer_count = sales_df["customer_count"].sum()

    #利用できる消費税
    active_tax_rate = tax_rate_master_df.loc[
        tax_rate_master_df["is_active"] == 1,
        "tax_rate"
    ].iloc[0]

    tax_amount = sales_amount_tax_ex * active_tax_rate
    sales_amount_tax_in = sales_amount_tax_ex + tax_amount

    #対象店舗
    store_code = sales_df["store_code"].iloc[0]
    store_cost = cost_master_df.loc[
        cost_master_df["store_code"] == store_code
    ]

    #原価
    cost_rate = store_cost["cost_rate"].iloc[0]
    cost_amount = sales_amount_tax_ex * cost_rate

    #人件費
    labor_cost_rate = store_cost["labor_cost_rate"].iloc[0]
    labor_cost_amount = (
        sales_amount_tax_ex * labor_cost_rate
    )

    #経費
    rent_cost = store_cost["rent_cost"].iloc[0]
    utility_cost = store_cost["utility_cost"].iloc[0]
    other_expense_cost = store_cost["other_expense_cost"].iloc[0]
    expense_amount = (
        rent_cost + utility_cost + other_expense_cost
    )

    #粗利
    gross_profit = (
        sales_amount_tax_ex - cost_amount
    )

    net_profit = (
        sales_amount_tax_ex - cost_amount - labor_cost_amount - expense_amount
    )

    if sales_amount_tax_ex == 0:
        profit_rate = 0
    else:
        profit_rate = (
            net_profit / sales_amount_tax_ex
        ) * 100

    if customer_count == 0:
        average_spend = 0
    else:
        average_spend =sales_amount_tax_in / customer_count

    result = {
        "sales_amount_tax_in": sales_amount_tax_in,
        "sales_amount_tax_ex": sales_amount_tax_ex,
        "tax_amount": tax_amount,
        "customer_count": customer_count,
        "average_spend": average_spend,
        "tax_rate": active_tax_rate,
        "cost_amount": cost_amount,
        "labor_cost_amount": labor_cost_amount,
        "expense_amount": expense_amount,
        "gross_profit": gross_profit,
        "net_profit": net_profit,
        "profit_rate": profit_rate,
    }

    return result
