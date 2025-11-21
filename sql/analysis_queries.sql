-- Monthly Revenue
SELECT
    strftime('%Y-%m', order_purchase_timestamp) AS year_month,
    SUM(payment_value) AS revenue
FROM orders
LEFT JOIN payments USING(order_id)
GROUP BY year_month
ORDER BY year_month;

-- Monthly Orders
SELECT
    strftime('%Y-%m', order_purchase_timestamp) AS year_month,
    COUNT(DISTINCT order_id) AS total_orders
FROM orders
GROUP BY year_month
ORDER BY year_month;

-- Monthly AOV
SELECT
    strftime('%Y-%m', order_purchase_timestamp) AS year_month,
    SUM(payment_value) / COUNT(DISTINCT order_id) AS aov
FROM orders
JOIN payments USING(order_id)
GROUP BY year_month
ORDER BY year_month;

-- Top 10 Categories by Revenue
SELECT
    c.product_category_name_english AS category_name,
    SUM(p.payment_value) AS revenue
FROM order_items oi
JOIN products pr 
        ON oi.product_id = pr.product_id
JOIN payments p 
        ON oi.order_id = p.order_id
JOIN categories c 
        ON pr.product_category_name = c.product_category_name
GROUP BY c.product_category_name_english
ORDER BY revenue DESC
LIMIT 10;

-- Top 10 Sellers by Revenue
SELECT
    seller_id,
    SUM(payment_value) AS revenue,
    COUNT(order_items.order_id) AS items_sold
FROM order_items
JOIN payments USING(order_id)
GROUP BY seller_id
ORDER BY revenue DESC
LIMIT 10;

-- Delivery Performance
SELECT
    strftime('%Y-%m', order_purchase_timestamp) AS year_month,
    AVG(CASE WHEN order_delivered_customer_date <= order_estimated_delivery_date THEN 1 ELSE 0 END)
        AS on_time_rate,
    AVG(julianday(order_delivered_customer_date) - julianday(order_estimated_delivery_date))
        AS avg_delay_days
FROM orders
GROUP BY year_month
ORDER BY year_month;
