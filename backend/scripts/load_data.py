"""Load the Phase 1 BBQ CSVs into a normalized SQLite database.

Usage (from the project root):

    python scripts/load_data.py

Reads the five CSVs from ``config.DATASET_DIR`` and writes a fresh
``data/bbq.db`` with primary keys, foreign keys and indexes. Re-running
rebuilds the database from scratch (idempotent).
"""
from __future__ import annotations

import sqlite3
import sys
from pathlib import Path

import pandas as pd

# Make the project root importable when run as a plain script.
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app import config  # noqa: E402

TABLES = ["branches", "products", "customers", "orders", "order_items"]

SCHEMA = """
DROP TABLE IF EXISTS order_items;
DROP TABLE IF EXISTS orders;
DROP TABLE IF EXISTS customers;
DROP TABLE IF EXISTS products;
DROP TABLE IF EXISTS branches;

CREATE TABLE branches (
    branch_id         INTEGER PRIMARY KEY,
    branch_name       TEXT    NOT NULL,
    city              TEXT    NOT NULL,
    popularity_weight REAL    NOT NULL
);

CREATE TABLE products (
    product_id        INTEGER PRIMARY KEY,
    product_name      TEXT    NOT NULL,
    category          TEXT    NOT NULL,
    unit_price        REAL    NOT NULL,
    unit_cost         REAL    NOT NULL,
    popularity_weight REAL    NOT NULL
);

CREATE TABLE customers (
    customer_id   INTEGER PRIMARY KEY,
    customer_name TEXT    NOT NULL,
    phone         TEXT,
    signup_date   TEXT
);

CREATE TABLE orders (
    order_id     INTEGER PRIMARY KEY,
    order_date   TEXT    NOT NULL,
    branch_id    INTEGER NOT NULL REFERENCES branches(branch_id),
    customer_id  INTEGER NOT NULL REFERENCES customers(customer_id),
    total_amount REAL    NOT NULL
);

CREATE TABLE order_items (
    order_item_id INTEGER PRIMARY KEY,
    order_id      INTEGER NOT NULL REFERENCES orders(order_id),
    product_id    INTEGER NOT NULL REFERENCES products(product_id),
    quantity      INTEGER NOT NULL,
    unit_price    REAL    NOT NULL,
    discount_pct  REAL    NOT NULL,
    line_total    REAL    NOT NULL
);
"""

INDEXES = """
CREATE INDEX idx_orders_date     ON orders(order_date);
CREATE INDEX idx_orders_branch   ON orders(branch_id);
CREATE INDEX idx_orders_customer ON orders(customer_id);
CREATE INDEX idx_items_order     ON order_items(order_id);
CREATE INDEX idx_items_product   ON order_items(product_id);
"""


def main() -> None:
    dataset_dir = Path(config.DATASET_DIR)
    db_path = Path(config.DB_PATH)
    db_path.parent.mkdir(parents=True, exist_ok=True)

    missing = [t for t in TABLES if not (dataset_dir / f"{t}.csv").exists()]
    if missing:
        raise SystemExit(
            f"Missing CSV(s) in {dataset_dir}: {', '.join(missing)}.\n"
            "Set BBQ_DATASET_DIR or place the Phase 1 CSVs there."
        )

    conn = sqlite3.connect(db_path)
    try:
        # Enforce referential integrity at load time (must be set outside a txn).
        conn.execute("PRAGMA foreign_keys = ON;")
        conn.executescript(SCHEMA)
        # Parent tables first so foreign keys resolve.
        for table in TABLES:
            df = pd.read_csv(dataset_dir / f"{table}.csv")
            df.to_sql(table, conn, if_exists="append", index=False)
        conn.executescript(INDEXES)
        conn.commit()

        print(f"Loaded SQLite database -> {db_path}\n")
        for table in TABLES:
            n = conn.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]
            print(f"  {table:<12} {n:>7,} rows")
        rev = conn.execute("SELECT SUM(total_amount) FROM orders").fetchone()[0]
        rng = conn.execute(
            "SELECT MIN(order_date), MAX(order_date) FROM orders"
        ).fetchone()
        print(f"\n  date range:    {rng[0]} -> {rng[1]}")
        print(f"  total revenue: PKR {rev:,.0f}")
    finally:
        conn.close()


if __name__ == "__main__":
    main()
