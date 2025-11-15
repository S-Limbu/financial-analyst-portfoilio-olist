-- sql/etl.sql
-- SQL version of transformations (run inside SQLite or a SQL client).
-- NOTE: adapt column names if your processed CSVs have slightly different names.

-- Example: create monthly revenue mart
DROP TABLE IF EXISTS mart_monthly_revenue;
CREATE TABLE mart_monthly_revenue AS
SELECT
    strftime('%Y-%m', o.order_purchase_timestamp) AS year_month,
    SUM(p.payment_value) AS revenue,
    COUNT(DISTINCT o.order_id) AS orders,
    (SUM(p.payment_value) * 1.0) / NULLIF(COUNT(DISTINCT o.order_id), 0) AS aov
FROM orders o
LEFT JOIN payments p ON o.order_id = p.order_id
GROUP BY 1;

-- Product performance
DROP TABLE IF EXISTS mart_product_performance;
CREATE TABLE mart_product_performance AS
SELECT
    oi.product_id,
    pr.product_category_name,
    COUNT(DISTINCT oi.order_id) AS orders_count,
    SUM(oi.price) AS revenue,
    AVG(oi.price) AS avg_price
FROM order_items oi
LEFT JOIN products pr ON oi.product_id = pr.product_id
GROUP BY oi.product_id, pr.product_category_name;

-- Seller performance
DROP TABLE IF EXISTS mart_seller_performance;
CREATE TABLE mart_seller_performance AS
SELECT
    oi.seller_id,
    COUNT(DISTINCT oi.order_id) AS orders_count,
    SUM(oi.price) AS revenue
FROM order_items oi
GROUP BY oi.seller_id;
