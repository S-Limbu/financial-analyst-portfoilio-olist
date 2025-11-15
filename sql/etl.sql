DROP TABLE IF EXISTS mart_monthly_revenue;
CREATE TABLE mart_monthly_revenue AS
SELECT
    strftime('%Y-%m', order_purchase_timestamp) AS year_month,
    SUM(payment_value) AS revenue,
    COUNT(DISTINCT order_id) AS orders
FROM orders
JOIN payments USING(order_id)
GROUP BY 1;

