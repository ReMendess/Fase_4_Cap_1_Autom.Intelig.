# app.py
import streamlit as st
st.set_page_config(
    page_title='Aplicação de Análise e Predição',
    layout='wide'
)
st.title('Análise das REgiões')
st.write('Bem-vindo ao aplicativo de análise de dados agrícolas.')
st.markdown("""
Este aplicativo permite explorar um dataset simulado de produção agrícola,
realizar análises exploratórias e aplicar modelos preditivos.
Utilize o menu à esquerda para navegar entre as páginas.
""")
