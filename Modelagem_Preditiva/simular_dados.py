import numpy as np
import pandas as pd
import streamlit as st
import time
from datetime import datetime, timedelta

@st.cache_data(show_spinner=True)

def simular_dados_sensores(n_samples=1000):
    import numpy as np
    import pandas as pd
    from datetime import datetime, timedelta
    import time

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
    meses = [dt.month for dt in data_hora]

    # Sazonalidade: temperatura e umidade
    def temperatura_sazonal(mes):
        return np.random.normal(loc=25 + 5 * np.cos((mes - 1) * np.pi / 6), scale=2)

    def umidade_sazonal(mes, temp):
        base = 60 + 20 * np.sin((mes - 1) * np.pi / 6)
        ajuste = -0.5 * (temp - 25)  # temperatura ↑ → umidade ↓
        return np.clip(np.random.normal(loc=base + ajuste, scale=8), 30, 100)

    temperatura = np.array([temperatura_sazonal(m) for m in meses])
    umidade = np.array([umidade_sazonal(m, temp) for m, temp in zip(meses, temperatura)])

    # pH afetado pela umidade (mais umidade, pH ligeiramente mais ácido)
    ph = np.random.normal(loc=6.8 - 0.01 * umidade, scale=0.15)

    # Fósforo afetado pela umidade e pH extremos (muito baixo ou alto → disponibilidade menor)
    fosforo = 45 - 0.1 * umidade - 8 * np.abs(ph - 6.5)
    fosforo += np.random.normal(loc=0, scale=3, size=n_samples)

    # Potássio levemente impactado pela temperatura e umidade
    potassio = 150 + 0.5 * temperatura - 0.2 * umidade + np.random.normal(loc=0, scale=10, size=n_samples)

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
        criar_df('Temperatura', temperatura),
        criar_df('Umidade', umidade),
        criar_df('pH', ph),
        criar_df('Fósforo', fosforo),
        criar_df('Potássio', potassio),
    ])

    df_final = df_final.sort_values(by='Data/Hora', ascending=False).reset_index(drop=True)
    return df_final
