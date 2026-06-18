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

# --- CABEÇALHO ---
st.markdown("<h1 style='text-align: center; color: #004d26;'>Portal OLSIF</h1>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align: center;'>Gêmeo Digital Ferroviário (Fase 3)</h4>", unsafe_allow_html=True)

H_AGORA = datetime.now().strftime('%H:%M:%S')
INFO_TXT = f"Vagão: BR-998 | Evento: Anitta | Data: 19/06/2026 | Horário: {H_AGORA}"
st.markdown(f"<p style='text-align: center; font-weight: bold; color: #004d26;'>{INFO_TXT}</p>", unsafe_allow_html=True)

# Limites Regulamentares
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
            cor_caixa_temp, cor_texto_temp = "#fef3c7", "#d97706"
            status_conexao_temp = "MONITORAR"
        else:
            cor_caixa_temp, cor_texto_temp = "#def7ec", "#03543f"
            status_conexao_temp = "CONECTADO"

        if vel_atual and vel_atual >= L_VEL:
            cor_caixa_vel, cor_texto_vel = "#fde8e8", "#b00020"
            status_conexao_vel = "EXCESSO VEL."
        else:
            cor_caixa_vel, cor_texto_vel = "#def7ec", "#03543f"
            status_conexao_vel = "CONECTADO"

        if temp_atual != st.session_state.ultima_temp and temp_atual is not None:
            msg = f"Temp alterada para {temp_atual} °C. Status: {status_conexao_temp}."
            st.session_state.historico_eventos.insert(0, {"Data e Hora": data_hora_log, "Componente": "Sensor Temp.", "Descrição / Logs": msg})
            st.session_state.ultima_temp = temp_atual

        if vel_atual != st.session_state.ultima_vel and vel_atual is not None:
            msg = f"Velocidade alterada para {vel_atual} km/h."
            st.session_state.historico_eventos.insert(0, {"Data e Hora": data_hora_log, "Componente": "Sensor Vel.", "Descrição / Logs": msg})
            st.session_state.ultima_vel = vel_atual
    else:
        status_texto = "STATUS: AGUARDANDO SINAL"
        cor_painel = "#6c757d"
        status_conexao_temp, status_conexao_vel = "SEM SINAL", "SEM SINAL"

except Exception as erro:
    status_texto = "STATUS: ERRO DE CONEXÃO"
    cor_painel = "#b00020"
    cor_caixa_temp, cor_caixa_vel = "#fde8e8", "#fde8e8"
    cor_texto_temp, cor_texto_vel = "#b00020", "#b00020"
    status_conexao_temp, status_conexao_vel = "ERRO", "ERRO"

# --- RENDERIZAÇÃO DA INTERFACE ---
st.markdown(f"<div style='background-color: {cor_painel}; padding: 15px; border-radius: 8px; text-align: center; margin-bottom: 25px;'><h2 style='color: white; margin: 0; font-size: 20px;'>{status_texto}</h2></div>", unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    html_t = f"<div style='background-color: {cor_caixa_temp}; border: 1px solid {cor_texto_temp}40; padding: 20px; border-radius: 12px; text-align: center;'><p style='margin: 0; font-size: 12px; font-weight: bold;'>⚙️ SENSOR TEMPERATURA</p><h1 style='color: {cor_texto_temp};'>{temp_exibida}</h1></div>"
    st.markdown(html_t, unsafe_allow_html=True)
    if status_conexao_temp in ["CRÍTICO", "ERRO"]: st.error(status_conexao_temp)
    elif status_conexao_temp == "MONITORAR": st.warning("MONITORAR")
    else: st.success(status_conexao_temp)

with col2:
    html_v = f"<div style='background-color: {cor_caixa_vel}; border: 1px solid {cor_texto_vel}40; padding: 20px; border-radius: 12px; text-align: center;'><p style='margin: 0; font-size: 12px; font-weight: bold;'>⚡ SENSOR VELOCIDADE</p><h1 style='color: {cor_texto_vel};'>{vel_exibida}</h1></div>"
    st.markdown(html_v, unsafe_allow_html=True)
    if status_conexao_vel in ["EXCESSO VEL.", "ERRO"]: st.error(status_conexao_vel)
    else: st.success(status_conexao_vel)

st.markdown("<br>### 📋 Registro de Eventos ANTT")
if st.session_state.historico_eventos:
    st.dataframe(pd.DataFrame(st.session_state.historico_eventos[:5]), width="stretch", hide_index=True)
else:
    st.info("Aguardando dados do Firebase...")

time.sleep(2)
st.rerun()
