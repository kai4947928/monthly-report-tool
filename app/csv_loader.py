import pandas as pd
from app.config import INPUT_DIR

def load_csv(file_path):
    df = pd.read_csv(file_path)

    return df

def load_monthly_sales_csv(target_month):
    input_dir = INPUT_DIR / target_month
    csv_files = list(input_dir.glob("*.csv"))

    sales_df_list = []

    for csv_file in csv_files:
        df = pd.read_csv(csv_file)
        sales_df_list.append(df)

    monthly_sales_df = pd.concat(sales_df_list, ignore_index=True)

    return monthly_sales_df
