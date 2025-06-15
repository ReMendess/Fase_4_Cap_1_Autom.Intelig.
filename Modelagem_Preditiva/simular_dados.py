import numpy as np
import pandas as pd
import streamlit as st
import time
from datetime import datetime, timedelta

@st.cache_data(show_spinner=True)
def simular_dados_sensores(n_samples=1000):
    np.random.seed(42)
    time.sleep(1)
    print("Simulando dados dos sensores...")

    # Simula timestamps nas últimas 24 horas
    agora = datetime.now()
    data_hora = [agora - timedelta(minutes=np.random.randint(0, 1440)) for _ in range(n_samples)]

    # Valores simulados
    ph = np.random.normal(loc=6.5, scale=0.4, size=n_samples)
    fosforo = np.random.normal(loc=40, scale=10, size=n_samples)
    potassio = np.random.normal(loc=150, scale=30, size=n_samples)
    temperatura = np.random.normal(loc=28, scale=5, size=n_samples)     # °C
    umidade = np.random.uniform(low=40, high=90, size=n_samples)        # %

    status = np.random.choice(['Ativo', 'Inativo', 'Manutenção'], size=n_samples, p=[0.8, 0.1, 0.1])
    locais = np.random.choice(['Zona Norte', 'Zona Sul', 'Zona Leste', 'Zona Oeste', 'Área Rural'], size=n_samples)

    # Criação dos DataFrames para cada sensor
    df_ph = pd.DataFrame({
        'Sensor': 'pH',
        'Valor Registrado': ph,
        'Data/Hora': data_hora,
        'Status do Sensor': status,
        'Local do Sensor': locais
    })

    df_fosforo = pd.DataFrame({
        'Sensor': 'Fósforo',
        'Valor Registrado': fosforo,
        'Data/Hora': data_hora,
        'Status do Sensor': status,
        'Local do Sensor': locais
    })

    df_potassio = pd.DataFrame({
        'Sensor': 'Potássio',
        'Valor Registrado': potassio,
        'Data/Hora': data_hora,
        'Status do Sensor': status,
        'Local do Sensor': locais
    })

    df_temperatura = pd.DataFrame({
        'Sensor': 'Temperatura',
        'Valor Registrado': temperatura,
        'Data/Hora': data_hora,
        'Status do Sensor': status,
        'Local do Sensor': locais
    })

    df_umidade = pd.DataFrame({
        'Sensor': 'Umidade',
        'Valor Registrado': umidade,
        'Data/Hora': data_hora,
        'Status do Sensor': status,
        'Local do Sensor': locais
    })

    # Junta todos os DataFrames
    df_final = pd.concat([df_ph, df_fosforo, df_potassio, df_temperatura, df_umidade])
    df_final = df_final.sort_values(by='Data/Hora', ascending=False).reset_index(drop=True)

    return df_final
