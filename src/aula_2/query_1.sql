SELECT 
  order_itens.seller_id,

  t3.idade_base AS idade_base_dias,
  1 + CAST(t3.idade_base / 30 AS INTEGER) AS idade_base_mes,

  COUNT (DISTINCT strftime('%m', orders.order_approved_at)) AS qtde_mes_ativacao,
  CAST(COUNT (DISTINCT strftime('%m', orders.order_approved_at)) AS FLOAT) / MIN (1 + CAST(t3.idade_base / 30 AS INTEGER), 6) AS prop_ativacao,

  SUM (order_itens.price) AS receita_total,
  SUM (order_itens.price) / COUNT (DISTINCT order_itens.order_id) AS avg_vl_venda,
  SUM (order_itens.price) / MIN (1 + CAST(t3.idade_base / 30 AS INTEGER), 6) AS avg_vl_venda_mes,
  SUM (order_itens.price) / COUNT (DISTINCT strftime('%m', orders.order_approved_at)) AS avg_vl_venda_mes_ativado,

  COUNT (DISTINCT order_itens.order_id) AS qtde_vendas,
  COUNT (order_itens.product_id) AS qtde_produto,
  COUNT (DISTINCT order_itens.product_id) AS qtde_produto_distinct,

  SUM (order_itens.price) / COUNT (order_itens.product_id) AS avg_vl_produto,

  COUNT (order_itens.product_id) / COUNT (DISTINCT order_itens.order_id) AS avg_qtde_produto_venda

FROM tb_orders AS orders

LEFT JOIN tb_order_items AS order_itens
  ON orders.order_id = order_itens.order_id

LEFT JOIN (
  SELECT 
      order_itens.seller_id,
      MAX(julianday('2017-04-01') - julianday(orders.order_approved_at)) AS idade_base
  FROM tb_orders AS orders
  LEFT JOIN tb_order_items AS order_itens
    ON orders.order_id = order_itens.order_id
  WHERE 
    orders.order_approved_at < '2017-04-01'
    AND orders.order_status = 'delivered'
  GROUP BY order_itens.seller_id
) AS t3 ON order_itens.seller_id = t3.seller_id


WHERE 
  orders.order_approved_at BETWEEN '2016-10-01' AND '2017-04-01'
  AND orders.order_status = 'delivered'

GROUP BY order_itens.seller_id
--LIMIT 100
;



/*
SELECT * FROM tb_order_items LIMIT 100;



/*ALTER TABLE olist_customers_dataset
  RENAME TO tb_costumers;

ALTER TABLE olist_geolocation_dataset
  RENAME TO tb_geolocation;

ALTER TABLE olist_order_items_dataset
  RENAME TO tb_order_items;

ALTER TABLE olist_order_payments_dataset
  RENAME TO tb_order_payments;

ALTER TABLE olist_order_reviews_dataset
  RENAME TO tb_order_reviews;

ALTER TABLE olist_orders_dataset
  RENAME TO tb_orders;

ALTER TABLE olist_products_dataset
  RENAME TO tb_products;

ALTER TABLE olist_sellers_dataset
  RENAME TO tb_sellers;

ALTER TABLE product_category_name_translation
  RENAME TO tb_product_category_name_translation;
*/