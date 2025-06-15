import streamlit as st
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
from simular_dados import simular_dados_sensores
from sklearn.metrics import accuracy_score, classification_report


st.set_page_config(page_title='Modelo de Risco de Deslizamento', layout='wide')
st.title('Modelagem Preditiva de Risco de Deslizamento')

df = simular_dados_sensores()

st.header("Modelo de Predição de Irrigação")

# Preparar os dados para o modelo
# Focaremos nos dados de umidade como principal preditor
# Filtrar o DataFrame com base no sensor selecionado
df_filtrado = df[df['Sensor'].isin(sensor_selecionado)]
df_umidade_filtered = df_filtrado[df_filtrado['Sensor'] == 'Umidade'].copy()

if not df_umidade_filtered.empty:
    # Definir um limiar para a necessidade de irrigação (exemplo: umidade < 60%)
    # Isso é um exemplo, o limiar ideal dependeria do tipo de cultura e solo.
    umidade_limiar = st.slider("Defina o limiar de Umidade (%) para Irrigação", 0.0, 100.0, 60.0)
    df_umidade_filtered['Necessidade_Irrigacao'] = (df_umidade_filtered['Valor Registrado'] < umidade_limiar).astype(int)

    st.write(f"Baseado em um limiar de umidade abaixo de {umidade_limiar}%, a necessidade de irrigação foi definida.")

    # Selecionar features e target
    # Para um modelo simples, usaremos apenas a umidade, mas em um cenário real,
    # outros fatores como temperatura, tipo de solo e cultura seriam importantes.
    X = df_umidade_filtered[['Valor Registrado']]
    y = df_umidade_filtered['Necessidade_Irrigacao']

    if len(y.unique()) > 1: # Garantir que há mais de uma classe (necessita e não necessita)
        # Dividir os dados em treino e teste
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        # Treinar o modelo (Random Forest Classifier como exemplo)
        st.subheader("Treinando o Modelo")
        model = RandomForestClassifier(n_estimators=100, random_state=42)
        model.fit(X_train, y_train)

        # Fazer previsões no conjunto de teste
        y_pred = model.predict(X_test)

        # Avaliar o modelo
        st.subheader("Avaliação do Modelo")
        accuracy = accuracy_score(y_test, y_pred)
        st.write(f"Acurácia do modelo: {accuracy:.2f}")

        st.text("Relatório de Classificação:")
        report = classification_report(y_test, y_pred)
        st.text(report)

        # Fazer uma previsão para um novo valor de umidade
        st.subheader("Prever Necessidade de Irrigação para um novo valor de Umidade")
        novo_umidade = st.number_input("Insira um novo valor de Umidade (%)", min_value=0.0, max_value=100.0, value=55.0)
        previsao = model.predict([[novo_umidade]])

        if previsao[0] == 1:
            st.warning("PREVISÃO: Necessidade de Irrigação!")
        else:
            st.success("PREVISÃO: Não há Necessidade de Irrigação.")

    else:
        st.warning("Dados insuficientes para treinar o modelo. Certifique-se de que há registros de umidade acima e abaixo do limiar.")

else:
    st.warning("Nenhum dado de umidade disponível para treinamento do modelo.")
