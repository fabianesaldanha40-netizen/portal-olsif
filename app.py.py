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
    if valor is None: return None
    try:
        if isinstance(valor, str):
            valor = valor.lower().replace('o', '0').strip()
        return float(valor)
    except: return None

# --- CABEÇALHO COMPACTO (LINHAS CURTAS PARA EVITAR CORTES) ---
st.markdown("<h1 style='text-align: center; color: #004d26;'>Portal OLSIF</h1>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align: center;'>Gêmeo Digital Ferroviário (Fase 3)</h4>", unsafe_allow_html=True)

H_AGORA = datetime.now().strftime('%H:%M:%S')
INFO_TXT = f"Vagão: BR-998 | Evento: Anitta | Data: 19/06/2026 | Horário: {H_AGORA}"
st.markdown(f"<p style='text-align: center; font-weight: bold; color: #004d26;'>{INFO_TXT}</p>", unsafe_allow_html=True)

# Limites Fixos Regulamentares
L_TEMP_M = 40.0
L_TEMP_P = 60.0
L_VEL = 80.0

temp_exibida, vel_exibida = "— °C", "— km/h"
status_texto = "STATUS: AGUARDANDO DADOS"
cor_painel = "#6c757d"
cor_caixa_temp, cor_caixa_vel = "#f8f9fa", "#f8f9fa"
cor_texto_temp, cor_texto_vel = "#333333", "#333333"
status_conexao_temp, status_conexao_vel = "CONECTANDO...", "CONECTANDO..."

try:
    resposta = requests.get(URL_FIREBASE, timeout=5).json()
    if resposta and isinstance(resposta, dict):
        t_raw = resposta.get('temperatura_atual', resposta.get('temperatura atual', None))
        v_raw = resposta.get('velocidade_atual', resposta.get('velocidade', None))
        temp_atual = converter_para_numero(t_raw)
        vel_atual = converter_para_numero(v_raw)
    else:
        temp_atual, vel_atual = None, None

    data_hora_log = datetime.now().strftime('%d/%m/%Y - %H:%M:%S')

    if temp_atual is not None or vel_atual is not None:
        if temp_atual is not None: temp_exibida = f"{temp_atual} °C"
        if vel_atual is not None: vel_exibida = f"{vel_atual} km/h"
        
        if (temp_atual and temp_atual >= L_TEMP_P) or (vel_atual and vel_atual >= L_VEL):
            status_texto = "STATUS OPERACIONAL: PARE / RETIDO"
            cor_painel = "#b00020"
        elif temp_atual and temp_atual >= L_TEMP_M:
            status_texto = "STATUS OPERACIONAL: MONITORAR"
            cor_painel = "#f39c12"
        else:
            status_texto = "STATUS OPERACIONAL: LIBERADO"
            cor_painel = "#2e9d52"

        if temp_atual and temp_atual >= L_TEMP_P:
            cor_caixa_temp, cor_texto_temp = "#fde8e8", "#b00020"
            status_conexao_temp = "CRÍTICO"
        elif temp_atual and temp_atual >= L_TEMP_M:
            cor




