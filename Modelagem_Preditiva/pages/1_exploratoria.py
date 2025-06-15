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
df.drop(df.column["Data/Hora"], index = true
