import streamlit as st
import requests
import time
from datetime import datetime
import pandas as pd

st.set_page_config(page_title="Portal OLSIF", layout="centered")

# URL corrigida apontando direto para a pasta de sensores do seu Firebase
URL_FIREBASE = "https://portal-olsif-default-rtdb.firebaseio.com/sensores.json"

# Inicializa o histórico na memória se ele não existir
if 'historico_eventos' not in st.session_state:
    st.session_state.historico_eventos = []
if 'ultima_temp' not in st.session_state:
    st.session_state.ultima_temp = None
if 'ultima_vel' not in st.session_state:
    st.session_state.ultima_vel = None

# --- FUNÇÃO DE TRATAMENTO SEGURO DE TEXTO PARA NÚMERO ---
def converter_para_numero(valor):
    if valor is None:
        return None
    try:
        if isinstance(valor, str):
            valor = valor.lower().replace('o', '0').strip()
        return float(valor)
    except:
        return None

# Cabeçalho do Portal OLSIF
st.markdown("<div style='background-color: #004d26; padding: 15px; border-radius: 5px; text-align: center; margin-bottom: 20px;'><h1 style='color: white; margin: 0; font-family: sans-serif; font-size: 30px;'>Portal OLSIF</h1></div>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center; font-weight: bold; margin-bottom: 5px;'>Mini Gêmeo Digital Ferroviário (Fase 3)</h3>", unsafe_allow_html=True)

# --- ALTERAÇÃO AQUI: Cabeçalho dinâmico com Evento Anitta, Data fixa e Horário do sistema atualizando ---
hora_atual
