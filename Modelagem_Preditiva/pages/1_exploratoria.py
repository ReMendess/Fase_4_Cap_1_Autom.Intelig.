import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from simular_dados import simular_dados_sensores

st.title("Análise Exploratória")

# Pegando um df simulado pela nossa função
df = simular_dados_sensores()
st.subheader("Amostra dos Dados")
st.dataframe(df.head())

st.write(f"O DataFrame tem {df.shape[0]} linhas e {df.shape[1]} colunas.")

# Calculando a média
medias_por_sensor = df.groupby('Sensor')['Valor Registrado'].mean().reset_index()
medias_por_sensor.columns = ['Sensor', 'Média dos Valores']
medias_por_sensor['Média dos Valores'] = medias_por_sensor['Média dos Valores'].round(2) # Arredonda os valores para 2 casas decimais

st.subheader("Médias Gerais")
st.table(medias_por_sensor)

df_umidade = df[df['Sensor'] == 'Umidade']
df_umidade['Data'] = df_umidade['Data/Hora'].dt.date

media_diaria_umidade = df_umidade.groupby('Data')['Valor Registrado'].mean().reset_index()

# Gráfico de variação da umidade
st.subheader("Variação Diária da Umidade")
fig, ax = plt.subplots()
sns.lineplot(data=media_diaria_umidade, x='Data', y='Valor Registrado', ax=ax)
plt.ylabel('Umidade (%)')
plt.xlabel('Data')
plt.xticks(rotation=45)
plt.title('Umidade Média ao Longo dos Dias')
st.pyplot(fig)

df_umidade = df[df['Sensor'] == 'Umidade']

st.subheader("Distribuição de Umidade")
fig, ax = plt.subplots()
sns.histplot(df_umidade['Valor Registrado'], bins=30, kde=True, ax=ax)
plt.axvline(x=40, color='red', linestyle='--', label='Limite Crítico?')
plt.title('Frequência dos Níveis de Umidade')
plt.xlabel('Umidade (%)')
plt.ylabel('Contagem')
plt.legend()
st.pyplot(fig)


# Filtrando os sensores
sensores_desejados = ['Temperatura', 'Umidade', 'pH', 'Potássio', 'Fósforo']
df_corr = df[df['Sensor'].isin(sensores_desejados)]

# Cria uma df onde cada linha representa uma data/hora e cada coluna um sensor
df_pivot = df_corr.pivot_table(index='Data/Hora', columns='Sensor', values='Valor Registrado')

# Removendo linhas com valores ausentes
df_pivot = df_pivot.dropna()

# Calcula a correlação
matriz_corr = df_pivot.corr()

# Gráfico de calor
st.subheader("Mapa de Correlação")
fig, ax = plt.subplots(figsize=(8, 6))
sns.heatmap(matriz_corr, annot=True, cmap='coolwarm', center=0, linewidths=0.5, fmt=".2f")
plt.title("Correlação entre Temperatura, Umidade, pH, Potássio e Fósforo")
st.pyplot(fig)

# Garante que a coluna 'Data/Hora' é do tipo datetime
df['Data/Hora'] = pd.to_datetime(df['Data/Hora'])

# Gráfico Personalizado / Escolhido pelo Usuário
# Extrai componentes de data e hora para análise
df['Hora'] = df['Data/Hora'].dt.hour
df['Dia da Semana'] = df['Data/Hora'].dt.day_name()
df['Mês'] = df['Data/Hora'].dt.month_name()

st.sidebar.header('Configurações do Gráfico')

variaveis_x = ['Hora', 'Dia da Semana', 'Mês', 'Local do Sensor']
x_axis = st.sidebar.selectbox('Selecione a variável para o Eixo X', variaveis_x)
variaveis_y = ['Valor Registrado']
y_axis = st.sidebar.selectbox('Selecione a variável para o Eixo Y', variaveis_y)

# Opção para selecionar o tipo de gráfico
tipo_grafico = st.sidebar.selectbox('Selecione o tipo de gráfico', ['Linha', 'Dispersão', 'Barra', 'Boxplot'])

# Opção para selecionar o sensor
sensores_unicos = df['Sensor'].unique().tolist()
sensor_selecionado = st.sidebar.multiselect('Selecione o(s) Sensor(es)', sensores_unicos, default=sensores_unicos)

# Filtrar o df com base no sensor selecionado
df_filtrado = df[df['Sensor'].isin(sensor_selecionado)]

# Opção para agrupar dados para gráficos de barra e boxplot
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

