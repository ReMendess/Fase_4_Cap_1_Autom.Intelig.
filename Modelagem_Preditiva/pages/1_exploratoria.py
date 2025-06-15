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

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.title("Análise com Agregação por Período")

df = simular_dados_sensores()  # sua função que retorna o DataFrame

# Converter DataHora para datetime
df['Data/Hora'] = pd.to_datetime(df['Data/Hora'])

# Criar coluna de período por hora
df['DataHora_Hora'] = df['DataHora'].dt.floor('H')

st.subheader("Dados agregados por hora (média)")

# Agrupar por período e variável, calcular média do valor
df_agg = df.groupby(['DataHora_Hora', 'Variavel']).Valor.mean().reset_index()

# Mostrar tabela agregada
st.dataframe(df_agg.head(20))

# Plotar gráfico das médias por hora para Temperatura e Umidade
fig, ax = plt.subplots(figsize=(12, 6))
for variavel in ['Temperatura', 'Umidade']:
    df_plot = df_agg[df_agg['Variavel'] == variavel]
    ax.plot(df_plot['DataHora_Hora'], df_plot['Valor'], label=variavel)
ax.set_xlabel('Hora')
ax.set_ylabel('Valor Médio')
ax.set_title('Valores Médios por Hora - Temperatura e Umidade')
ax.legend()
ax.tick_params(axis='x', rotation=45)
st.pyplot(fig)

st.subheader("Distribuição dos valores por variável")

# Histogramas por variável
variaveis = df['Variavel'].unique()
for v in variaveis:
    st.write(f"**Distribuição de {v}**")
    fig, ax = plt.subplots()
    sns.histplot(df[df['Variavel'] == v]['Valor'], bins=30, kde=True, ax=ax)
    st.pyplot(fig)
