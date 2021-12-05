from operator import index
import pandas as pd
import os
import sqlalchemy
import matplotlib.pyplot as plt
import argparse
import datetime

parser = argparse.ArgumentParser()
parser.add_argument('--dt_ref', help = 'Data referencia para a safra a ser predita: YYYY-MM-DD')

args = parser.parse_args()

PRED_DIR = os.path.dirname(os.path.abspath(__file__))
MODELLING_DIR = os.path.dirname(PRED_DIR)
BASE_DIR = os.path.dirname(MODELLING_DIR)
MODELS_DIR = os.path.join(BASE_DIR, 'models')
DATA_DIR = 'C:\\Users\\lucas.schiavetti\\Desktop\\olist\\data\\olist.db'

print('Importando Modelo')
model = pd.read_pickle(os.path.join(MODELS_DIR, 'model_churn.pkl'))
print('ok')


print('Abrindo conexão com banco de dados')
con = sqlalchemy.create_engine('sqlite:///'+ DATA_DIR)
print('ok')

print('Importando dados...', end='')
df = pd.read_sql_query(f"SELECT * FROM tb_book_sellers WHERE dt_ref = '{args.dt_ref}';", con)
print(df.head())
print('ok')

print('Preaparando dados para aplicar modelo...')
df_onehot = pd.DataFrame(model['onehot'].transform(df[model['cat_features']]),
                        columns=model['onehot'].get_feature_names(model['cat_features']))
print('ok')

df_full = pd.concat([df[model['num_features']], df_onehot], axis=1)[model['features_fit']]
print(df_full)
print('ok')

print('Criando score...')
df['score'] = model['modelo'].predict_proba(df_full)[:,1]
print('ok')

print('Enviando os dados para o banco de dados...')
df_score = df[['dt_ref','seller_id', 'score']].copy()
df_score['dt_atualizacao'] = datetime.datetime.now()

df_score.to_sql('tb_churn_score', con, if_exists='replace', index=False)

print('ok')