
SELECT
    t1.*,
    CASE WHEN t2.seller_id IS NOT NULL THEN 1 ELSE 0 END AS flag_model
FROM tb_book_sellers AS t1

LEFT JOIN (
    --treês meses
    SELECT
        DISTINCT t2.seller_id
    FROM tb_orders AS t1

    LEFT JOIN tb_order_items AS t2
        ON t1.order_id = t2.order_id


    WHERE t1.order_approved_at BETWEEN '2017-04-01' AND '2017-07-01' --Y de três meses adiante
    AND t1.order_status = 'delivered'
) AS t2 
ON t1.seller_id = t2.seller_id