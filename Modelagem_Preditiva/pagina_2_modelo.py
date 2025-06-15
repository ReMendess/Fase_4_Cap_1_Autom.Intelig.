import streamlit as st
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
from simulador_dados import gerar_dados_sensores

def mostrar_pagina_modelo():
    st.title(" Análise Preditiva - Necessidade de Irrigação")

    df = gerar_dados_sensores()

    # Criando a coluna-alvo
    df["precisa_irrigar"] = ((df["umidade"] < 50) & (df["temperatura"] > 30)).astype(int)

    X = df[["temperatura", "umidade"]]
    y = df["precisa_irrigar"]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

    modelo = RandomForestClassifier()
    modelo.fit(X_train, y_train)

    y_pred = modelo.predict(X_test)

    st.subheader("Relatório de Classificação")
    st.text(classification_report(y_test, y_pred))

    st.subheader("Faça uma previsão personalizada:")
    temp = st.slider("Temperatura", 0.0, 50.0, 25.0)
    umi = st.slider("Umidade", 0.0, 100.0, 60.0)

    pred = modelo.predict([[temp, umi]])[0]
    st.success(" Necessita irrigação!" if pred == 1 else "Não precisa irrigação agora.")

