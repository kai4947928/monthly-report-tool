import pandas as pd

from app.config import MASTER_DIR

#店舗マスタ読み込み
def load_store_master():
    file_path = MASTER_DIR / "store_master_20260524.csv"
    return pd.read_csv(file_path, dtype={"store_code": str},)

#エリアマスタ読み込み
def load_area_master():
    file_path = MASTER_DIR / "area_master_20260524.csv"
    return pd.read_csv(file_path, dtype={"store_code": str},)

#コストマスタ読み込み
def load_cost_master():
    file_path = MASTER_DIR / "cost_master_20260529.csv"
    return pd.read_csv(file_path, dtype={"store_code": str},)


#消費税マスタ読み込み
def load_tax_rate_master():
    file_path = MASTER_DIR / "tax_rate_master_20260529.csv"
    return pd.read_csv(file_path, dtype={"store_code": str},)

