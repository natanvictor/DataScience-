# -*- coding: utf-8 -*-
"""ProjetoRegressãoPIBICipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1f8heLY4K54zboPGBPYuInaQxsHHkjYK3

# 1 Leitura dos dados
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
pd.set_option('display.max_columns', None)

url = '/content/drive/MyDrive/Ciência de dados /PESQUISA PIBIC/df_pesquisa.csv'
df = pd.read_csv(url)
df.head(10)

"""# 2 Preparação dos dados"""

df.shape

df.info()

df.describe()

df.duplicated().sum()

from sklearn.utils import shuffle
df_modi = shuffle(df, random_state=42)
df_modi =  df_modi.reset_index(drop=True)
df_modi.head(15)

df_filtrado = df_modi.dropna(subset=['Offline Penicillin concentration(P_offline:P(g L^{-1}))'])

df_filtrado

df_filtrado = df_filtrado.reset_index(drop=False)

df_filtrado = df_filtrado.iloc[:, 1:]

df_filtrado

df_filtrado.shape

df_filtrado.isnull().sum()

"""# 3 EDA (Análise Exploratória de Dados):"""

fig = plt.figure(figsize = (15, 40))
ax = fig.gca()
df_filtrado.hist(ax=ax)

numeric_vars = df_filtrado.select_dtypes(include=['int64', 'float64']).columns
for var in numeric_vars:
    plt.figure(figsize=(8, 5))
    sns.kdeplot(df_filtrado[var], fill=True, color='blue')
    plt.title(f'Distribuição da variável: {var}')
    plt.show()

"""#4 features selection"""

x1 = df_filtrado.drop('Penicillin concentration(P:g/L)', axis=1)
y=df_filtrado['Penicillin concentration(P:g/L)']

from sklearn.linear_model import Ridge
model = Ridge()

from sklearn.feature_selection import RFE
rfe = RFE(estimator=model, n_features_to_select=8)
fit = rfe.fit(x1,y)


print("Características selecionadas:", fit.support_)
print("Ranking das características:", fit.ranking_)

cols = fit.get_support(indices = True)
print(cols)

x = df_filtrado.iloc[:, cols]

from sklearn.preprocessing import MinMaxScaler


scaler = MinMaxScaler()
X_normalized = scaler.fit_transform(x)
x_norm = pd.DataFrame(X_normalized, columns=x.columns)


print("Dados escalados (MinMaxScaler):")
print(x_norm)

"""# 5 Tratamento de Outilers

# 6 Divisão dos dados
"""

from sklearn.model_selection import train_test_split

x_train, x_test, y_train, y_test = train_test_split(x_norm, y, test_size=0.2, random_state = 42)

from sklearn.metrics import mean_squared_error, r2_score

"""# 7 Treinamento dos modelos

Modelos escolhidos para regressão linear:

A) Ridge:
"""

from sklearn.linear_model import Ridge

ridge_model = Ridge(alpha = 1)
ridge_model.fit(x_train, y_train)

y_pred1 = ridge_model.predict(x_test)

r2_1 = round(r2_score(y_test, y_pred1), 4)
print(r2_1)

"""B) Lasso:"""

from sklearn.linear_model import Lasso

lasso_model = Lasso()

lasso_model.fit(x_train, y_train)

y_pred2 = lasso_model.predict(x_test)
r2_2 = round(r2_score(y_test, y_pred2), 4)

print(r2_2)

"""C) ElasticNet:"""

from sklearn.linear_model import ElasticNet

elastic_model = ElasticNet()
elastic_model.fit(x_train, y_train)
y_pred3 = elastic_model.predict(x_test)
r2_3 = round(r2_score(y_test, y_pred3), 4)
print(r2_3)

"""D) Gradiente Boosting Regression:"""

from sklearn.ensemble import GradientBoostingRegressor

gradien_model = GradientBoostingRegressor(n_estimators = 100, learning_rate = 0.1, max_depth = 3, random_state = 42)
gradien_model.fit(x_train, y_train)
y_pred4 = gradien_model.predict(x_test)

r2_4 = round(r2_score(y_test, y_pred4), 4)
print(r2_4)

y_pred_train = gradien_model.predict(x_train)
r2_8 = round(r2_score(y_train, y_pred_train), 4)
print(r2_8)

"""# 8 Validação Cruzada e Ajuste Fino

"""

from sklearn.model_selection import cross_val_score

scores = cross_val_score(gradien_model, x_norm, y, cv = 6 , scoring = 'r2' )

print(round(scores.mean(), 4))

"""Ajuste fino com a GridSearchCV:

"""

from sklearn.model_selection import GridSearchCV


arr1 = [0.01, 0.05, 0.1]
arr2 = [10, 20, 30]
arr3 = [0.7, 0.8, 0.9]
arr4 = [3, 5]

hiper_parametros = {
    'learning_rate': arr1,
    'n_estimators': arr2,
    'subsample': arr3,
    'max_depth': arr4,

}

procura = GridSearchCV(estimator = gradien_model, param_grid = hiper_parametros, cv=5)
procura.fit(x_norm, y)

print(f'Melhor score é: {procura.best_score_}')
print(f'Melhor learning_rate é : {procura.best_estimator_.learning_rate}')
print(f'Melhor n_estimators é: {procura.best_estimator_.n_estimators}')
print(f'Melhor subsample é: {procura.best_estimator_.subsample}')
print(f'Melhor max_depth é : {procura.best_estimator_.max_depth}')

grad_model = GradientBoostingRegressor(learning_rate = 0.1, n_estimators = 30, subsample = 0.9, max_depth = 5 )
grad_model.fit(x_train, y_train)
y_pred = grad_model.predict(x_test)
r2 = round(r2_score(y_test, y_pred), 4)
print(r2)

y_pred_train = grad_model.predict(x_train)
r2_train = round(r2_score(y_train, y_pred_train), 4)
print(r2_train)

grad_model.fit(x, y)
y_pred_definido = grad_model.predict(x)
r2_definido = round(r2_score(y, y_pred_definido), 8)
print(r2_definido)

"""Verificando os erros entre o valor real da variável dependente e variável preditiva"""

df_define = x
df_define['Y_real'] = y
df_define['y_pred'] = y_pred_definido

df_define

df_define['erro_abs'] = np.abs(df_define['Y_real'] - df_define['y_pred'])
df_define.shape

"""Analisando algumas métricas de desempenho"""

from sklearn.metrics import mean_absolute_error, mean_squared_error

mae = mean_absolute_error(y, y_pred_definido)
print(mae)
mse = mean_squared_error(y, y_pred_definido)
print(mse)

index = np.arange(0, 772)

index_df = pd.DataFrame(index)
df_insert(1, 'indice', index_df)

df_define

plt.figure(figsize = (45, 6))

plt.plot(df_define['indice'], df_define[['Y_real', 'y_pred']])

plt.title('Comportamento entre y real e y predito')
plt.show()

"""# Conclusão"""