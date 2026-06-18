import streamlit as st
import requests as req
import time
from datetime import datetime as dt, timedelta as td, timezone

st.set_page_config(page_title="Portal OLSIF", layout="centered")

URL = "https://portal-olsif-default-rtdb.firebaseio.com/sensores.json"

if 'historico_eventos' not in st.session_state:
    st.session_state.historico_eventos = []
if 'ultima_temp' not in st.session_state:
    st.session_state.ultima_temp = None
if 'ultima_vel' not in st.session_state:
    st.session_state.ultima_vel = None

def num(v):
    if v is None: return None
    try:
        if isinstance(v, str): v = v.lower().replace('o', '0').strip()
        return float(v)
    except: return None

st.markdown("<div style='background-color:#004d26;padding:15px;border-radius:5px;text-align:center;margin-bottom:20px;'><h1 style='color:white;margin:0;font-family:sans-serif;font-size:30px;'>Portal OLSIF</h1></div>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align:center;font-weight:bold;margin-bottom:5px;'>Mini Gêmeo Digital Ferroviário (Fase 3)</h3>", unsafe_allow_html=True)

fuso = dt.now(timezone.utc) - td(hours=3)
hora = fuso.strftime('%H:%M:%S')

st.markdown(f"<p style='text-align:center;font-size:14px;'>Monitoramento Analógico de Segurança - Carga: Etanol (UN 1170) - Vagão: BR-998 | Horário: {hora}</p>", unsafe_allow_html=True)

lim_m, lim_p
