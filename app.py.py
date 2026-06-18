import streamlit as st
import requests as req
import time
from datetime import datetime as dt
from datetime import timedelta as td
import pandas as pd

# Configuração Inicial
st.set_page_config(
    page_title="Portal OLSIF",
    layout="centered"
)

# Endpoint Firebase
URL = (
    "https://portal-olsif-default-rtdb."
    "firebaseio.com/sensores.json"
)

# Inicialização de Estado (Session State)
if 'historico_eventos' not in st.session_state:
    st.session_state.historico_eventos = []
if 'ultima_temp' not in st.session_state:
    st.session_state.ultima_temp = None
if 'ultima_vel' not in st.session_state:
    st.session_state.ultima_vel = None

# Função de Tratamento Numérico
def num(v):
    if v is None:
        return None
    try:
        if isinstance(v, str):
            v = v.lower().replace('o', '0').strip()
        return float(v)
    except:
        return None

# Renderização do Cabeçalho
st.markdown(
    "<div style='background-color:#004d26;"
    "padding:15px;border-radius:5px;"
    "text-align:center;margin-bottom:20px;'>"
    "<h1 style='color:white;margin:0;"
    "font-family:sans-serif;font-size:30px;'>"
    "Portal OLSIF</h1></div>",
    unsafe_allow_html=True
)

st.markdown(
    "<h3 style='text-align:center;"
    "font-weight:bold;margin-bottom:5px;'>"
    "Mini Gêmeo Digital Ferroviário "
    "(Fase 3)</h3>",
    unsafe_allow_html=True
)

# Cálculo de Fuso Horário (Brasília GMT-3)
fuso = dt.utcnow() - td(hours=3)
hora = fuso.strftime('%H:%M:%S')

st.markdown(
    f"<p style='text-align:center;"
    f"font-size:14px;'>"
    f"Monitoramento Analógico de "
    f"Segurança - Carga: Etanol "
    f"(UN 1170) - Vagão: BR-998 | "
    f"Horário: {hora}</p>",
    unsafe_allow_html=True
)

# Definição de Parâmetros e Limites Regulamentares
lim_m = 40.0
lim_p = 60.0
lim_v = 80.0

# Inicialização de Variáveis de Exibição
t_txt, v_txt = "— °C", "— km/h"
status = "STATUS OPERACIONAL: AGUARDANDO DADOS"
c_pnl = "#6c757d"
c_cx_t, c_cx_v = "#f8f9fa", "#f8f9fa"
c_tx_t, c_tx_v = "#333333", "#333333"
st_t, st_v = "CONECTANDO...", "CONECTANDO..."
t_val, v_val = None, None

# Bloco Principal de Captura de Dados
try:
    res = req.get(URL, timeout=5).json()
    if res and isinstance(res, dict):
        t_raw = res.get(
            'temperatura_atual',
            res.get('temperatura atual', None)
        )
        v_raw = res.get(
            'velocidade_atual',
            res.get('velocidade', None)
        )
        t_val = num(t_raw)
        v_val = num(v_raw)

    log_dt = fuso.strftime('%d/%m/%Y - %H:%M:%S')

    if t_val is not None or v_val is not None:
        if t_val is not None:
            t_txt = f"{t_val} °C"
        if v_val is not None:
            v_txt = f"{v_val} km/h"
        
        is_p_t = t_val and t_val >= lim_p
        is_p_v = v_val and v_val >= lim_v
        
        if is_p_t or is_p_v:
            status = "STATUS OPERACIONAL: PARE / RETIDO"
            c_pnl = "#b00020"
        elif t_val and t_val >= lim_m:
            status = "STATUS OPERACIONAL: MONITORAR"
            c_pnl = "#f39c12"
        else:
            status = "STATUS OPERACIONAL: LIBERADO"
            c_pnl = "#2e9d52"

        if t_val and t_val >= lim_p:
            c_cx_t, c_tx_t = "#fde8e8", "#b00020"
            st_t = "CRÍTICO"
        elif t_val and t_val >= lim_m:
            c_cx_t, c_tx_t = "#fef3c7", "#d97706"
            st_t = "MONITORAR"
        else:
            c_cx_t, c_tx_t = "#def7ec", "#03543f"
            st_t = "CONECTADO"

        if v_val and v_val >= lim_v:
            c_cx_v, c_tx_v = "#fde8e8", "#b00020"
            st_v = "EXCESSO VEL."
        else:
            c_cx_v, c_tx_v = "#def7ec", "#03543f"
            st_v = "CONECTADO"

        hist = st.session_state.historico_eventos
        if t_val != st.session_state.ultima_temp and t_val is not None:
            m_t = f"Temp alterada para {t_val}C. Status: {st_t}."
            hist.insert(0, {"Data e Hora": log_dt, "Componente": "Sensor Temp.", "Descrição / Logs": m_t})
            st.session_state.ultima_temp = t_val

        if v_val != st.session_state.ultima_vel and v_val is not None:
            m_v = f"Vel alterada para {v_val}km/h. Limites validados."
            hist.insert(0, {"Data e Hora": log_dt, "Componente": "Sensor Vel.", "Descrição / Logs": m_v})
            st.session_state.ultima_vel = v_val
    else:
        status = "STATUS OPERACIONAL: AGUARDANDO SINAL"
        c_pnl = "#6c757d"
        st_t, st_v = "SEM SINAL", "SEM SINAL"

except Exception:
    status = "STATUS OPERACIONAL: ERRO DE CONEXÃO"
    c_pnl = "#b00020"
    c_cx_t, c_cx_v = "#fde8e8", "#fde8e8"
    c_tx_t, c_tx_v = "#b00020", "#b00020"
    st_t, st_v = "ERRO", "ERRO"

# Interface Gráfica - Painel de Status Geral
st.markdown(
    f"<div style='background-color:{c_pnl};"
    f"padding:15px;border-radius:8px;"
    f"text-align:center;margin-bottom:25px;'>"
    f"<h2 style='color:white;margin:0;"
    f"font-size:22px;font-weight:bold;'>"
    f"{status}</h2></div>",
    unsafe_allow_html=True
)

col1, col2 = st.columns(2)

# Bloco da Temperatura
