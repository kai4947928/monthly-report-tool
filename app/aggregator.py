def aggregate_store_data(sales_df, tax_rate_master_df):
    sales_amount_tax_ex = sales_df["sales_amount_tax_ex"].sum()
    customer_count = sales_df["customer_count"].sum()

    active_tax_rate = tax_rate_master_df.loc[
        tax_rate_master_df["is_active"] == 1,
        "tax_rate"
    ].iloc[0]

    tax_amount = sales_amount_tax_ex * active_tax_rate
    sales_amount_tax_in = sales_amount_tax_ex + tax_amount

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
    }

    return result
