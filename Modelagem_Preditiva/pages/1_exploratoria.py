import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from simular_dados import simular_dados_sensores

st.title("Análise Exploratória dos Dados de Sensores")

df = simular_dados_sensores()
st.subheader("Amostra dos Dados")
st.dataframe(df.head())

# Pivot para reorganizar dados por Sensor
try:
    df_pivot = df.pivot_table(
        index=["Data/Hora", "Local do Sensor", "Status do Sensor"],
        columns="Sensor",
        values="Valor Registrado"
    ).reset_index()
    st.subheader("Dados reorganizados por Sensor")
    st.dataframe(df_pivot.head())
except KeyError as e:
    st.error(f"Erro ao criar pivot_table: {e}")

# Exemplo de gráfico: temperatura e umidade ao longo do tempo em um local específico
st.subheader("Gráfico de Temperatura e Umidade ao longo do tempo")

# Selecionar um local para filtrar (exemplo)
locais = df["Local do Sensor"].unique()
local_selecionado = st.selectbox("Selecione o Local do Sensor:", locais)

df_filtrado = df_pivot[df_pivot["Local do Sensor"] == local_selecionado]

fig, ax1 = plt.subplots(figsize=(12,6))

if 'Temperatura' in df_filtrado.columns and 'Umidade' in df_filtrado.columns:
    ax1.plot(df_filtrado["Data/Hora"], df_filtrado["Temperatura"], color='tab:red', label='Temperatura (°C)')
    ax1.set_ylabel("Temperatura (°C)", color='tab:red')
    ax1.tick_params(axis='y', labelcolor='tab:red')

    ax2 = ax1.twinx()
    ax2.plot(df_filtrado["Data/Hora"], df_filtrado["Umidade"], color='tab:blue', label='Umidade (%)')
    ax2.set_ylabel("Umidade (%)", color='tab:blue')
    ax2.tick_params(axis='y', labelcolor='tab:blue')

    plt.title(f"Temperatura e Umidade ao longo do tempo - {local_selecionado}")
    fig.autofmt_xdate()
    st.pyplot(fig)
else:
    st.warning("Não há dados de Temperatura e/ou Umidade no DataFrame reorganizado.")

# Exemplo de análise estatística simples
st.subheader("Análise Estatística Descritiva")

st.write(df.describe())
