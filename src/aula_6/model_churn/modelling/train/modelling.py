import pandas as pd
import os
import sqlalchemy

from sklearn import model_selection
from sklearn import tree
from sklearn import metrics

# interativo
#TRAIN_DIR = os.path.join(os.path.abspath('.'), 'src', 'ep06','model_churn','modelling','train')

TRAIN_DIR = os.path.dirname(os.path.abspath(__file__))
MODELLING_DIR = os.path.dirname(TRAIN_DIR)
BASE_DIR = os.path.dirname(MODELLING_DIR)
DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(BASE_DIR))), 'data')

engine = sqlalchemy.create_engine('sqlite:///' + os.path.join(DATA_DIR, 'olist.db'))

abt = pd.read_sql_table('tb_abt_churn', engine)
df_oot = abt[abt['dt_ref'] == abt['dt_ref'].max()].copy() # filtrando base out of time
df_abt = abt[abt['dt_ref'] < abt['dt_ref'].max()].copy() # filtrando a base abt

print(df_oot.shape)
print(df_abt.shape)

# definindo variáveis
target = 'flag_churn'
to_remove = ['dt_ref', 'seller_city', 'seller_state', 'seller_id', target]
features = df_abt.columns.tolist()
for f in to_remove:
    features.remove(f)

# separando entre treino e teste

X = df_abt[features]
y = df_abt[target]

X_train, X_test, y_train, y_test = model_selection.train_test_split(X, y, test_size = 0.20, random_state=1992)

# treinamdo modelo
clf = tree.DecisionTreeClassifier(min_samples_leaf=100)
clf.fit(X_train, y_train)

y_train_pred = clf.predict(X_train)
y_train_prob = clf.predict_proba(X_train)
print('\nAcuracia Treino: ', metrics.accuracy_score(y_train, y_train_pred))
print('AUC Treino: ', metrics.roc_auc_score(y_train, y_train_prob[:,1]))

y_test_pred = clf.predict(X_test)
y_test_prob = clf.predict_proba(X_test)
print('\nAcuracia Teste: ', metrics.accuracy_score(y_test, y_test_pred))
print('AUC Teste: ', metrics.roc_auc_score(y_test, y_test_prob[:,1]))

y_oot_pred = clf.predict(df_oot[features])
y_oot_prob = clf.predict_proba(df_oot[features])
print('\nAcuracia Out of Time: ', metrics.accuracy_score(df_oot[target], y_oot_pred))
print('AUC Out of Time: ', metrics.roc_auc_score(df_oot[target], y_oot_prob[:,1]))