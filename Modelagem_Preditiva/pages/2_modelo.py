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
st.title('Modelo de Necessidade de Irrigação + Previsão de Umidade Futura')

# Simular dados
df = simular_dados_sensores()

# ========================
# MODELO DE CLASSIFICAÇÃO
# ========================
st.header("1. Predição de Necessidade de Irrigação (Baseado em umidade atual)")

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

# =====================
# MODELO DE REGRESSÃO
# =====================
st.header("2. Previsão da Umidade Média para os Próximos Meses")

# Extrair mês e calcular média histórica de umidade por mês
df_umidade['Mês'] = pd.to_datetime(df_umidade['Data/Hora']).dt.month
media_umidade_mes = df_umidade.groupby('Mês')['Valor Registrado'].mean().reset_index()

# Modelo de regressão: prever umidade com base no mês
X_reg = media_umidade_mes[['Mês']]
y_reg = media_umidade_mes['Valor Registrado']

model_reg = RandomForestRegressor(n_estimators=100, random_state=42)
model_reg.fit(X_reg, y_reg)

# Previsão para todos os meses
meses_futuros = pd.DataFrame({'Mês': np.arange(1, 13)})
umidade_prevista = model_reg.predict(meses_futuros)
meses_futuros['Umidade Prevista'] = umidade_prevista

# Gráfico
st.subheader("Umidade Média Prevista por Mês")
fig, ax = plt.subplots()
sns.barplot(data=meses_futuros, x='Mês', y='Umidade Prevista', palette='Blues', ax=ax)
plt.ylabel('Umidade (%)')
plt.xlabel('Mês')
plt.title('Previsão da Umidade Média Mensal')
st.pyplot(fig)


