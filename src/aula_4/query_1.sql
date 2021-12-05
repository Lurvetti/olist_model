SELECT 
  '{date}' AS dt_ref,
  t1.*,
  sellers.seller_city,
  sellers.seller_state

FROM (

  SELECT 
    order_itens.seller_id,

    AVG (order_reviews.review_score) AS avg_review_score, -- media do score de reviews

    t3.idade_base AS idade_base_dias,
    1 + CAST(t3.idade_base / 30 AS INTEGER) AS idade_base_mes,
    CAST (JULIANDAY('{date}') - JULIANDAY(MAX (orders.order_approved_at)) AS INTEGER) AS qtde_dias_ult_vendas,

    COUNT (DISTINCT strftime('%m', orders.order_approved_at)) AS qtde_mes_ativacao,
    CAST(COUNT (DISTINCT strftime('%m', orders.order_approved_at)) AS FLOAT) / MIN (1 + CAST(t3.idade_base / 30 AS INTEGER), 6) AS prop_ativacao,

    SUM(CASE WHEN julianday(orders.order_estimated_delivery_date) < julianday(orders.order_delivered_customer_date) THEN 1 ELSE 0 END) / COUNT (DISTINCT order_itens.order_id) AS prop_atraso,
    CAST (AVG(julianday(orders.order_estimated_delivery_date) - julianday(orders.order_purchase_timestamp)) AS INTEGER) AS avg_tempo_entrega_est,

    SUM (order_itens.price) AS receita_total,
    SUM (order_itens.price) / COUNT (DISTINCT order_itens.order_id) AS avg_vl_venda,
    SUM (order_itens.price) / MIN (1 + CAST(t3.idade_base / 30 AS INTEGER), 6) AS avg_vl_venda_mes,
    SUM (order_itens.price) / COUNT (DISTINCT strftime('%m', orders.order_approved_at)) AS avg_vl_venda_mes_ativado,

    COUNT (DISTINCT order_itens.order_id) AS qtde_vendas,
    COUNT (order_itens.product_id) AS qtde_produto,
    COUNT (DISTINCT order_itens.product_id) AS qtde_produto_distinct,

    SUM (order_itens.price) / COUNT (order_itens.product_id) AS avg_vl_produto,

    COUNT (order_itens.product_id) / COUNT (DISTINCT order_itens.order_id) AS avg_qtde_produto_venda,

    -- Variáveis de volume de vendas por categoria de produto
    SUM (CASE WHEN product_category_name = 'cama_mesa_banho' THEN 1 ELSE 0 END ) AS qtde_cama_mesa_banho,
    SUM (CASE WHEN product_category_name = 'beleza_saude' THEN 1 ELSE 0 END ) AS qtde_beleza_saude,
    SUM (CASE WHEN product_category_name = 'esporte_lazer' THEN 1 ELSE 0 END ) AS qtde_esporte_lazer,
    SUM (CASE WHEN product_category_name = 'moveis_decoracao' THEN 1 ELSE 0 END ) AS qtde_moveis_decoracao,
    SUM (CASE WHEN product_category_name = 'informatica_acessorios' THEN 1 ELSE 0 END ) AS qtde_informatica_acessorios,
    SUM (CASE WHEN product_category_name = 'utilidades_domesticas' THEN 1 ELSE 0 END ) AS qtde_utilidades_domesticas,
    SUM (CASE WHEN product_category_name = 'relogios_presentes' THEN 1 ELSE 0 END ) AS qtde_relogios_presentes,
    SUM (CASE WHEN product_category_name = 'telefonia' THEN 1 ELSE 0 END ) AS qtde_telefonia,
    SUM (CASE WHEN product_category_name = 'ferramentas_jardim' THEN 1 ELSE 0 END ) AS qtde_ferramentas_jardim,
    SUM (CASE WHEN product_category_name = 'automotivo' THEN 1 ELSE 0 END ) AS qtde_automotivo,
    SUM (CASE WHEN product_category_name = 'brinquedos' THEN 1 ELSE 0 END ) AS qtde_brinquedos,
    SUM (CASE WHEN product_category_name = 'cool_stuff' THEN 1 ELSE 0 END ) AS qtde_cool_stuff,
    SUM (CASE WHEN product_category_name = 'perfumaria' THEN 1 ELSE 0 END ) AS qtde_perfumaria,
    SUM (CASE WHEN product_category_name = 'bebes' THEN 1 ELSE 0 END ) AS qtde_bebes,
    SUM (CASE WHEN product_category_name = 'eletronicos' THEN 1 ELSE 0 END ) AS qtde_eletronicos,
    SUM (CASE WHEN product_category_name = 'papelaria' THEN 1 ELSE 0 END ) AS qtde_papelaria,
    SUM (CASE WHEN product_category_name = 'fashion_bolsas_e_acessorios' THEN 1 ELSE 0 END ) AS qtde_fashion_bolsas_e_acessorios,
    SUM (CASE WHEN product_category_name = 'pet_shop' THEN 1 ELSE 0 END ) AS qtde_pet_shop,
    SUM (CASE WHEN product_category_name = 'moveis_escritorio' THEN 1 ELSE 0 END ) AS qtde_moveis_escritorio,
    SUM (CASE WHEN product_category_name = 'consoles_games' THEN 1 ELSE 0 END ) AS qtde_consoles_games,
    SUM (CASE WHEN product_category_name = 'malas_acessorios' THEN 1 ELSE 0 END ) AS qtde_malas_acessorios,
    SUM (CASE WHEN product_category_name = 'construcao_ferramentas_construcao' THEN 1 ELSE 0 END ) AS qtde_construcao_ferramentas_construcao,
    SUM (CASE WHEN product_category_name = 'eletrodomesticos' THEN 1 ELSE 0 END ) AS qtde_eletrodomesticos,
    SUM (CASE WHEN product_category_name = 'instrumentos_musicais' THEN 1 ELSE 0 END ) AS qtde_instrumentos_musicais,
    SUM (CASE WHEN product_category_name = 'eletroportateis' THEN 1 ELSE 0 END ) AS qtde_eletroportateis,
    SUM (CASE WHEN product_category_name = 'casa_construcao' THEN 1 ELSE 0 END ) AS qtde_casa_construcao,
    SUM (CASE WHEN product_category_name = 'livros_interesse_geral' THEN 1 ELSE 0 END ) AS qtde_livros_interesse_geral,
    SUM (CASE WHEN product_category_name = 'alimentos' THEN 1 ELSE 0 END ) AS qtde_alimentos,
    SUM (CASE WHEN product_category_name = 'moveis_sala' THEN 1 ELSE 0 END ) AS qtde_moveis_sala,
    SUM (CASE WHEN product_category_name = 'casa_conforto' THEN 1 ELSE 0 END ) AS qtde_casa_conforto,
    SUM (CASE WHEN product_category_name = 'bebidas' THEN 1 ELSE 0 END ) AS qtde_bebidas,
    SUM (CASE WHEN product_category_name = 'audio' THEN 1 ELSE 0 END ) AS qtde_audio,
    SUM (CASE WHEN product_category_name = 'market_place' THEN 1 ELSE 0 END ) AS qtde_market_place,
    SUM (CASE WHEN product_category_name = 'construcao_ferramentas_iluminacao' THEN 1 ELSE 0 END ) AS qtde_construcao_ferramentas_iluminacao,
    SUM (CASE WHEN product_category_name = 'climatizacao' THEN 1 ELSE 0 END ) AS qtde_climatizacao,
    SUM (CASE WHEN product_category_name = 'moveis_cozinha_area_de_servico_jantar_e_jardim' THEN 1 ELSE 0 END ) AS qtde_moveis_cozinha_area_de_servico_jantar_e_jardim,
    SUM (CASE WHEN product_category_name = 'alimentos_bebidas' THEN 1 ELSE 0 END ) AS qtde_alimentos_bebidas,
    SUM (CASE WHEN product_category_name = 'industria_comercio_e_negocios' THEN 1 ELSE 0 END ) AS qtde_industria_comercio_e_negocios,
    SUM (CASE WHEN product_category_name = 'livros_tecnicos' THEN 1 ELSE 0 END ) AS qtde_livros_tecnicos,
    SUM (CASE WHEN product_category_name = 'telefonia_fixa' THEN 1 ELSE 0 END ) AS qtde_telefonia_fixa,
    SUM (CASE WHEN product_category_name = 'fashion_calcados' THEN 1 ELSE 0 END ) AS qtde_fashion_calcados,
    SUM (CASE WHEN product_category_name = 'eletrodomesticos_2' THEN 1 ELSE 0 END ) AS qtde_eletrodomesticos_2,
    SUM (CASE WHEN product_category_name = 'construcao_ferramentas_jardim' THEN 1 ELSE 0 END ) AS qtde_construcao_ferramentas_jardim,
    SUM (CASE WHEN product_category_name = 'agro_industria_e_comercio' THEN 1 ELSE 0 END ) AS qtde_agro_industria_e_comercio,
    SUM (CASE WHEN product_category_name = 'artes' THEN 1 ELSE 0 END ) AS qtde_artes,
    SUM (CASE WHEN product_category_name = 'pcs' THEN 1 ELSE 0 END ) AS qtde_pcs,
    SUM (CASE WHEN product_category_name = 'sinalizacao_e_seguranca' THEN 1 ELSE 0 END ) AS qtde_sinalizacao_e_seguranca,
    SUM (CASE WHEN product_category_name = 'construcao_ferramentas_seguranca' THEN 1 ELSE 0 END ) AS qtde_construcao_ferramentas_seguranca,
    SUM (CASE WHEN product_category_name = 'artigos_de_natal' THEN 1 ELSE 0 END ) AS qtde_artigos_de_natal

  FROM tb_orders AS orders

  LEFT JOIN tb_order_items AS order_itens
    ON orders.order_id = order_itens.order_id

  LEFT JOIN (
    SELECT 
        order_itens.seller_id,
        MAX(julianday('{date}') - julianday(orders.order_approved_at)) AS idade_base
    FROM tb_orders AS orders
    LEFT JOIN tb_order_items AS order_itens
      ON orders.order_id = order_itens.order_id
    WHERE 
      orders.order_approved_at < '{date}'
      AND orders.order_status = 'delivered'
    GROUP BY order_itens.seller_id
  ) AS t3 ON order_itens.seller_id = t3.seller_id


  LEFT JOIN tb_products AS products
    ON order_itens.product_id = products.product_id

  LEFT JOIN tb_order_reviews AS order_reviews
    ON order_itens.order_id = order_reviews.order_id

  WHERE 
    orders.order_approved_at BETWEEN date('{date}', '-6 months') AND '{date}'
    AND orders.order_status = 'delivered'

  GROUP BY order_itens.seller_id
) AS t1

LEFT JOIN tb_sellers AS sellers
  ON t1.seller_id = sellers.seller_id

ORDER BY qtde_vendas DESC
;