import streamlit as st
import requests
import time
from datetime import datetime
import pandas as pd

st.set_page_config(page_title="Portal OLSIF", layout="centered")

URL_FIREBASE = "https://portal-olsif-default-rtdb.firebaseio.com/sensores.json"

if 'historico_eventos' not in st.session_state:
    st.session_state.historico_eventos = []
if 'ultima_temp' not in st.session_state:
    st.session_state.ultima_temp = None
if 'ultima_vel' not in st.session_state:
    st.session_state.ultima_vel = None

def converter_para_numero(valor):
    if valor is None:
        return None
    try:
        if isinstance(valor, str):
            valor = valor.lower().replace('o', '0').strip()
        return float(valor)
    except:
        return None

# --- CABEÇALHO SEGURO CONTRA QUEBRAS DE LINHA ---
st.markdown("<div style='background-color: #004d26; padding: 15px; border-radius: 5px; text-align: center; margin-bottom: 20px;'><h1 style='color: white; margin: 0; font-family: sans-serif; font-size: 30px;'>Portal OLSIF</h1></div>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center; font-weight: bold; margin-bottom: 5px;'>Mini Gêmeo Digital Ferroviário (Fase 3)</h3>", unsafe_allow_html=True)

hora_atual_sistema = datetime.now().strftime('%H:%M:%S')

# Usando aspas triplas para evitar o erro se o editor quebrar a linha
texto_sub = f"""Monitoramento Analógico - Carga: Etanol (UN 1170) - Vagão: BR-998 
| Evento: Anitta | Data: 19/06/2026 | Horário: {hora_atual_sistema}"""

st.markdown(f"<p style='text-align: center; font-size: 14px; font-weight: bold; color: #004d26;'>{texto_sub}</p>", unsafe_allow_html=True)

limite_temp_monitorar = 40.0
limite_temp_pare = 60.0
lim
