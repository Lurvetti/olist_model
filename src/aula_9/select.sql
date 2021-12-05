SELECT
    dt_ref,
    COUNT(*)
from tb_book_sellers
GROUP BY dt_ref
;