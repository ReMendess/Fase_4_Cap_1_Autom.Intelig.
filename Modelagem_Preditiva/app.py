# app.py
import streamlit as st
st.set_page_config(
    page_title='Aplicação de Análise e Predição',
    layout='wide'
)
st.title('Aplicação de Análise e Predição')
st.write('Aplicativo de análise de dados agrícolas, com base em dados simulados.')
st.markdown("""
Desenvolvemos essa aplicação para realizar uma análise exploratória dos dados, e aplicar um modelo de machine learning, para prever a necessidade de irrigação, usando como os valores captados nos sensores.
""")
