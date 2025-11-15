# src/etl/load_to_db.py
"""
Load processed CSV files into a SQLite database (data/olist.db).

This script:
 - looks for processed CSVs (see src/config.py CSV_TABLE_MAP)
 - loads each found CSV into the SQLite DB using its logical table name
"""

import os
import sqlite3
from src.config import DB_PATH, DATA_PROCESSED_DIR, CSV_TABLE_MAP
from src.utils import safe_read_csv, ensure_dir

def load_tables_to_sqlite():
    ensure_dir(os.path.dirname(DB_PATH))
    conn = sqlite3.connect(DB_PATH)
    print(f"Connected to SQLite DB at: {DB_PATH}")

    for table_name, csv_file in CSV_TABLE_MAP.items():
        csv_path = os.path.join(DATA_PROCESSED_DIR, csv_file)
        df = safe_read_csv(csv_path)
        if df is None:
            print(f"Skipping load for `{table_name}` — CSV not present: {csv_file}")
            continue

        print(f"Loading `{csv_file}` -> table `{table_name}` ({df.shape[0]} rows, {df.shape[1]} cols)")
        # try to write, if fails show error
        try:
            df.to_sql(table_name, conn, if_exists="replace", index=False)
        except Exception as e:
            print(f"ERROR writing table {table_name}: {e}")

    conn.close()
    print("Done loading tables to SQLite.")

if __name__ == "__main__":
    load_tables_to_sqlite()


