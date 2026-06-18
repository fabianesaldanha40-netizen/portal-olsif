import streamlit as st
import requests
import time
from datetime import datetime
from datetime import timedelta
import pandas as pd

st.set_page_config(
    page_title="Portal OLSIF",
    layout="centered"
)

# URL do seu Firebase
URL_FIREBASE = (
    "https://portal-olsif-default-rtdb."
    "firebaseio.com/sensores.json"
)

# Inicializa o historico
if 'historico_eventos' not in (
    st.session_state
):
    st.session_state.historico_eventos = []
if 'ultima_temp' not in st.session_state:
    st.session_state.ultima_temp = None
if 'ultima_vel' not in st.session_state:
    st.session_state.ultima_vel = None

# --- TRATAMENTO SEGURO ---
def converter_para_numero(valor):
    if valor is None:
        return None
    try:
        if isinstance(valor, str):
            valor = (
                valor.lower()
                .replace('o', '0')
                .strip()
            )
        return float(valor)
    except:
        return None

# Cabecalho do Portal OLSIF
st.markdown(
    "<div style='background-color: "
    "#004d26; padding: 15px; "
    "border-radius: 5px; "
    "text-align: center; "
    "margin-bottom: 20px;'>"
    "<h1 style='color: white; margin: 0; "
    "font-family: sans-serif; "
    "font-size: 30px;'>Portal OLSIF</h1>"
    "</div>",
    unsafe_allow_html=True
)
st.markdown(
    "<h3 style='text-align: center; "
    "font-weight: bold; "
    "margin-bottom: 5px;'>"
    "Mini Gemeo Digital Ferroviario "
    "(Fase 3)</h3>",
    unsafe_allow_html=True
)

# --- HORARIO DINAMICO ---
hb = (
    datetime.utcnow() - 
    timedelta(hours=3)
)
hr = hb.strftime('%H:%M:%S')

st.markdown(
    f"<p style='text-align: center; "
    f"font-size: 14px;'>"
    f"Monitoramento Analogico de "
    f"Seguranca - Carga: Etanol "
    f"(UN 1170) - Vagao: BR-998 | "
    f"Horario: {hr}</p>",
    unsafe_allow_html=True
)

# Limites Fixos Curtos
m = 40.0
p = 60.0
v = 80.0

# Valores padrao
temp_exibida = "— °C"
vel_exibida = "— km/h"
status_texto = (
    "STATUS OPERACIONAL DO TREM: "
    "AGUARDANDO DADOS"
)
cor_painel = "#6c757d"
cor_caixa_temp = "#f8f9fa"
cor_caixa_vel = "#f8f9fa"
cor_texto_temp = "#333333"
cor_texto_vel = "#333333"
status_conexao_temp = "CONECTANDO..."
status_conexao_vel = "CONECTANDO..."
temp_atual = None
vel_atual = None

try:
    resposta = requests.get(
        URL_FIREBASE, timeout=5
    ).json()
    
    if (resposta and 
            isinstance(resposta, dict)):
        t_raw = resposta.get(
