# src/config.py
import os

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DATA_RAW_DIR = os.path.join(BASE_DIR, "..", "data", "raw")
DATA_INTERIM_DIR = os.path.join(BASE_DIR, "..", "data", "interim")
DATA_PROCESSED_DIR = os.path.join(BASE_DIR, "..", "data", "processed")

# SQLite DB file (inside data folder)
DB_PATH = os.path.join(BASE_DIR, "..", "data", "olist.db")

# Map of logical table name -> expected processed CSV filename (common names)
CSV_TABLE_MAP = {
    "orders": "orders_cleaned.csv",
    "customers": "customers_cleaned.csv",
    "order_items": "order_items_cleaned.csv",
    "products": "products_cleaned.csv",
    "sellers": "sellers_cleaned.csv",
    "payments": "payments_cleaned.csv",
    "reviews": "reviews_cleaned.csv",
    "geolocation": "geolocation_cleaned.csv",
    "order_features": "order_features.csv",
    "product_features": "product_features.csv",
    "seller_features": "seller_features.csv",
    "customer_features": "customer_features.csv",
}

