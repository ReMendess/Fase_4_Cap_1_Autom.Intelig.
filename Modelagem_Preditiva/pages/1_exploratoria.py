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
# Garante que a coluna 'Data/Hora' é do tipo datetime
df['Data/Hora'] = pd.to_datetime(df['Data/Hora'])

st.write(df.describe())

# Extrai componentes de data e hora para análise
df['Hora'] = df['Data/Hora'].dt.hour
df['Dia da Semana'] = df['Data/Hora'].dt.day_name()
df['Mês'] = df['Data/Hora'].dt.month_name()

st.sidebar.header('Configurações do Gráfico')

# Opções de variáveis para o eixo X
variaveis_x = ['Hora', 'Dia da Semana', 'Mês', 'Local do Sensor']
x_axis = st.sidebar.selectbox('Selecione a variável para o Eixo X', variaveis_x)

# Opções de variáveis para o eixo Y (apenas variáveis numéricas ou agregadas)
# Filtra os dados de cada sensor

variaveis_y = ['Valor Registrado']
y_axis = st.sidebar.selectbox('Selecione a variável para o Eixo Y', variaveis_y)

# Opção para selecionar o tipo de gráfico
tipo_grafico = st.sidebar.selectbox('Selecione o tipo de gráfico', ['Linha', 'Dispersão', 'Barra', 'Boxplot'])

# Opção para selecionar o sensor
sensores_unicos = df['Sensor'].unique().tolist()
sensor_selecionado = st.sidebar.multiselect('Selecione o(s) Sensor(es)', sensores_unicos, default=sensores_unicos)

# Filtrar o DataFrame com base no sensor selecionado
df_filtrado = df[df['Sensor'].isin(sensor_selecionado)]

# Opção para agrupar dados (útil para gráficos de barra, boxplot, violinplot)
if tipo_grafico in ['Barra', 'Boxplot']:
    agrupar_por = st.sidebar.selectbox('Agrupar por', ['Sensor', 'Local do Sensor', None])
else:
    agrupar_por = None

# Criar o gráfico
st.header(f'Gráfico de {tipo_grafico} para {y_axis} vs {x_axis}')

if not df_filtrado.empty:
    plt.figure(figsize=(12, 6))

    if tipo_grafico == 'Linha':
        if agrupar_por:
            sns.lineplot(data=df_filtrado, x=x_axis, y=y_axis, hue=agrupar_por, marker='o')
        else:
            sns.lineplot(data=df_filtrado, x=x_axis, y=y_axis, marker='o')
        plt.xticks(rotation=45)

    elif tipo_grafico == 'Dispersão':
        if agrupar_por:
             sns.scatterplot(data=df_filtrado, x=x_axis, y=y_axis, hue=agrupar_por)
        else:
             sns.scatterplot(data=df_filtrado, x=x_axis, y=y_axis)
        plt.xticks(rotation=45)

    elif tipo_grafico == 'Barra':
        if agrupar_por:
            sns.barplot(data=df_filtrado, x=x_axis, y=y_axis, hue=agrupar_por)
        else:
            sns.barplot(data=df_filtrado, x=x_axis, y=y_axis)
        plt.xticks(rotation=45)

    elif tipo_grafico == 'Boxplot':
        if agrupar_por:
            sns.boxplot(data=df_filtrado, x=x_axis, y=y_axis, hue=agrupar_por)
        else:
            sns.boxplot(data=df_filtrado, x=x_axis, y=y_axis)
        plt.xticks(rotation=45)

    plt.title(f'Relação entre {x_axis} e {y_axis}')
    plt.xlabel(x_axis)
    plt.ylabel(y_axis)
    plt.tight_layout()
    st.pyplot(plt)
    plt.close()
else:
    st.warning("Nenhum dado encontrado para o(s) sensor(es) selecionado(s).")

# Exibir o DataFrame filtrado (opcional)
st.subheader("Dados Filtrados")
st.dataframe(df_filtrado)
