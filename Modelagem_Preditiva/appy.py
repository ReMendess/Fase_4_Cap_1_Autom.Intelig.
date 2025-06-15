
import streamlit as st
from pagina_1_exploratoria import mostrar_pagina_exploratoria
from pagina_2_modelo import mostrar_pagina_modelo

st.set_page_config(page_title="Monitoramento de Sensores", layout="wide")

paginas = {
    "Análise Exploratória": mostrar_pagina_exploratoria,
    "Análise Preditiva": mostrar_pagina_modelo
}

pagina = st.sidebar.radio("Escolha a página:", list(paginas.keys()))
paginas[pagina]()

