import pandas as pd
import sqlalchemy

DBPATH =  'C:\\Users\\lucas.schiavetti\\Desktop\\olist\\data\\olist.db'
con = sqlalchemy.create_engine('sqlite:///' + DBPATH)

def churn_score (seller_id):
    df = pd.read_sql_query (f"SELECT score FROM tb_churn_score WHERE seller_id = '{seller_id}' ", con)
    return df['score'][0]

#print(churn_score('6560211a19b47992c3666cc44a7e94c0'))
