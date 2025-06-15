import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from simular_dados import simular_dados_sensores

st.title("Análise Exploratória dos Dados de Sensores")

df = simular_dados_sensores()
st.subheader("Amostra dos Dados")
st.dataframe(df.head())

st.write(f"O DataFrame tem {df.shape[0]} linhas e {df.shape[1]} colunas.")

# Mostrar estatísticas básicas
st.subheader("Estatísticas Descritivas")
st.write(df.describe())

# Filtrar dados de Temperatura
temp = df[df['Variavel'] == 'Temperatura']

# Filtrar dados de Umidade
umid = df[df['Variavel'] == 'Umidade']

# Gráfico Temperatura ao longo do tempo (últimos 100 registros)
st.subheader("Temperatura ao longo do tempo")
fig, ax = plt.subplots()
ax.plot(temp['DataHora'].tail(100), temp['Valor'].tail(100), color='red')
ax.set_xlabel('DataHora')
ax.set_ylabel('Temperatura (°C)')
ax.tick_params(axis='x', rotation=45)
st.pyplot(fig)

# Gráfico Umidade ao longo do tempo (últimos 100 registros)
st.subheader("Umidade ao longo do tempo")
fig2, ax2 = plt.subplots()
ax2.plot(umid['DataHora'].tail(100), umid['Valor'].tail(100), color='blue')
ax2.set_xlabel('DataHora')
ax2.set_ylabel('Umidade (%)')
ax2.tick_params(axis='x', rotation=45)
st.pyplot(fig2)
