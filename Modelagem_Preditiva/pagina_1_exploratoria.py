import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from simular_dados import simular_dados_sensores

def mostrar_pagina_exploratoria():
    st.title(" Análise Exploratória dos Dados de Sensores")

    df = simular_dados_sensores()
    st.subheader("Amostra dos Dados")
    st.dataframe(df.head())

    st.subheader("Distribuição de Temperatura e Umidade")
    col1, col2 = st.columns(2)

    with col1:
        fig, ax = plt.subplots()
        sns.histplot(df["Temperatura"], kde=True, ax=ax)
        ax.set_title("Distribuição de Temperatura")
        st.pyplot(fig)

    with col2:
        fig, ax = plt.subplots()
        sns.histplot(df["Umidade"], kde=True, ax=ax)
        ax.set_title("Distribuição de Umidade")
        st.pyplot(fig)

    st.subheader("Correlação entre Variáveis")
    fig, ax = plt.subplots()
    sns.heatmap(df.corr(numeric_only=True), annot=True, cmap="coolwarm", ax=ax)
    st.pyplot(fig)
