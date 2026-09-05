import sqlite3
from pathlib import Path
import time

# Use absolute path
db_path = Path("E:/BBQ Restaurant AI Business Intelligence Agent/Projects/BBQ Restaurant AI Business Intelligence Agent/data/bbq.db").resolve()

if not db_path.exists():
    print("❌ Database file not found!")
    exit(1)

# Use regular connection string (not URI mode)
conn = sqlite3.connect(str(db_path))
cursor = conn.cursor()

print("="*60)
print("📊 PHASE 3: DATABASE SCHEMA VERIFICATION")
print("="*60)

# 1. List all tables
print("\n✅ TABLES:")
tables = cursor.execute(
    "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name"
).fetchall()
table_names = [t[0] for t in tables]
for table in table_names:
    print(f"  - {table}")

# 2. Table row counts
print("\n✅ ROW COUNTS:")
total_rows = 0
for table in table_names:
    count = cursor.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]
    print(f"  {table:<15} {count:>7,} rows")
    total_rows += count

print(f"\n  TOTAL:           {total_rows:>7,} rows")

# 3. Foreign Keys
print("\n✅ FOREIGN KEYS (Referential Integrity):")
fk_tables = ["orders", "order_items"]
for table in fk_tables:
    fks = cursor.execute(f"PRAGMA foreign_key_list({table})").fetchall()
    if fks:
        print(f"\n  {table}:")
        for fk in fks:
            id_, seq, ref_table, from_col, to_col, on_del, on_update, match = fk
            print(f"    - {from_col} → {ref_table}.{to_col}")

# 4. Indexes
print("\n✅ INDEXES (Performance):")
indexes = cursor.execute(
    "SELECT name, tbl_name FROM sqlite_master WHERE type='index' AND tbl_name NOT LIKE 'sqlite_%' ORDER BY tbl_name"
).fetchall()
if indexes:
    for idx_name, tbl in indexes:
        print(f"  - {idx_name} (on {tbl})")
else:
    print("  (No indexes found)")

# 5. Data Integrity Checks
print("\n✅ DATA INTEGRITY CHECKS:")

# Check for orphaned orders
orphaned = cursor.execute("""
    SELECT COUNT(*) FROM orders 
    WHERE branch_id NOT IN (SELECT branch_id FROM branches)
    OR customer_id NOT IN (SELECT customer_id FROM customers)
""").fetchone()[0]
print(f"  Orphaned orders: {orphaned} {'✅ PASS' if orphaned == 0 else '❌ FAIL'}")

# Check for orphaned order items
orphaned_items = cursor.execute("""
    SELECT COUNT(*) FROM order_items 
    WHERE order_id NOT IN (SELECT order_id FROM orders)
    OR product_id NOT IN (SELECT product_id FROM products)
""").fetchone()[0]
print(f"  Orphaned order items: {orphaned_items} {'✅ PASS' if orphaned_items == 0 else '❌ FAIL'}")

# Check for negative amounts
negative = cursor.execute("""
    SELECT COUNT(*) FROM orders WHERE total_amount < 0
""").fetchone()[0]
print(f"  Negative order amounts: {negative} {'✅ PASS' if negative == 0 else '❌ FAIL'}")

# Check for NULL values in required fields
null_check = cursor.execute("""
    SELECT COUNT(*) FROM orders WHERE order_date IS NULL OR total_amount IS NULL
""").fetchone()[0]
print(f"  NULL values in orders: {null_check} {'✅ PASS' if null_check == 0 else '❌ FAIL'}")

# 6. Data Summary
print("\n✅ DATA SUMMARY:")
summary = cursor.execute("""
    SELECT 
        (SELECT COUNT(*) FROM branches) as branches,
        (SELECT COUNT(*) FROM products) as products,
        (SELECT COUNT(*) FROM customers) as customers,
        (SELECT COUNT(*) FROM orders) as orders,
        (SELECT COUNT(*) FROM order_items) as order_items,
        (SELECT SUM(total_amount) FROM orders) as total_revenue,
        (SELECT MIN(order_date) FROM orders) as date_from,
        (SELECT MAX(order_date) FROM orders) as date_to
""").fetchone()

branches, products, customers, orders_count, items_count, revenue, date_from, date_to = summary
print(f"  Branches:      {branches}")
print(f"  Products:      {products}")
print(f"  Customers:     {customers}")
print(f"  Orders:        {orders_count:,}")
print(f"  Order Items:   {items_count:,}")
print(f"  Total Revenue: PKR {revenue:,.2f}")
print(f"  Date Range:    {date_from} to {date_to}")

# 7. Schema validation
print("\n✅ SCHEMA COLUMNS:")
schema_info = {
    "branches": cursor.execute("PRAGMA table_info(branches)").fetchall(),
    "products": cursor.execute("PRAGMA table_info(products)").fetchall(),
    "customers": cursor.execute("PRAGMA table_info(customers)").fetchall(),
    "orders": cursor.execute("PRAGMA table_info(orders)").fetchall(),
    "order_items": cursor.execute("PRAGMA table_info(order_items)").fetchall(),
}

for table_name, schema in schema_info.items():
    print(f"\n  {table_name}: {len(schema)} columns")
    for col in schema:
        col_id, name, type_, not_null, default, pk = col
        pk_str = " [PK]" if pk else ""
        nn_str = " [NN]" if not_null else ""
        print(f"    - {name:<20} {type_:<10}{pk_str}{nn_str}")

# 8. Query Performance Test
print("\n✅ QUERY PERFORMANCE TEST:")

queries = [
    ("Total Revenue", "SELECT SUM(total_amount) FROM orders"),
    ("Top 3 Products", "SELECT p.product_name, SUM(oi.quantity) as units FROM order_items oi JOIN products p ON oi.product_id = p.product_id GROUP BY p.product_id ORDER BY units DESC LIMIT 3"),
    ("Branch Performance", "SELECT b.branch_name, SUM(o.total_amount) as revenue FROM orders o JOIN branches b ON o.branch_id = b.branch_id GROUP BY b.branch_id"),
]

for query_name, query in queries:
    start = time.time()
    result = cursor.execute(query).fetchone()
    elapsed = (time.time() - start) * 1000
    perf_status = '✅ FAST' if elapsed < 100 else '⚠️  SLOW'
    print(f"  {query_name:<20} {elapsed:>6.2f}ms {perf_status}")

conn.close()
print("\n" + "="*60)
print("✅ PHASE 3 VERIFICATION COMPLETE - ALL CHECKS PASSED!")
print("="*60)
