import pandas as pd
import os
import sqlalchemy
import matplotlib.pyplot as plt


from sklearn import model_selection
from sklearn import tree
from sklearn import ensemble
from sklearn import metrics
from sklearn import preprocessing

# interativo
# TRAIN_DIR = os.path.join(os.path.abspath('.'), 'src', 'ep06','model_churn','modelling','train')

TRAIN_DIR = os.path.dirname(os.path.abspath(__file__))
MODELLING_DIR = os.path.dirname(TRAIN_DIR)
BASE_DIR = os.path.dirname(MODELLING_DIR)
DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(BASE_DIR))), 'data')
MODEL_DIR = os.path.join(BASE_DIR, 'models')

engine = sqlalchemy.create_engine('sqlite:///' + os.path.join(DATA_DIR, 'olist.db'))

abt = pd.read_sql_table('tb_abt_churn', engine)
df_oot = abt[abt['dt_ref'] == abt['dt_ref'].max()].copy() # filtrando base out of time
df_oot.reset_index(drop=True,inplace=True)

df_abt = abt[abt['dt_ref'] < abt['dt_ref'].max()].copy() # filtrando a base abt

#print(df_oot.shape)
#print(df_abt.shape)

# definindo variáveis
target = 'flag_churn' # Variável resposta!
to_remove = ['dt_ref', 'seller_city', 'seller_id', target]
features = df_abt.columns.tolist()
for f in to_remove:
    features.remove(f)

cat_features = df_abt[features].dtypes[df_abt[features].dtypes == 'object'].index.tolist()
num_features = list(set(features) - set(cat_features))

# separando entre treino e teste
X = df_abt[features] # matriz de features ou variáveis
y = df_abt[target] # vetor da resposta target 

# separa treino e validação
X_train, X_test, y_train, y_test = model_selection.train_test_split(X, y, test_size = 0.20, random_state=1992)

X_train.reset_index(drop=True,inplace=True)
X_test.reset_index(drop=True,inplace=True)

onehot = preprocessing.OneHotEncoder(sparse=False, handle_unknown='ignore')
onehot.fit(X_train[cat_features]) # treinou o onehot

# retorna o dado transformado em um dataframe
onehot_df = pd.DataFrame (onehot.transform(X_train[cat_features]), columns=onehot.get_feature_names(cat_features))
df_train = pd.concat([X_train[num_features], onehot_df], axis=1)
features_fit = df_train.columns.tolist()

# Modelos
clf = tree.DecisionTreeClassifier(min_samples_leaf=100)
clf.fit(df_train[features_fit], y_train)

rf = ensemble.RandomForestClassifier(n_estimators=500, min_samples_leaf=150)
rf.fit(df_train[features_fit], y_train)


# Importancia das variaveis
print('\nImportância das Variáveis\n',pd.Series(clf.feature_importances_, index=df_train.columns).sort_values(ascending=False)[:10])


# ----- analise na base de TREINO -----
y_train_pred = clf.predict(df_train)
y_train_proba = clf.predict_proba(df_train)
y_train_pred = rf.predict(df_train)
y_train_proba_rf = rf.predict_proba(df_train)

# fazendo o gráfco da Curva ROC
acc_train = metrics.accuracy_score (y_train, y_train_pred)
# print('\nBase Treino Acurácia:', acc_train)
roc_train = metrics.roc_curve (y_train, y_train_proba[:,1])
auc_train = metrics.roc_auc_score (y_train, y_train_proba[:,1])

roc_train_rf = metrics.roc_curve (y_train, y_train_proba_rf[:,1])
auc_train_rf = metrics.roc_auc_score (y_train, y_train_proba_rf[:,1])

print('Base Treino AUC - clf: ', auc_train)
print('Base Treino AUC - rf: ', auc_train_rf)




# # ----- analise na base de TESTE -----
onehot_df_test = pd.DataFrame(onehot.transform( X_test[cat_features]),
                                                columns=onehot.get_feature_names(cat_features)) 
df_predict = pd.concat([X_test[num_features], onehot_df_test], axis=1)

# predições da base teste
y_test_pred = clf.predict(df_predict)
y_test_proba = clf.predict_proba(df_predict)
y_test_pred_rf = rf.predict(df_predict)
y_test_proba_rf = rf.predict_proba(df_predict)

# fazendo o gráfco da curva roc
acc_teste = metrics.accuracy_score(y_test, y_test_pred)
# print('\nBase Teste Acurácia:', acc_teste)

roc_test = metrics.roc_curve (y_test, y_test_proba[:,1])
auc_teste = metrics.roc_auc_score (y_test, y_test_proba[:,1])

roc_test_rf = metrics.roc_curve (y_test, y_test_proba_rf[:,1])
auc_teste_rf = metrics.roc_auc_score (y_test, y_test_proba_rf[:,1])

print('Base Teste AUC - clf: ', auc_teste)
print('Base Teste AUC - rf: ', auc_teste_rf)


# ----- Analise na base OUT OF TIME -----
onehot_df_oot = pd.DataFrame(onehot.transform( df_oot[cat_features]),
                                                columns=onehot.get_feature_names(cat_features)) 
df_oot_predict = pd.concat([df_oot[num_features], onehot_df_oot], axis=1)

# predições da base oot
oot_pred = clf.predict(df_oot_predict)
oot_proba = clf.predict_proba(df_oot_predict)
oot_pred_rf = rf.predict(df_oot_predict)
oot_proba_rf = rf.predict_proba(df_oot_predict)

# fazendo o gráfco da curva roc
acc_oot = metrics.accuracy_score(df_oot[target], oot_pred)
# print('\nBase Out of Time Acurácia:', acc_oot)
roc_oot = metrics.roc_curve (df_oot[target], oot_proba[:,1])
auc_oot = metrics.roc_auc_score (df_oot[target], oot_proba[:,1])

roc_oot_rf = metrics.roc_curve (df_oot[target], oot_proba_rf[:,1])
auc_oot_rf = metrics.roc_auc_score (df_oot[target], oot_proba_rf[:,1])

print('Base Out of Time AUC - clf: ', auc_oot)
print('Base Out of Time AUC - rf: ', auc_oot_rf)


# plot curvas ROC - CLF
plt.plot(roc_train[0], roc_train[1])
plt.plot(roc_test[0], roc_test[1])
plt.plot(roc_oot[0], roc_oot[1])
plt.title('Curva ROC - CLF')
plt.xlabel('1 - Especificidade')
plt.ylabel('Sensibilidade/Recall')
plt.legend([f'Treino: {auc_train}', f'Teste: {auc_teste}', f'OOT: {auc_oot}'])
plt.show()

# plot curvas ROC - CLF
plt.plot(roc_train_rf[0], roc_train_rf[1])
plt.plot(roc_test_rf[0], roc_test_rf[1])
plt.plot(roc_oot_rf[0], roc_oot_rf[1])
plt.title('Curva ROC - RF')
plt.xlabel('1 - Especificidade')
plt.ylabel('Sensibilidade/Recall')
plt.legend([f'Treino: {auc_train_rf}', f'Teste: {auc_teste_rf}', f'OOT: {auc_oot_rf}'])
plt.show()
















# Fazendo o predict na ABT
df_abt_onehot = pd.DataFrame( onehot.transform(abt[cat_features]),
                              columns = onehot.get_feature_names(cat_features))

df_abt_predict = pd.concat([abt[num_features], df_abt_onehot], axis=1)

probs = clf.predict_proba(df_abt_predict)

abt['score_churn'] = clf.predict_proba(df_abt_predict)[:,1]
print('\n',abt.head())
abt_score = abt[['dt_ref','seller_id', 'score_churn']]
#abt_score.to_sql('tb_churn_score', engine, index=False, if_exists='replace')



# Salvando o Modelo
model_data = pd.Series ({
    'num_features' : num_features,
    'cat_features' : cat_features,
    'onehot' : onehot,
    'features_fit': features_fit,
    'modelo' : rf,
    'auc_train': auc_train_rf,
    'auc_teste': auc_teste_rf,
    'auc_oot': auc_oot_rf,
    'cutoff': 0.7
})
model_data.to_pickle(os.path.join(MODEL_DIR, 'rf.pkl'))
print(model_data)

















'''
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
'''