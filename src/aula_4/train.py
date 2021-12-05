import pandas as pd
import sqlalchemy
import os

from sklearn import tree
from sklearn import metrics

# para o jupyter
EP_DIR = os.path.join(os.path.abspath('.'), 'src', 'aula_4')
EP_DIR = os.path.dirname(os.path.abspath(__file__))

SRC_DIR = os.path.dirname(EP_DIR)
BASE_DIR = os.path.dirname(SRC_DIR)
DATA_DIR = os.path.join(BASE_DIR, 'data')

print(EP_DIR)

def import_query (path, **kwards):
    with open(path, 'r', **kwards) as file_open:
        result = file_open.read()
    return result

def connect_db():
    return sqlalchemy.create_engine('sqlite:///' + os.path.join(DATA_DIR, 'olist.db'))

query = import_query(os.path.join(EP_DIR, 'create_safra.sql'))
con = connect_db()

#print(query)
#print(con.table_names())

# o dado é nosso
df = pd.read_sql(query, con)
columns = df.columns.tolist()

# variáveis para serem removidas
to_remove = ['seller_id', 'seller_city']

# variável alvo, resposta, targe
target = 'flag_model'

# remove variáveis
for i in to_remove + [target]:
    columns.remove(i)

# define tipos de variávies
cat_features = df[columns].dtypes[df[columns].dtypes == 'object'].index.tolist()
num_features = list(set(columns) - set(cat_features))


# treinando o algoritmo de teste de decisão -- ainda mal, apenas uma safra e predizendo o próprio dataset de treinamento
clf = tree.DecisionTreeClassifier(max_depth=10)
clf.fit(df[num_features], df[target])

y_pred = clf.predict(df[num_features])
y_prob = clf.predict_proba(df[num_features])

print(metrics.confusion_matrix(df[target], y_pred))

feature_importance = pd.Series(clf.feature_importances_, index=num_features)
print(feature_importance.sort_values(ascending=False))
