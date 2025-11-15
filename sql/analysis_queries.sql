-- Top 10 categories by revenue
SELECT product_category_name, SUM(payment_value) AS revenue
FROM order_items
JOIN products USING(product_id)
JOIN payments USING(order_id)
GROUP BY 1
ORDER BY revenue DESC
LIMIT 10;

