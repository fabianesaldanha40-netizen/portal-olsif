import streamlit as st
import pandas as pd
import time
import random

# Configuração da página do Portal OLSIF
st.set_page_config(
    page_title="Portal OLSIF - Telemetria Ferroviária",
    page_icon="🚂",
    layout="wide"
)

# --- CABEÇALHO ---
st.title("🚂 Ecossistema Digital OLSIF")
st.subheader("Sistema Automatizado de Telemetria e Segurança - Transporte de Etanol (UN 1170)")
st.markdown("---")

# --- HISTÓRICO / TELEMETRIA SIMULADA ---
# Gerando dados fictícios seguros para monitoramento
dados_torres = {
    "Vagão ID": ["BR-998", "BR-998", "BR-998"],
    "Posto de Controle / Torre IoT": ["Pátio Uruguaiana (Torre 01)", "Via Permanente (Torre 02)", "Zona de Fronteira (Torre 03)"],
    "Status da Carga (Art. 6º)": ["Carga Perigosa Ativa", "Carga Perigosa Ativa", "Carga Perigosa Ativa"],
    "Pressão Manométrica (Seção 1.2.2.4)": ["1.2 bar", "1.5 bar", "1.1 bar"],
    "Temperatura": ["21.4 °C", "22.8 °C", "21.9 °C"]
}
df_telemetria = pd.DataFrame(dados_torres)

# Layout em colunas para os dados operacionais
col1, col2 = st.columns([2, 1])

with col1:
    st.write("### 📊 Últimas Leituras das Torres IoT (Protocolo LoRaWAN)")
    st.table(df_telemetria)
    
    st.info("ℹ️ **Nota de Engenharia:** Conforme a Seção 1.2.2.4, todas as pressões relativas aos vasos de pressão são calculadas em pressão manométrica.")

with col2:
    st.write("### 🚨 Lógicas Ativas de Risco (Sloshing & Velocidade)")
    st.metric(label="Status do Comboio", value="CONFORME", delta="Teto Rígido Ativo")
    st.warning("⚠️ Monitoramento de Sloshing ativo: Coeficiente de expansão térmica sob supervisão contínua.")

st.markdown("---")

# --- CONEXÃO COM O ASSISTENTE COGNITIVO (OLSIF-GPT) ---
st.write("### 🤖 OLSIF-GPT: Auditor Fiscal Sênior da ANTT")
st.caption("Assistente cognitivo especializado em conformidade e validação da Resolução nº 5.998/22.")

# Inicializar o histórico de chat se não existir
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Saudações. Sou o Auditor Fiscal Sênior da ANTT integrado ao painel OLSIF. Em que posso ajudar na validação regulatória do transporte ferroviário de Etanol (UN 1170) hoje?"}
    ]

# Exibir mensagens anteriores
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# Lógica básica de respostas restritas à norma legal do OLSIF
if prompt := st.chat_input("Digite sua dúvida sobre EPIs, sinalização ou retenção do vagão..."):
    # Exibir comando do usuário
    with st.chat_message("user"):
        st.write(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Processamento da resposta restrita
    prompt_lower = prompt.lower()
    with st.chat_message("assistant"):
        with st.spinner("Consultando base regulatória da ANTT..."):
            time.sleep(0.8)
            
            if "epi" in prompt_lower or "equipamento" in prompt_lower:
                resposta = "Conforme o Artigo 9º da Resolução ANTT nº 5.998/22, a presença e a conformidade dos Equipamentos de Proteção Individual (EPIs) adequados ao produto inflamável (Classe 3) são requisitos obrigatórios antes da liberação do comboio ferroviário."
            elif "sinalização" in prompt_lower or "placa" in prompt_lower or "painel" in prompt_lower:
                resposta = "De acordo com o Artigo 6º da Resolução ANTT nº 5.998/22, a sinalização composta por painéis de segurança laranjas (Número ONU 1170 / Risco 33) deve permanecer ativa mesmo com o vagão vazio, caso persistam resíduos ou contaminação."
            elif "retenção" in prompt_lower or "vazamento" in prompt_lower or "artigo 40" in prompt_lower:
                resposta = "Sob a ocorrência de desconformidades graves ou vazamentos técnicos de fluido manométrico, aplica-se o Artigo 40 da regulamentação vigente, determinando a retenção imediata e o isolamento físico do vagão-tanque afetado."
            else:
                resposta = "Alerta: A indagação apresentada está fora do escopo de conformidade ativa mapeado pela ANTT. Como assistente auditor restrito, estou vedado de criar ou estender artigos, sanções ou interpretações jurídicas não documentadas na Resolução nº 5.998/22."
            
            st.write(resposta)
            st.session_state.messages.append({"role": "assistant", "content": resposta})
