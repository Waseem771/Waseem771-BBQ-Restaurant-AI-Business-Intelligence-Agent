"""Analytics queries over the BBQ database.

Each function runs a controlled, read-only SQL query and returns plain
Python data structures (dicts / lists of dicts). These are the building
blocks shared by the FastAPI endpoints, the dashboard, and the AI
assistant's deterministic engine — business logic lives here, not in the
route handlers (CLAUDE.md sec. 31).
"""
from __future__ import annotations

import pandas as pd

from . import db

# SQLite strftime('%w'): Sunday=0 ... Saturday=6.
# The dataset treats Friday (5) and Saturday (6) as the weekend rush.
_WEEKEND = (5, 6)


def kpis() -> dict:
    """Headline KPIs for the dashboard."""
    row = db.query_rows(
        """
        SELECT COUNT(*)          AS total_orders,
               SUM(total_amount) AS total_revenue,
               AVG(total_amount) AS avg_order_value,
               MIN(order_date)   AS start_date,
               MAX(order_date)   AS end_date
        FROM orders
        """
    )[0]
    profit = db.query_rows(
        """
        SELECT SUM(oi.line_total)              AS revenue_items,
               SUM(oi.quantity * p.unit_cost)  AS cost
        FROM order_items oi
        JOIN products p ON p.product_id = oi.product_id
        """
    )[0]
    counts = db.query_rows(
        """
        SELECT (SELECT COUNT(*) FROM customers) AS total_customers,
               (SELECT COUNT(*) FROM products)  AS total_products,
               (SELECT COUNT(*) FROM branches)  AS total_branches
        """
    )[0]
    gross_profit = (profit["revenue_items"] or 0) - (profit["cost"] or 0)
    return {
        "total_revenue": round(row["total_revenue"] or 0, 2),
        "total_orders": row["total_orders"],
        "avg_order_value": round(row["avg_order_value"] or 0, 2),
        "gross_profit": round(gross_profit, 2),
        "gross_margin_pct": round(
            100 * gross_profit / row["total_revenue"], 1
        )
        if row["total_revenue"]
        else 0.0,
        "total_customers": counts["total_customers"],
        "total_products": counts["total_products"],
        "total_branches": counts["total_branches"],
        "start_date": row["start_date"],
        "end_date": row["end_date"],
    }


def revenue_by_month() -> list[dict]:
    return db.query_rows(
        """
        SELECT substr(order_date, 1, 7) AS month,
               SUM(total_amount)        AS revenue,
               COUNT(*)                 AS orders
        FROM orders
        GROUP BY month
        ORDER BY month
        """
    )


def revenue_by_branch() -> list[dict]:
    return db.query_rows(
        """
        SELECT b.branch_id,
               b.branch_name,
               SUM(o.total_amount) AS revenue,
               COUNT(*)            AS orders,
               AVG(o.total_amount) AS avg_order_value
        FROM orders o
        JOIN branches b ON b.branch_id = o.branch_id
        GROUP BY b.branch_id
        ORDER BY revenue DESC
        """
    )


def top_products(limit: int = 10) -> list[dict]:
    return db.query_rows(
        """
        SELECT p.product_name,
               p.category,
               SUM(oi.line_total) AS revenue,
               SUM(oi.quantity)   AS units_sold
        FROM order_items oi
        JOIN products p ON p.product_id = oi.product_id
        GROUP BY p.product_id
        ORDER BY revenue DESC
        LIMIT ?
        """,
        (int(limit),),
    )


def category_breakdown() -> list[dict]:
    return db.query_rows(
        """
        SELECT p.category,
               SUM(oi.line_total) AS revenue,
               SUM(oi.quantity)   AS units_sold
        FROM order_items oi
        JOIN products p ON p.product_id = oi.product_id
        GROUP BY p.category
        ORDER BY revenue DESC
        """
    )


def best_day() -> dict:
    return db.query_rows(
        """
        SELECT order_date        AS date,
               SUM(total_amount) AS revenue,
               COUNT(*)          AS orders
        FROM orders
        GROUP BY order_date
        ORDER BY revenue DESC
        LIMIT 1
        """
    )[0]


def daily_revenue() -> list[dict]:
    return db.query_rows(
        """
        SELECT order_date        AS date,
               SUM(total_amount) AS revenue,
               COUNT(*)          AS orders
        FROM orders
        GROUP BY order_date
        ORDER BY order_date
        """
    )


def weekend_vs_weekday() -> dict:
    row = db.query_rows(
        """
        WITH daily AS (
            SELECT order_date,
                   COUNT(*) AS orders,
                   SUM(total_amount) AS revenue,
                   CAST(strftime('%w', order_date) AS INTEGER) AS dow
            FROM orders
            GROUP BY order_date
        )
        SELECT
            AVG(CASE WHEN dow IN (5, 6) THEN orders END)  AS weekend_avg_orders,
            AVG(CASE WHEN dow NOT IN (5, 6) THEN orders END) AS weekday_avg_orders,
            AVG(CASE WHEN dow IN (5, 6) THEN revenue END) AS weekend_avg_revenue,
            AVG(CASE WHEN dow NOT IN (5, 6) THEN revenue END) AS weekday_avg_revenue
        FROM daily
        """
    )[0]
    we, wd = row["weekend_avg_orders"], row["weekday_avg_orders"]
    return {
        "weekend_avg_orders": round(we, 1),
        "weekday_avg_orders": round(wd, 1),
        "orders_ratio": round(we / wd, 2) if wd else None,
        "weekend_avg_revenue": round(row["weekend_avg_revenue"], 0),
        "weekday_avg_revenue": round(row["weekday_avg_revenue"], 0),
    }


def month_compare() -> dict:
    """Compare the two most recent months present in the data."""
    months = revenue_by_month()
    if len(months) < 2:
        return {"error": "Not enough monthly data to compare."}
    prev, curr = months[-2], months[-1]
    change = (
        100 * (curr["revenue"] - prev["revenue"]) / prev["revenue"]
        if prev["revenue"]
        else 0
    )
    return {
        "previous_month": prev["month"],
        "previous_revenue": round(prev["revenue"], 0),
        "current_month": curr["month"],
        "current_revenue": round(curr["revenue"], 0),
        "change_pct": round(change, 1),
    }


def detect_anomalies(threshold: float = 0.6) -> list[dict]:
    """Flag days whose revenue deviates sharply from the norm.

    MVP method (statistical, not ML — the ML phase comes later): compute a
    day-of-week-aware expected revenue as the median revenue for that
    weekday, then flag days deviating more than ``threshold`` (fractional).
    Being day-of-week aware means normal weekend peaks are *not* flagged,
    while the injected spikes/drops are.
    """
    df = pd.DataFrame(daily_revenue())
    if df.empty:
        return []
    df["date"] = pd.to_datetime(df["date"])
    df["dow"] = df["date"].dt.dayofweek  # pandas: Mon=0 ... Sun=6
    df["expected"] = df.groupby("dow")["revenue"].transform("median")
    df["deviation"] = (df["revenue"] - df["expected"]) / df["expected"]

    flagged = df[df["deviation"].abs() >= threshold].copy()
    flagged = flagged.sort_values("date")
    out: list[dict] = []
    for _, r in flagged.iterrows():
        dev = float(r["deviation"])
        out.append(
            {
                "date": r["date"].strftime("%Y-%m-%d"),
                "revenue": round(float(r["revenue"]), 0),
                "expected": round(float(r["expected"]), 0),
                "deviation_pct": round(dev * 100, 1),
                "direction": "spike" if dev > 0 else "drop",
                "severity": "HIGH" if abs(dev) >= 0.7 else "MEDIUM",
            }
        )
    return out
