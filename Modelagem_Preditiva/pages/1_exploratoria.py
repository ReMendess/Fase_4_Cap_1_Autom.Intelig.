import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from simular_dados import simular_dados_sensores

st.title("Análise Exploratória dos Dados de Sensores")

df = simular_dados_sensores()
st.subheader("Amostra dos Dados")
st.dataframe(df.head())

# Mostrar forma e tipos
linhas, colunas = df.shape
st.write(f"O dataframe possui {linhas} linhas e {colunas} colunas")

df_types = pd.DataFrame({
    'Coluna': df.columns,
    'Tipo de Dados': df.dtypes.astype(str)
})
st.write(df_types)

# Valores ausentes
st.subheader("Valores Ausentes")
st.write(df.isnull().sum())

# Estatísticas descritivas
st.subheader("Estatísticas Descritivas")
st.write(df.describe(include='all'))

# Para facilitar análise, pivotar os dados de "Variável" e "Valor"
df_pivot = df.pivot_table(index=["DataHora", "Zona", "Status"], columns="Variável", values="Valor").reset_index()

st.subheader("Dados pivotados (colunas por variável)")
st.dataframe(df_pivot.head())

# Análise temporal: tendência média da Temperatura e Umidade por Zona
st.subheader("Tendência Temporal por Zona")

fig, ax = plt.subplots(figsize=(12,6))
for zona in df_pivot['Zona'].unique():
    temp_media = df_pivot[df_pivot['Zona'] == zona].groupby('DataHora')['Temperatura'].mean()
    ax.plot(temp_media.index, temp_media.values, label=f'Temperatura - {zona}')
ax.set_xlabel('DataHora')
ax.set_ylabel('Temperatura (°C)')
ax.legend()
st.pyplot(fig)

fig, ax = plt.subplots(figsize=(12,6))
for zona in df_pivot['Zona'].unique():
    umid_media = df_pivot[df_pivot['Zona'] == zona].groupby('DataHora')['Umidade'].mean()
    ax.plot(umid_media.index, umid_media.values, label=f'Umidade - {zona}')
ax.set_xlabel('DataHora')
ax.set_ylabel('Umidade (%)')
ax.legend()
st.pyplot(fig)

# Boxplot por Zona para pH e Potássio
st.subheader("Distribuição de pH e Potássio por Zona")
fig, axs = plt.subplots(1, 2, figsize=(14,5))

sns.boxplot(data=df_pivot, x='Zona', y='pH', ax=axs[0])
axs[0].set_title("pH por Zona")

sns.boxplot(data=df_pivot, x='Zona', y='Potássio', ax=axs[1])
axs[1].set_title("Potássio por Zona")

st.pyplot(fig)

# Correlação das variáveis numéricas
st.subheader("Matriz de Correlação das Variáveis Numéricas")

corr = df_pivot[['Temperatura', 'Umidade', 'Potássio', 'pH']].corr()
fig, ax = plt.subplots(figsize=(8,6))
sns.heatmap(corr, annot=True, cmap='coolwarm', ax=ax)
st.pyplot(fig)

# Status geral
st.subheader("Status dos Sensores")
status_count = df['Status'].value_counts()
st.bar_chart(status_count)

# Pergunta interativa
st.subheader("Explorar dados por Zona")
zona_sel = st.selectbox("Escolha uma Zona", df['Zona'].unique())
df_zona = df[df['Zona'] == zona_sel]

st.write(f"Resumo estatístico para a Zona {zona_sel}:")
st.write(df_zona.groupby('Variável')['Valor'].describe())

# Gráfico de série temporal para a zona escolhida e variável selecionada
variavel_sel = st.selectbox("Escolha a variável para visualizar ao longo do tempo", df['Variável'].unique())
df_var = df_zona[df_zona['Variável'] == variavel_sel]

fig, ax = plt.subplots(figsize=(12,4))
ax.plot(df_var['DataHora'], df_var['Valor'], marker='o', linestyle='-', markersize=3)
ax.set_title(f'{variavel_sel} ao longo do tempo - Zona {zona_sel}')
ax.set_xlabel('DataHora')
ax.set_ylabel('Valor')
plt.xticks(rotation=45)
st.pyplot(fig)
