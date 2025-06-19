import streamlit as st
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.metrics import accuracy_score, mean_squared_error
from simular_dados import simular_dados_sensores
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

st.set_page_config(page_title='Previsão de Irrigação', layout='wide')
st.title('Modelo de Necessidade de Irrigação e Modelo de Previsão de Umidade por Região')

# Simular dados
df = simular_dados_sensores()

# ========================
# Modelo de classificação / Irrigação

st.header("1. Modelo de Predição de Necessidade de Irrigação")

df_umidade = df[df['Sensor'] == 'Umidade'].copy()

st.markdown("""
O **limiar de umidade** define se o solo está seco demais e precisa de irrigação.  
- Umidade **abaixo do limiar** → necessita irrigação.  
- Umidade **acima do limiar** → não necessita.
""")

limiar = st.slider("Limiar de Umidade para Irrigação (%)", 0.0, 100.0, 60.0)
df_umidade['Necessita_Irrigacao'] = (df_umidade['Valor Registrado'] < limiar).astype(int)

X = df_umidade[['Valor Registrado']]
y = df_umidade['Necessita_Irrigacao']

if len(y.unique()) > 1:
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model_class = RandomForestClassifier(n_estimators=50, random_state=42)
    model_class.fit(X_train, y_train)

    acc = accuracy_score(y_test, model_class.predict(X_test))
    st.metric("Acurácia do Modelo", f"{acc:.2%}")

    novo_valor = st.number_input("Novo valor de umidade (%)", min_value=0.0, max_value=100.0, value=55.0)
    previsao = model_class.predict([[novo_valor]])[0]

    if previsao == 1:
        st.warning("PREVISÃO: Necessita Irrigação!")
    else:
        st.success("PREVISÃO: Não necessita Irrigação.")
else:
    st.warning("Ajuste o limiar para que o modelo tenha exemplos de ambas as classes.")

# Modelo de regressão por Região

st.header("2. Modelo de Previsão da Umidade por Região")

# Extraindo mês e região
df_umidade['Mês'] = pd.to_datetime(df_umidade['Data/Hora']).dt.month
df_umidade['Região'] = df_umidade['Local do Sensor']

# Agrupar média por mês e região
media_por_regiao = df_umidade.groupby(['Mês', 'Região'])['Valor Registrado'].mean().reset_index()
media_por_regiao.rename(columns={'Valor Registrado': 'Umidade Média'}, inplace=True)

# Lista de regiões
regioes = media_por_regiao['Região'].unique().tolist()

# Criar DataFrame para guardar previsões
previsoes_total = pd.DataFrame()

for reg in regioes:
    df_reg = media_por_regiao[media_por_regiao['Região'] == reg]
    
    X_reg = df_reg[['Mês']]
    y_reg = df_reg['Umidade Média']
    
    model_reg = RandomForestRegressor(n_estimators=100, random_state=42)
    model_reg.fit(X_reg, y_reg)
    
    meses = pd.DataFrame({'Mês': np.arange(1, 13)})
    umidade_pred = model_reg.predict(meses)
    meses['Umidade Prevista'] = umidade_pred
    meses['Região'] = reg
    
    previsoes_total = pd.concat([previsoes_total, meses])

st.write(previsoes_total.head())

# Mostrar gráfico
st.subheader("Previsão de Umidade Média por Região (Mensal)")
fig, ax = plt.subplots(figsize=(12, 6))
sns.barplot(data=previsoes_total, x='Mês', y='Umidade Prevista', hue='Região')
plt.title('Previsão de Umidade por Região e Mês')
plt.ylabel('Umidade (%)')
plt.xlabel('Mês')
st.pyplot(fig)


