# Olist E-commerce Analytics — Portfolio Project

This repository contains an end-to-end data analytics portfolio project using the Brazilian Olist dataset.
It includes data cleaning (Jupyter), ETL (Python + SQLite), SQL modeling, analytic marts and a Tableau executive dashboard.

## Repo structure

olist-portfolio/
├─ data/
│ ├─ raw/
│ ├─ interim/
│ └─ processed/
├─ notebooks/
│ ├─ 01_data_overview.ipynb
│ ├─ 02_cleaning.ipynb
│ ├─ 03_feature_engineering.ipynb
│ ├─ 04_eda_financials.ipynb
│ ├─ 05_sql_etl.ipynb
│ └─ 06_tableau_prep.ipynb
├─ src/
│ ├─ etl/
│ │ ├─ load_to_db.py
│ │ └─ build_marts.py
│ ├─ utils.py
│ └─ config.py
├─ sql/
│ ├─ schema.sql
│ ├─ etl.sql
│ └─ analysis_queries.sql
├─ dashboards/
│ └─ tableau_design.md
└─ README.md
