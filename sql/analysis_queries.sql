-- sql/analysis_queries.sql
-- Useful queries for analysis / Tableau / validation

-- 1) Monthly GMV
SELECT year_month, revenue FROM mart_monthly_revenue ORDER BY year_month;

-- 2) AOV per month
SELECT
    year_month,
    revenue / NULLIF(orders,0) AS aov
FROM mart_monthly_revenue
ORDER BY year_month;

-- 3) Top 10 categories by revenue
SELECT product_category_name, SUM(oi.price) AS revenue
FROM order_items oi
LEFT JOIN products p ON oi.product_id = p.product_id
LEFT JOIN payments pay ON oi.order_id = pay.order_id
GROUP BY product_category_name
ORDER BY revenue DESC
LIMIT 10;

-- 4) Top 10 sellers by revenue
SELECT seller_id, SUM(price) AS revenue
FROM order_items
GROUP BY seller_id
ORDER BY revenue DESC
LIMIT 10;

-- 5) On-time delivery rate
SELECT
    SUM(CASE WHEN order_delivered_customer_date <= order_estimated_delivery_date THEN 1 ELSE 0 END) * 1.0
    / COUNT(*) AS on_time_rate
FROM orders
WHERE order_delivered_customer_date IS NOT NULL
AND order_estimated_delivery_date IS NOT NULL;

