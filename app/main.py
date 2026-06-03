from app.master_loader import (
    load_store_master,
    load_area_master,
    load_cost_master,
    load_tax_rate_master,
)

store_master = load_store_master()
area_master = load_area_master()
cost_master = load_cost_master()
tax_rate_master = load_tax_rate_master()

print(store_master.head())
print(area_master.head())
print(cost_master.head())
print(tax_rate_master.head())
