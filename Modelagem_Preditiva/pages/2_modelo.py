import streamlit as st
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from simular_dados import simular_dados_sensores

st.set_page_config(page_title='Previsão de Irrigação', layout='wide')
st.title('Modelo Simples de Necessidade de Irrigação')

# Simular dados
df = simular_dados_sensores()

# Filtrar apenas os dados de umidade
df_umidade = df[df['Sensor'] == 'Umidade'].copy()

# Definir limiar
limiar = st.slider("Limiar de Umidade para Irrigação (%)", 0.0, 100.0, 60.0)

# Criar target binário
df_umidade['Necessita_Irrigacao'] = (df_umidade['Valor Registrado'] < limiar).astype(int)

# Separar features e target
X = df_umidade[['Valor Registrado']]
y = df_umidade['Necessita_Irrigacao']

# Garantir que há pelo menos duas classes
if len(y.unique()) > 1:
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = RandomForestClassifier(n_estimators=50, random_state=42)
    model.fit(X_train, y_train)

    acc = accuracy_score(y_test, model.predict(X_test))
    st.metric("Acurácia do Modelo", f"{acc:.2%}")

    novo_valor = st.number_input("Novo valor de umidade (%)", min_value=0.0, max_value=100.0, value=55.0)
    previsao = model.predict([[novo_valor]])[0]

    if previsao == 1:
        st.warning("PREVISÃO: Necessita Irrigação!")
    else:
        st.success("PREVISÃO: Não necessita Irrigação.")
else:
    st.warning("Ajuste o limiar para que o modelo tenha exemplos de ambas as classes.")

