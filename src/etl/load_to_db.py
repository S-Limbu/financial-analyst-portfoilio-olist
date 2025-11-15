import pandas as pd
import sqlite3
import os
from src.config import DB_PATH

def load_all_to_db():
    conn = sqlite3.connect(DB_PATH)

    csv_files = {
        "orders": "data/processed/orders_processed.csv",
        "customers": "data/processed/customers_processed.csv",
        "order_items": "data/processed/order_items_processed.csv",
        "products": "data/processed/products_processed.csv",
        "sellers": "data/processed/sellers_processed.csv",
        "geolocation": "data/processed/geolocation_processed.csv",
        "payments": "data/processed/payments_processed.csv",
        "reviews": "data/processed/reviews_processed.csv"
    }

    for table, path in csv_files.items():
        df = pd.read_csv(path)
        df.to_sql(table, conn, if_exists="replace", index=False)
        print(f"Loaded {table} → database.")

    conn.close()

if __name__ == "__main__":
    load_all_to_db()

