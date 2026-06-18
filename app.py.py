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

# Horário dinâmico que atualiza na tela
horario_atual_tela = datetime.now().strftime('%H:%M:%S')
st.markdown(f"<p style='text-align: center; font-size: 14px;'>Monitoramento Analógico de Segurança - Carga: Etanol (UN 1170) - Vagão: BR-998 | Horário: {horario_atual_tela}</p>", unsafe_allow_html=True)

# Limites Fixos Regulamentares
limite_temp_monitorar = 40.0
limite_temp_pare = 60.0
limite_velocidade = 80.0

# Valores padrão de exibição antes da checagem
temp_exibida, vel_exibida = "— °C", "— km/h"
status_texto = "STATUS OPERACIONAL DO TREM: AGUARDANDO DADOS"
cor_painel = "#6c757d"
cor_caixa_temp, cor_caixa_vel = "#f8f9fa", "#f8f9fa"
cor_texto_temp, cor_texto_vel = "#333333", "#333333"
status_conexao_temp, status_conexao_vel = "CONECTANDO...", "CONECTANDO..."
temp_atual, vel_atual = None, None

try:
    resposta = requests.get(URL_FIREBASE, timeout=5).json()
    
    if resposta and isinstance(resposta, dict):
        t_raw = resposta.get('temperatura_atual', resposta.get('temperatura atual', None))
        v_raw = resposta.get('velocidade_atual', resposta.get('velocidade', None))
        
        temp_atual = converter_para_numero(t_raw)
        vel_atual = converter_para_numero(v_raw)

    data_hora_agora = datetime.now().strftime('%d/%m/%Y - %H:%M:%S')

    if temp_atual is not None or vel_atual is not None:
        if temp_atual is not None: temp_exibida = f"{temp_atual} °C"
        if vel_atual is not None: vel_exibida = f"{vel_atual} km/h"
        
        if (temp_atual and temp_atual >= limite_temp_pare) or (vel_atual and vel_atual >= limite_velocidade):
