from openpyxl import load_workbook

PERCENTAGE_NUMBER_FORMAT = "0.0%"

def _write_percentage_values(sheet, result):
    """比率を小数値で書き込み、Excelのパーセント表示を設定する。"""
    percentage_cells = {
        "D18": result["cost_rate"],
        "F18": result["labor_cost_rate"],
        "B21": result["operating_profit_rate"],
    }

    for cell_address, value in percentage_cells.items():
        sheet[cell_address] = value
        sheet[cell_address].number_format = PERCENTAGE_NUMBER_FORMAT


def write_overall_report(
    result,
    target_month,
    template_path,
    output_path,
):
    workbook = load_workbook(template_path)
    sheet = workbook.active

    # 基本情報
    sheet["A1"] = f"【{target_month}】全体月次報告書"
    sheet["B3"] = target_month
    sheet["D3"] = "ALL"
    sheet["F3"] = "全体"

    # 売上情報
    sheet["B6"] = result["sales_amount_tax_ex"]
    sheet["D6"] = result["tax_amount"]
    sheet["F6"] = result["sales_amount_tax_in"]

    # 顧客・税率情報
    sheet["B9"] = result["customer_count"]
    sheet["D9"] = result["average_customer_spend"]
    sheet["F9"] = result["tax_rate"]

    # コスト情報
    sheet["B12"] = result["cost_amount"]
    sheet["D12"] = result["labor_cost_amount"]
    sheet["F12"] = result["rent_cost"]

    sheet["B15"] = result["utility_cost"]
    sheet["D15"] = result["other_expense_cost"]
    sheet["F15"] = result["operating_cost"]

    # 利益・比率情報
    sheet["B18"] = result["operating_profit"]
    _write_percentage_values(sheet, result)

    workbook.save(output_path)

def write_store_report(
    result,
    target_month,
    store_code,
    store_name,
    template_path,
    output_path,
):
    workbook = load_workbook(template_path)
    sheet = workbook.active

    # 基本情報
    sheet["A1"] = f"【{target_month}】{store_name}月次報告書"
    sheet["B3"] = target_month
    sheet["D3"] = store_code
    sheet["F3"] = store_name

    # 売上情報
    sheet["B6"] = result["sales_amount_tax_ex"]
    sheet["D6"] = result["tax_amount"]
    sheet["F6"] = result["sales_amount_tax_in"]

    # 顧客・税率情報
    sheet["B9"] = result["customer_count"]
    sheet["D9"] = result["average_customer_spend"]
    sheet["F9"] = result["tax_rate"]

    # コスト情報
    sheet["B12"] = result["cost_amount"]
    sheet["D12"] = result["labor_cost_amount"]
    sheet["F12"] = result["rent_cost"]

    sheet["B15"] = result["utility_cost"]
    sheet["D15"] = result["other_expense_cost"]
    sheet["F15"] = result["operating_cost"]

    # 利益・比率情報
    sheet["B18"] = result["operating_profit"]
    _write_percentage_values(sheet, result)

    workbook.save(output_path)


def write_area_report(
    result,
    target_month,
    area_code,
    area_name,
    template_path,
    output_path,
):
    workbook = load_workbook(template_path)
    sheet = workbook.active

    # 基本情報
    sheet["A1"] = f"【{target_month}】{area_name}月次報告書"
    sheet["B3"] = target_month
    sheet["D3"] = area_code
    sheet["F3"] = area_name

    # 売上情報
    sheet["B6"] = result["sales_amount_tax_ex"]
    sheet["D6"] = result["tax_amount"]
    sheet["F6"] = result["sales_amount_tax_in"]

    # 顧客・税率情報
    sheet["B9"] = result["customer_count"]
    sheet["D9"] = result["average_customer_spend"]
    sheet["F9"] = result["tax_rate"]

    # コスト情報
    sheet["B12"] = result["cost_amount"]
    sheet["D12"] = result["labor_cost_amount"]
    sheet["F12"] = result["rent_cost"]

    sheet["B15"] = result["utility_cost"]
    sheet["D15"] = result["other_expense_cost"]
    sheet["F15"] = result["operating_cost"]

    # 利益・比率情報
    sheet["B18"] = result["operating_profit"]
    _write_percentage_values(sheet, result)

    workbook.save(output_path)
