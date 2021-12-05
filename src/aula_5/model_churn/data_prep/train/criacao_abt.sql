DROP TABLE IF EXISTS tb_abt_churn;

CREATE TABLE tb_abt_churn AS

    SELECT
        t2.*,
        t1.flag_churn
        
    FROM (
        SELECT 
            t1.dt_ref,
            t1.seller_id,
            MIN (COALESCE(t2.venda,1)) AS flag_churn
            
        FROM tb_book_sellers AS t1

        LEFT JOIN (
            SELECT
                strftime('%Y-%m', t1.order_approved_at) || "-01" AS dt_venda,
                t2.seller_id,
                max(0) AS venda
            FROM tb_orders AS t1

            LEFT JOIN tb_order_items AS t2
                ON t1.order_id = t2.order_id

            WHERE order_approved_at IS NOT NULL
            AND seller_id IS NOT NULL
            AND t1.order_status = 'delivered'

            GROUP BY strftime('%Y-%m', t1.order_approved_at) || "-01", t2.seller_id
            ORDER BY t2.seller_id, strftime('%Y-%m', t1.order_approved_at) || "-01"
        ) AS t2 
        ON t1.seller_id = t2.seller_id
        AND t2.dt_venda BETWEEN t1.dt_ref AND DATE (t1.dt_ref, '+2 months')

        GROUP BY t1.dt_ref,t1.seller_id

        ORDER BY dt_ref
    ) AS t1

    LEFT JOIN tb_book_sellers AS t2
        ON t1.seller_id = t2.seller_id
        AND t1.dt_ref = t2.dt_ref
;