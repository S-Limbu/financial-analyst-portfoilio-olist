# src/etl/build_marts.py
"""
Build analytics-ready marts (CSV + tables) from raw tables in SQLite.
Creates CSVs in data/processed/ for Tableau consumption and creates
mart_* tables back into the SQLite DB.

Requires that load_to_db.py has been run first so base tables exist.
"""

import os
import sqlite3
import pandas as pd
from src.config import DB_PATH, DATA_PROCESSED_DIR
from src.utils import ensure_dir

ensure_dir(DATA_PROCESSED_DIR)

MART_QUERIES = {
    # Monthly revenue mart (order-level aggregations)
    "mart_monthly_revenue": """
        SELECT
            strftime('%Y-%m', o.order_purchase_timestamp) AS year_month,
            SUM(p.payment_value) AS revenue,
            COUNT(DISTINCT o.order_id) AS orders,
            (SUM(p.payment_value) * 1.0) / NULLIF(COUNT(DISTINCT o.order_id),0) AS aov
        FROM orders o
        LEFT JOIN payments p ON o.order_id = p.order_id
        GROUP BY 1
        ORDER BY 1;
    """,

    # Product-level revenue and sales counts
    "mart_product_performance": """
        SELECT
            oi.product_id,
            pr.product_category_name,
            COUNT(DISTINCT oi.order_id) AS orders_count,
            SUM(oi.price) AS revenue,
            AVG(oi.price) AS avg_price
        FROM order_items oi
        LEFT JOIN products pr ON oi.product_id = pr.product_id
        GROUP BY 1,2
        ORDER BY revenue DESC;
    """,

    # Seller-level performance
    "mart_seller_performance": """
        SELECT
            oi.seller_id,
            COUNT(DISTINCT oi.order_id) AS orders_count,
            SUM(oi.price) AS revenue,
            AVG(r.review_score) AS avg_review_score
        FROM order_items oi
        LEFT JOIN reviews r ON oi.order_id = r.order_id
        GROUP BY oi.seller_id
        ORDER BY revenue DESC;
    """,

    # Customer-level features summary
    "mart_customer_summary": """
        SELECT
            o.customer_id,
            COUNT(DISTINCT o.order_id) AS num_orders,
            SUM(p.payment_value) AS total_spent,
            MIN(o.order_purchase_timestamp) AS first_order_date,
            MAX(o.order_purchase_timestamp) AS last_order_date
        FROM orders o
        LEFT JOIN payments p ON o.order_id = p.order_id
        GROUP BY o.customer_id;
    """,

    # Delivery performance at order-level
    "mart_delivery": """
        SELECT
            o.order_id,
            o.order_purchase_timestamp,
            o.order_estimated_delivery_date,
            o.order_delivered_customer_date,
            (julianday(o.order_delivered_customer_date) - julianday(o.order_estimated_delivery_date)) AS delay_days,
            CASE
                WHEN o.order_delivered_customer_date IS NULL THEN NULL
                WHEN o.order_delivered_customer_date <= o.order_estimated_delivery_date THEN 1
                ELSE 0
            END AS delivered_on_time
        FROM orders o;
    """
}


def build_marts():
    if not os.path.exists(DB_PATH):
        raise FileNotFoundError(f"SQLite DB not found at {DB_PATH}. Run load_to_db.py first.")

    conn = sqlite3.connect(DB_PATH)
    for name, query in MART_QUERIES.items():
        print(f"Building mart: {name} ...")
        try:
            df = pd.read_sql_query(query, conn)
        except Exception as e:
            print(f"  ERROR running query for {name}: {e}")
            continue

        out_csv = os.path.join(DATA_PROCESSED_DIR, f"{name}.csv")
        df.to_csv(out_csv, index=False)
        print(f"  Saved CSV: {out_csv} ({df.shape[0]} rows)")

        # Also write back to DB as a mart_* table
        try:
            df.to_sql(name, conn, if_exists="replace", index=False)
            print(f"  Written table `{name}` into SQLite.")
        except Exception as e:
            print(f"  ERROR writing mart table {name}: {e}")

    conn.close()
    print("All marts built.")


if __name__ == "__main__":
    build_marts()


