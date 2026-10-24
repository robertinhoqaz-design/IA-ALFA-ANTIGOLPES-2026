import streamlit as st
import requests
import re
import html

try:
    from ddgs import DDGS
except ImportError:
    DDGS = None

# Configuração da página
st.set_page_config(
    page_title="IA ALFA Antigolpes",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

OLLAMA_URL = "http://localhost:11434/api/chat"
MODELO_IA = "qwen2.5:0.5b"

# Estilo da interface
st.markdown("""
<style>
.stApp {
    background: linear-gradient(145deg, #07101e, #102747, #07101e);
    color: #f0f6ff;
}
header[data-testid="stHeader"] {
    background: transparent;
}
section.main > div.block-container {
    width: 96%;
    max-width: 1250px;
    padding: 1.5rem 1rem 3rem 1rem;
    margin: auto;
}
h1, h2, h3, p, label {
    color: #edf5ff;
}
.alfa-titulo {
    text-align: center;
    font-size: clamp(30px, 5vw, 48px);
    font-weight: 900;
    color: #6bd5ff;
    text-shadow: 0 0 16px #087bff;
    margin: 0;
}
.alfa-descricao {
    text-align: center;
    color: #b8d8ff;
    font-size: 16px;
    margin: 8px 0 20px 0;
}
.stTextArea textarea {
    background: #0b192d;
    color: white;
    border: 1px solid #3677b8;
    border-radius: 12px;
    font-size: 16px;
}
.stButton button, .stFormSubmitButton button {
    width: 100%;
    min-height: 45px;
    background: linear-gradient(90deg, #087bff, #00b9ff);
    color: white;
    border: none;
    border-radius: 10px;
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)

def analisar_golpe(texto):
    texto = texto.lower()
    sinais = []
    regras = [
        (["pix", "transferência", "transferencia", "depósito", "deposito"], "Menção a Pix, depósito ou transferência."),
        (["senha", "token", "código de segurança"], "Menção a senha ou código de segurança."),
        (["prêmio", "premio", "ganhou", "sorteio"], "Possível promessa de prêmio ou dinheiro."),
        (["urgente", "imediatamente", "última chance"], "Pressão para agir rapidamente."),
        (["conta bloqueada", "cartão bloqueado"], "Possível ameaça de bloqueio de conta ou cartão."),
        (["clique aqui", "acesse o link"], "Pedido para clicar em link ou confirmar dados.")
    ]
    for palavras, descricao in regras:
        if any(p in texto for p in palavras):
            sinais.append(descricao)
    if not sinais:
        sinais.append("Nenhum sinal conhecido foi identificado pelas regras básicas.")
    return sinais

if "historico_alfa" not in st.session_state:
    st.session_state.historico_alfa = []
if "ultima_resposta" not in st.session_state:
    st.session_state.ultima_resposta = ""

st.markdown('<div class="alfa-titulo">IA ALFA</div>', unsafe_allow_html=True)
st.markdown('<div class="alfa-descricao">ANTIGOLPES • ASSISTENTE DE SEGURANÇA DIGITAL</div>', unsafe_allow_html=True)

st.markdown("### 🔎 Analisar mensagem")
with st.form("formulario_analise"):
    pergunta = st.text_area("Mensagem ou pergunta", placeholder="Exemplo: Seu banco bloqueou sua conta...", height=160)
    enviar = st.form_submit_button("🛡️ ANALISAR AGORA")

if enviar and pergunta.strip():
    pergunta = pergunta.strip()
    sinais = analisar_golpe(pergunta)
    
    resposta = "### 🛡️ Análise de Segurança\n\n"
    resposta += "**Sinais identificados na mensagem:**\n"
    for s in sinais:
        resposta += f"- {s}\n"
    
    st.session_state.ultima_resposta = resposta
    st.session_state.historico_alfa.append({"pergunta": pergunta, "resposta": resposta})
    st.rerun()

if st.session_state.ultima_resposta:
    st.markdown("---")
    st.markdown("### 📊 Resultado da Análise")
    st.markdown(st.session_state.ultima_resposta)
