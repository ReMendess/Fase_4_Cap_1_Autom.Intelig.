import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from simular_dados import simular_dados_sensores

st.title(" Análise Exploratória dos Dados de Sensores")

df = simular_dados_sensores()
st.subheader("Amostra dos Dados")
st.dataframe(df.head())

st.title("Analise de dados")
st.subheader("Visualização dos dados")
st.dataframe(df.tail())

linhas, colunas = df.shape
st.write(f"o data frame possui {linhas} linhas e {colunas} colunas")
df_types = pd.DataFrame({
    'Coluna': df.columns,
    'Tipos de Dados': df.dtypes.astype(str)
})

st.write(df_types)
# Verificar valores ausentes
st.subheader('Valores Ausentes')
st.write(df.isnull().sum())
st.write("Analise descritiva dos dados:")
st.write(df.describe())


print(df.columns)

st.title("Matriz de correlação")
correlacao = df.corr()
fig, ax = plt.subplots(figsize=(10, 8))
sns.heatmap(correlacao, annot=True, cmap='coolwarm', ax=ax)
st.pyplot(fig)
