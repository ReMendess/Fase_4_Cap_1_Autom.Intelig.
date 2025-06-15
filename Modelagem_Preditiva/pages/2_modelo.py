import streamlit as st
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
from simular_dados import simular_dados_sensores


st.set_page_config(page_title='Modelo de Risco de Deslizamento', layout='wide')
st.title('Modelagem Preditiva de Risco de Deslizamento')

df = simular_dados_sensores()

# Mapear colunas categóricas
df['Chuva'] = df['Chuva'].map({'Sem chuva': 0, 'Chovendo': 1})
df['Tipo de Solo'] = df['Tipo de Solo'].map({'Arenoso': 2, 'Argiloso': 1, 'Rochoso': 0})
df['Inclinação'] = df['Inclinação'].map({'Leve': 0, 'Moderada': 1, 'Forte': 2})
df['Região'] = df['Região'].map({'A': 0, 'B': 1, 'C': 2, 'D': 3})

df.drop(columns=['Nivel de Risco'], inplace=True)  # Remover a variável de apoio

st.sidebar.title('Filtros de Dados')
st.sidebar.subheader('Intervalos das Variáveis Numéricas')

temp_min, temp_max = st.sidebar.slider('Temperatura (°C):', float(df['Temperatura'].min()), float(df['Temperatura'].max()), (float(df['Temperatura'].min()), float(df['Temperatura'].max())))
umid_min, umid_max = st.sidebar.slider('Umidade (%):', float(df['Umidade'].min()), float(df['Umidade'].max()), (float(df['Umidade'].min()), float(df['Umidade'].max())))
vib_min, vib_max = st.sidebar.slider('Vibração:', float(df['Vibração'].min()), float(df['Vibração'].max()), (float(df['Vibração'].min()), float(df['Vibração'].max())))

df_filtered = df[
    (df['Temperatura'] >= temp_min) & (df['Temperatura'] <= temp_max) &
    (df['Umidade'] >= umid_min) & (df['Umidade'] <= umid_max) &
    (df['Vibração'] >= vib_min) & (df['Vibração'] <= vib_max)
]

if df_filtered.empty:
    st.warning('Nenhum dado corresponde aos filtros selecionados.')
    st.stop()

st.subheader('Amostra dos Dados Filtrados')
st.dataframe(df_filtered.head())

X = df_filtered.drop(columns=['Risco'])
y = df_filtered['Risco']

# Checar se tem dados suficientes
if len(X) < 2:
    st.warning('Poucos dados para treinar. Ajuste os filtros.')
    st.stop()

# Treinamento
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
model = RandomForestRegressor(
    n_estimators=100,         # padrão ótimo para maioria dos casos
    max_depth=10,             # evita árvores profundas demais
    min_samples_leaf=5,       # impede que folhas tenham só 1 amostra
    max_features='sqrt',      # boa prática para diminuir overfitting
    random_state=42
)
model.fit(X_train, y_train)
score = model.score(X_test, y_test)
st.write(f'**Acurácia (R²):** {score:.2f}')

importances = pd.Series(model.feature_importances_, index=X.columns)
st.subheader('Importância das Variáveis')
st.bar_chart(importances.sort_values(ascending=False))

y_pred = model.predict(X_test)
fig, ax = plt.subplots()
ax.scatter(y_test, y_pred, alpha=0.7)
ax.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'r--')
ax.set_xlabel('Valor Real')
ax.set_ylabel('Predito')
ax.set_title('Previsão vs Real')
st.pyplot(fig)


r2_treino = model.score(X_train, y_train)
r2_teste = model.score(X_test, y_test)

st.write(f"R² Treino: {r2_treino:.2f}")
st.write(f"R² Teste: {r2_teste:.2f}")

y_train_pred = model.predict(X_train)
y_test_pred = model.predict(X_test)

mae_train = mean_absolute_error(y_train, y_train_pred)
mae_test = mean_absolute_error(y_test, y_test_pred)

st.write(f"MAE treino: {mae_train:.2f}")
st.write(f"MAE teste: {mae_test:.2f}")
