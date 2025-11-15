import sqlite3
import pandas as pd
from src.config import DB_PATH

def create_marts():
    conn = sqlite3.connect(DB_PATH)

    queries = {
        "monthly_revenue": """
            SELECT
                strftime('%Y-%m', order_purchase_timestamp) AS year_month,
                SUM(payment_value) AS revenue,
                COUNT(DISTINCT order_id) AS orders,
                SUM(payment_value) / COUNT(DISTINCT order_id) AS aov
            FROM orders
            JOIN payments USING(order_id)
            GROUP BY 1
            ORDER BY 1;
        """,
        "seller_performance": """
            SELECT
                seller_id,
                SUM(payment_value) AS total_revenue,
                COUNT(order_id) AS total_orders,
                AVG(review_score) AS avg_review_score
            FROM order_items
            JOIN payments USING(order_id)
            JOIN reviews USING(order_id)
            GROUP BY seller_id
            ORDER BY total_revenue DESC;
        """,
        "delivery_performance": """
            SELECT
                order_id,
                delivered_customer_date,
                estimated_delivery_date,
                julianday(delivered_customer_date) - julianday(estimated_delivery_date)
                    AS delay_days,
                CASE WHEN delivered_customer_date <= estimated_delivery_date
                    THEN 1 ELSE 0 END AS delivered_on_time
            FROM orders;
        """
    }

    for name, query in queries.items():
        df = pd.read_sql_query(query, conn)
        df.to_csv(f"data/processed/{name}.csv", index=False)
        print(f"Created mart: {name}")

    conn.close()

if __name__ == "__main__":
    create_marts()

