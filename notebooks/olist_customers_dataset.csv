# Customer Dataset Cleaning & Preprocessing

**Dataset:** `olist_customers_dataset.csv`  
**Objective:** Prepare the customers dataset for analysis and reporting by:

- Removing duplicates
- Handling missing values
- Standardizing column names & data types
- Exporting a cleaned dataset to `/data/cleaned/`

import pandas as pd

# Display settings for clarity
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', 5)
# Load raw dataset

raw_path = "../data/raw/olist_customers_dataset.csv"
customers = pd.read_csv(raw_path)

# Quick check
customers.info()
customers.head()

### Initial Observations
- Check for:
  - Missing values
  - Duplicate rows
  - Correct data types

# Check for missing values
print(customers.isnull().sum())

# Check for duplicates
print(f"Duplicate rows: {customers.duplicated().sum()}")

# Drop duplicates if any
customers.drop_duplicates(inplace=True)

# Standardize column names for clarity
customers.columns = [col.lower() for col in customers.columns]

# Optional: Ensure customer_id is string type
customers['customer_id'] = customers['customer_id'].astype(str)
customers['customer_unique_id'] = customers['customer_unique_id'].astype(str)
customers['customer_zip_code_prefix'] = customers['customer_zip_code_prefix'].astype(str)

# Verify cleaning
customers.info()
customers.head()

clean_path = "../data/cleaned/olist_customers_dataset_cleaned.csv"
customers.to_csv(clean_path, index=False)
print(f"Cleaned dataset saved to: {clean_path}")
