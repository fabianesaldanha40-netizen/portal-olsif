import streamlit as st
import requests
import time
from datetime import datetime, timedelta, timezone
import pandas as pd

st.set_page_config(page_title="Portal OLSIF", layout="centered")

# URL oficial do seu Firebase (.json no final)
URL_FIREBASE = "https://portal-olsif-default-rtdb.firebaseio.com/.json"

# Inicializa o histórico na memória se ele não existir
if 'historico_eventos' not in st.session_state:
    st.session_state.historico_eventos = []
if 'ultima_temp' not in st.session_state:
    st.session_state.ultima_temp = None
if 'ultima_vel' not in st.session_state:
    st.session_state.ultima_vel = None

# --- FUNÇÃO DE TRATAMENTO SEGURO DE TEXTO PARA NÚMERO ---
def converter_para_numero(valor):
    if valor is None: return None
    try:
        if isinstance(valor, str): valor = valor.lower().replace('o', '0').strip()
        return float(valor)
    except: return None

# Cabeçalho do Portal OLSIF
st.markdown("<div style='background-color: #004d26; padding: 15px; border-radius: 5px; text-align: center; margin-bottom: 20px;'><h1 style='color: white; margin: 0; font-family: sans-serif; font-size: 30px;'>Portal OLSIF</h1></div>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center; font-weight: bold; margin-bottom: 5px;'>Mini Gêmeo Digital Ferroviário (Fase 3)</h3>", unsafe_allow_html=True)

# Captura o horário correto de Brasília (GMT-3) baseado no UTC global
fuso_br = datetime.now(timezone.utc) - timedelta(hours=3)
hora_agora = fuso_br.strftime('%H:%M:%S')

st.markdown(f"<p style='text-align: center; font-size: 14px;'>Monitoramento Analógico de Segurança - Carga: Etanol (UN 1170) - Vagão: BR-998 | Horário: {hora_agora}</p>", unsafe_allow_html=True)

# Limites Fixos Regulamentares com nomes originais mantidos
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
        dados = resposta.get('sensores', resposta)
        
        if isinstance(dados, dict):
            # Mapeamento exato do seu Firebase
            t_raw = dados.get('temperatura atual', dados.get('temperatura_atual', None))
            v_raw = dados.get('velocidade_atual', dados.get('velocidade', None))
            
            temp_atual = converter_para_numero(t_raw)
            vel_atual = converter_para_numero(v_raw)

    if temp_atual is not None or vel_atual is not None:
        if temp_atual is not None: temp_exibida = f"{temp_atual} °C"
        if vel_atual is not None: vel_exibida = f"{vel_atual} km/h"
        
        # --- ÁRVORE DE DECISÃO AUTOMATIZADA ---
        if (temp_atual and temp_atual >= limite_temp_pare) or (vel_atual and vel_atual >= limite_velocidade):
            status_texto = "STATUS OPERACIONAL: PARE / RETIDO"
            cor_painel = "#b00020"
        elif temp_atual and temp_atual >= limite_temp_monitorar:
            status_texto = "STATUS OPERACIONAL: MONITORAR"
            cor_painel = "#f39c12"
        else:
            status_texto = "STATUS OPERACIONAL: LIBERADO"
            cor_painel = "#2e9d52"

        # Cores dinâmicas para as caixinhas estruturadas
        if temp_atual and temp_atual >= limite_temp_pare:
            cor_caixa_temp, cor_texto_temp = "#fde8e8", "#b00020"
            status_conexao_temp = "CRÍTICO"
        elif temp_atual and temp_atual >= limite_temp_monitorar:
            cor_caixa_temp, cor_texto_temp = "#fef3c7", "#d97706"
            status_conexao_temp = "MONITORAR"
        else:
            cor_caixa_temp, cor_texto_temp = "#def7ec", "#03543f"
            status_conexao_temp = "CONECTADO"

        if vel_atual and vel_atual >= limite_velocidade:
            cor_caixa_vel, cor_texto_vel = "#fde8e8", "#b00020"
            status_conexao_vel = "EXCESSO VEL."
        else:
            cor_caixa_vel, cor_texto_vel = "#def7ec", "#03543f"
            status_conexao_vel = "CONECTADO"

        # Inserção no histórico estruturado para preencher a tabela
        if temp_atual != st.session_state.ultima_temp and temp_atual is not None:
            msg = f"Temperatura alterada para {temp_atual} °C. Status: {status_conexao_temp}."
            st.session_state.historico_eventos.insert(0, {"Hora": hora_agora, "Componente": "Sensor Temp.", "Descrição / Logs": msg})
            st.session_state.ultima_temp = temp_atual

        if vel_atual != st.session_state.ultima_vel and vel_atual is not None:
            msg = f"Velocidade alterada para {vel_atual} km/h. Limites validados."
            st.session_state.historico_eventos.insert(0, {"Hora": hora_agora, "Componente": "Sensor Vel.", "Descrição / Logs": msg})
            st.session_state.ultima_vel = vel_atual
    else:
        status_texto = "STATUS OPERACIONAL: AGUARDANDO SINAL"
        cor_painel = "#6c757d"
        status_conexao_temp, status_conexao_vel = "SEM SINAL", "SEM SINAL"

except Exception:
    status_texto = "STATUS OPERACIONAL: ERRO DE CONEXÃO"
    cor_painel = "#b00020"
    cor_caixa_temp, cor_caixa_vel = "#fde8e8", "#fde8e8"
    cor_texto_temp, cor_texto_vel = "#b00020", "#b00020"
    status_conexao_temp, status_conexao_vel = "ERRO", "ERRO"

# Barra de status grande do topo
st.markdown(f"<div style='background-color: {cor_painel}; padding: 15px; border-radius: 8px; text-align: center; margin-bottom: 25px;'><h2 style='color: white; margin: 0; font-size: 22px; font-weight: bold;'>{status_texto}</h2></div>", unsafe_allow_html=True)

# Caixinhas dos sensores estruturadas em colunas
col1, col2 = st.columns(2)

with col1:
    html_temp = "<div style='background-color: " + cor_caixa_temp + "; border: 1px solid " + cor_texto_temp + "40; padding: 25px; border-radius: 12px; text-align: center; margin-bottom: 10px;'>"
    html_temp += "<p style='margin: 0; font-size: 13px; font-weight: bold; color: #555555; text-transform: uppercase;'>⚙️ SENSOR DE TEMPERATURA</p>"
    html_temp += "<h1 style='margin: 15px 0; font-size: 42px; color: " + cor_texto_temp + "; font-weight: bold;'>" + temp_exibida + "</h1></div>"
    st.markdown(html_temp, unsafe_allow_html=True)
    
    if status_conexao_temp in ["CRÍTICO", "ERRO"]: st.error(f"Alerta: {status_conexao_temp}")
    elif status_conexao_temp == "MONITORAR": st.warning("Alerta: MONITORAR")
    else: st.success(f"Status: {status_conexao_temp}")

with col2:
    html_vel = "<div style='background-color: " + cor_caixa_vel + "; border: 1px solid " + cor_texto_vel + "40; padding: 25px; border-radius: 12px; text-align: center; margin-bottom: 10px;'>"
    html_vel += "<p style='margin: 0; font-size: 13px; font-weight: bold; color: #555555; text-transform: uppercase;'>⚡ SENSOR DE VELOCIDADE</p>"
    html_vel += "<h1 style='margin: 15px 0; font-size: 42px; color: " + cor_texto_vel + "; font-weight: bold;'>" + vel_exibida + "</h1></div>"
    st.markdown(html_vel, unsafe_allow_html=True)
    
    if status_conexao_vel in ["EXCESSO VEL.", "ERRO"]: st.error(f"Alerta: {status_conexao_vel}")
    else: st.success(f"Status: {status_conexao_vel}")

st.markdown("<br>", unsafe_allow_html=True)

# --- TABELA DE EVENTOS ORGANIZADA DA ANTT ---
st.markdown("### 📋 Registro de Eventos da ANTT (Resolução nº 5.998/22)")

if st.session_state.historico_eventos:
    df_historico = pd.DataFrame(st.session_state.historico_eventos[:5])
    st.dataframe(df_historico, width="stretch", hide_index=True)
else:
    st.info("Aguardando alteração de dados no Firebase para gerar os logs na tabela...")

# Rodapé
st.markdown("<br><br><div style='background-color: #343a40; padding: 20px; text-align: center; margin-top: 30px;'><p style='color: white; margin: 0; font-size: 13px;'>© 2026 OLSIF - Logística Ferroviária Inteligente.</p></div>", unsafe_allow_html=True)

time.sleep(2)
st.rerun()
