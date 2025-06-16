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

    # Simular datas ao longo do ano
    data_base = datetime.now().replace(month=1, day=1)
    data_hora = [
        data_base + timedelta(days=np.random.randint(0, 365), hours=np.random.randint(0, 24), minutes=np.random.randint(0, 60))
        for _ in range(n_samples)
    ]
    data_hora = sorted(data_hora)

    # Extrair o mês de cada data para sazonalidade
    meses = [dt.month for dt in data_hora]

    # Funções para variação sazonal
    def temperatura_sazonal(mes):
        return np.random.normal(loc=25 + 5 * np.cos((mes - 1) * np.pi / 6), scale=3)

    def umidade_sazonal(mes):
        return np.clip(np.random.normal(loc=60 + 20 * np.sin((mes - 1) * np.pi / 6), scale=10), 30, 100)

    temperatura = np.array([temperatura_sazonal(m) for m in meses])
    umidade = np.array([umidade_sazonal(m) for m in meses])
    ph = np.random.normal(loc=6.5, scale=0.4, size=n_samples)
    fosforo = np.random.normal(loc=40, scale=10, size=n_samples)
    potassio = np.random.normal(loc=150, scale=30, size=n_samples)

    status = np.random.choice(['Ativo', 'Inativo', 'Manutenção'], size=n_samples, p=[0.8, 0.1, 0.1])
    locais = np.random.choice(['Zona Norte', 'Zona Sul', 'Zona Leste', 'Zona Oeste', 'Área Rural'], size=n_samples)

    def criar_df(sensor, valores):
        return pd.DataFrame({
            'Sensor': sensor,
            'Valor Registrado': valores,
            'Data/Hora': data_hora,
            'Status do Sensor': status,
            'Local do Sensor': locais
        })

    df_final = pd.concat([
        criar_df('pH', ph),
        criar_df('Fósforo', fosforo),
        criar_df('Potássio', potassio),
        criar_df('Temperatura', temperatura),
        criar_df('Umidade', umidade)
    ])

    df_final = df_final.sort_values(by='Data/Hora', ascending=False).reset_index(drop=True)
    return df_final
