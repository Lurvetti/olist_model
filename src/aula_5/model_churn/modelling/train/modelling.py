import pandas as pd
import os
import sqlalchemy

TRAIN_DIR = os.path.dirname(os.path.abspath(__file__))
MODELLING_DIR = os.path.dirname(TRAIN_DIR)
BASE_DIR = os.path.dirname(MODELLING_DIR)
DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(BASE_DIR))), 'data')

engine = sqlalchemy.create_engine('sqlite:///' + os.path.join(DATA_DIR, 'olist.db'))

abt = pd.read_sql_table('tb_abt_churn', engine)