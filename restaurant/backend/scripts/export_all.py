import json
from app import db, config

TABLES = ["branches", "products", "customers", "orders", "order_items"]
result = {table: db.query_rows(f"SELECT * FROM {table}") for table in TABLES}
print(json.dumps(result, indent=2))
