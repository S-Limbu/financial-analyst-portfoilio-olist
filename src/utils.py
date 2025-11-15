# src/utils.py
import os
import pandas as pd

def safe_read_csv(path, **kwargs):
    """Read CSV with a helpful message; returns None if not found."""
    if not os.path.exists(path):
        print(f"  - file not found: {path}")
        return None
    return pd.read_csv(path, **kwargs)

def ensure_dir(path):
    os.makedirs(path, exist_ok=True)

