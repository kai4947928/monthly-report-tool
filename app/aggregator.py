#店舗データ集計関数
def aggregate_store_data(store_df, tax_rate_master_df, cost_master_df):
    #店舗の税抜合計
    sales_amount_tax_ex = store_df["sales_amount_tax_ex"].sum()

    #店舗の来店数合計
    customer_count = store_df["customer_count"].sum()

    #有効消費税率を取得
    active_tax_rate = tax_rate_master_df.loc[
        tax_rate_master_df["is_active"] == 1,
        "tax_rate"
    ].iloc[0]

    #店舗売上消費税額
    tax_amount = sales_amount_tax_ex * active_tax_rate
    #店舗税込額
    sales_amount_tax_in = sales_amount_tax_ex + tax_amount

    #店舗のコスト情報を取得
    store_code = store_df["store_code"].iloc[0]
    store_cost = cost_master_df.loc[
        cost_master_df["store_code"] == store_code
    ]

    #店舗の原価率を取得し、店舗の原価を集計
    cost_rate = store_cost["cost_rate"].iloc[0]
    cost_amount = sales_amount_tax_ex * cost_rate
    cost_rate_percent = cost_rate * 100

    #店舗の人件費率を取得し、店舗の人件費を集計
    labor_cost_rate = store_cost["labor_cost_rate"].iloc[0]
    labor_cost_amount = (
        sales_amount_tax_ex * labor_cost_rate
    )
    labor_cost_rate_percent = labor_cost_rate * 100

    #店舗の固定費を取得し、人件費を含めた店舗運営費用を集計
    rent_cost = store_cost["rent_cost"].iloc[0]
    utility_cost = store_cost["utility_cost"].iloc[0]
    other_expense_cost = store_cost["other_expense_cost"].iloc[0]
    operating_cost = (
        rent_cost + utility_cost + other_expense_cost + labor_cost_amount
    )

    #営業利益
    operating_profit = (
        sales_amount_tax_ex - cost_amount - operating_cost
    )

    #営業利益率
    if sales_amount_tax_ex == 0:
        operating_profit_rate = 0
    else:
        operating_profit_rate = (
            operating_profit / sales_amount_tax_ex
        ) * 100

    #客単価
    if customer_count == 0:
        average_customer_spend = 0
    else:
        average_customer_spend = sales_amount_tax_in / customer_count

    store_summary = {
        "sales_amount_tax_in": sales_amount_tax_in,
        "sales_amount_tax_ex": sales_amount_tax_ex,
        "tax_amount": tax_amount,
        "customer_count": customer_count,
        "average_customer_spend": average_customer_spend,
        "tax_rate": active_tax_rate,
        "cost_amount": cost_amount,
        "labor_cost_amount": labor_cost_amount,
        "rent_cost": rent_cost,
        "utility_cost": utility_cost,
        "other_expense_cost": other_expense_cost,
        "operating_cost": operating_cost,
        "cost_rate": cost_rate_percent,
        "labor_cost_rate": labor_cost_rate_percent,
        "operating_profit": operating_profit,
        "operating_profit_rate": operating_profit_rate,
    }

    return store_summary

#エリアデータ集計関数
def aggregate_area_data(area_df, tax_rate_master_df, cost_master_df):
    #エリア税抜合計
    sales_amount_tax_ex = area_df["sales_amount_tax_ex"].sum()
    #エリア来店客数合計
    customer_count = area_df["customer_count"].sum()

    #有効消費税率取得
    active_tax_rate = tax_rate_master_df.loc[
        tax_rate_master_df["is_active"] == 1,
        "tax_rate"
    ].iloc[0]

    #エリア売上消費税額
    tax_amount = sales_amount_tax_ex * active_tax_rate
    #エリア売上税込額
    sales_amount_tax_in = sales_amount_tax_ex + tax_amount

    #エリア客単価
    if customer_count == 0:
        average_customer_spend = 0
    else:
        average_customer_spend = sales_amount_tax_in / customer_count

    #エリア内のコスト合計を初期化
    cost_amount = 0
    labor_cost_amount = 0
    rent_cost = 0
    utility_cost = 0
    other_expense_cost = 0

    #エリア内の店舗を1店舗ずつ処理
    for store_code, store_df in area_df.groupby("store_code"):
        #店舗の税抜売上合計
        store_sales_amount_tax_ex = store_df["sales_amount_tax_ex"].sum()

        #店舗のコストマスタ取得
        store_cost_master = cost_master_df.loc[
            cost_master_df["store_code"] == store_code
        ]

        #店舗の原価率
        cost_rate = store_cost_master["cost_rate"].iloc[0]
        #店舗の人件費率
        labor_cost_rate = store_cost_master["labor_cost_rate"].iloc[0]

        #店舗ごとのコストをエリア合計へ加算
        rent_cost += store_cost_master["rent_cost"].iloc[0]
        utility_cost += store_cost_master["utility_cost"].iloc[0]
        other_expense_cost += store_cost_master["other_expense_cost"].iloc[0]
        cost_amount += store_sales_amount_tax_ex * cost_rate
        labor_cost_amount += store_sales_amount_tax_ex * labor_cost_rate

    #店舗運営費用
    operating_cost = (
        labor_cost_amount
        + rent_cost
        + utility_cost
        + other_expense_cost
    )

    #営業利益
    operating_profit = (
        sales_amount_tax_ex
        - operating_cost
        - cost_amount
    )

    #営業利益率,原価率,人件費率
    if sales_amount_tax_ex == 0:
        cost_rate_percent = 0
        labor_cost_rate_percent = 0
        operating_profit_rate = 0
    else:
        cost_rate_percent = (
            cost_amount / sales_amount_tax_ex
        ) * 100

        labor_cost_rate_percent = (
            labor_cost_amount / sales_amount_tax_ex
        ) * 100

        operating_profit_rate = (
            operating_profit / sales_amount_tax_ex
        ) * 100

    area_summary = {
        "sales_amount_tax_in": sales_amount_tax_in,
        "sales_amount_tax_ex": sales_amount_tax_ex,
        "tax_amount": tax_amount,
        "customer_count": customer_count,
        "average_customer_spend": average_customer_spend,
        "tax_rate": active_tax_rate,
        "cost_amount": cost_amount,
        "labor_cost_amount": labor_cost_amount,
        "rent_cost": rent_cost,
        "utility_cost": utility_cost,
        "other_expense_cost": other_expense_cost,
        "operating_cost": operating_cost,
        "operating_profit": operating_profit,
        "cost_rate": cost_rate_percent,
        "labor_cost_rate": labor_cost_rate_percent,
        "operating_profit_rate": operating_profit_rate,
    }

    return area_summary

#全体集計関数
def aggregate_overall_data(area_summaries):
    if not area_summaries:
        raise ValueError("エリア集計結果が存在しません")

    sales_amount_tax_in = sum(
        area_summary["sales_amount_tax_in"]
        for area_summary in area_summaries
    )

    sales_amount_tax_ex = sum(
        area_summary["sales_amount_tax_ex"]
        for area_summary in area_summaries
    )

    tax_amount = sum(
        area_summary["tax_amount"]
        for area_summary in area_summaries
    )

    customer_count = sum(
        area_summary["customer_count"]
        for area_summary in area_summaries
    )

    cost_amount = sum(
        area_summary["cost_amount"]
        for area_summary in area_summaries
    )

    labor_cost_amount = sum(
        area_summary["labor_cost_amount"]
        for area_summary in area_summaries
    )

    rent_cost = sum(
        area_summary["rent_cost"]
        for area_summary in area_summaries
    )

    utility_cost = sum(
        area_summary["utility_cost"]
        for area_summary in area_summaries
    )

    other_expense_cost = sum(
        area_summary["other_expense_cost"]
        for area_summary in area_summaries
    )

    operating_cost = sum(
        area_summary["operating_cost"]
        for area_summary in area_summaries
    )

    operating_profit = sum(
        area_summary["operating_profit"]
        for area_summary in area_summaries
    )

    active_tax_rate = area_summaries[0]["tax_rate"]

    if customer_count == 0:
        average_customer_spend = 0
    else:
        average_customer_spend = (
            sales_amount_tax_in / customer_count
        )

    if sales_amount_tax_ex == 0:
        cost_rate_percent = 0
        labor_cost_rate_percent = 0
        operating_profit_rate = 0
    else:
        cost_rate_percent = (
            cost_amount / sales_amount_tax_ex
        ) * 100

        labor_cost_rate_percent = (
            labor_cost_amount / sales_amount_tax_ex
        ) * 100

        operating_profit_rate = (
            operating_profit / sales_amount_tax_ex
        ) * 100

    overall_summary = {
        "sales_amount_tax_in": sales_amount_tax_in,
        "sales_amount_tax_ex": sales_amount_tax_ex,
        "tax_amount": tax_amount,
        "customer_count": customer_count,
        "average_customer_spend": average_customer_spend,
        "tax_rate": active_tax_rate,
        "cost_amount": cost_amount,
        "labor_cost_amount": labor_cost_amount,
        "rent_cost": rent_cost,
        "utility_cost": utility_cost,
        "other_expense_cost": other_expense_cost,
        "operating_cost": operating_cost,
        "operating_profit": operating_profit,
        "cost_rate": cost_rate_percent,
        "labor_cost_rate": labor_cost_rate_percent,
        "operating_profit_rate": operating_profit_rate,
    }

    return overall_summary
