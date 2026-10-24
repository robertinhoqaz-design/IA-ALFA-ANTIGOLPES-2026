import streamlit as st
import streamlit.components.v1 as components
import requests
import re
import html

try:
    from ddgs import DDGS
except ImportError:
    DDGS = None

st.set_page_config(
    page_title="IA ALFA Antigolpes",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

OLLAMA_URL = "http://localhost:11434/api/chat"
MODELO_IA = "qwen2.5:0.5b"

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
.stButton button,
.stFormSubmitButton button {
    width: 100%;
    min-height: 45px;
    background: linear-gradient(90deg, #087bff, #00b9ff);
    color: white;
    border: none;
    border-radius: 10px;
    font-weight: bold;
}
div[data-testid="stSidebar"] {
    background: #081426;
}
</style>
""", unsafe_allow_html=True)

globo_html = """
<!DOCTYPE html>
<html>
<head>
<style>
html, body { margin: 0; padding: 0; background: transparent; overflow: hidden; }
.palco { height: 330px; display: flex; align-items: center; justify-content: center; }
.globo {
    width: 245px; height: 245px; border-radius: 50%; position: relative; overflow: hidden;
    background: radial-gradient(circle at 30% 25%, #a5edff, #1689ff 23%, #0750b5 52%, #06183e 78%, #020916);
    box-shadow: 0 0 25px #168bff, 0 0 60px rgba(0, 125, 255, 0.5);
    animation: flutuar 4s ease-in-out infinite;
}
@keyframes flutuar { 0%, 100% { translate: 0 0; } 50% { translate: 0 -8px; } }
</style>
</head>
<body>
<div class="palco"><div class="globo"></div></div>
</body>
</html>
"""

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

def pesquisar_internet(consulta):
    fontes = []
    if DDGS is None:
        return fontes
    try:
        with DDGS() as busca:
            resultados = busca.text(consulta + " golpe fraude Brasil", region="br-pt", max_results=3)
            for item in resultados:
                fontes.append({"titulo": item.get("title", "Resultado"), "url": item.get("href", ""), "resumo": item.get("body", "")})
    except Exception:
        pass
    return fontes

def consultar_ia(pergunta, sinais, fontes):
    contexto_fontes = "".join(f"\nTítulo: {f['titulo']}\nResumo: {f['resumo']}\n" for f in fontes)
    contexto_sinais = "\n".join(f"- {s}" for s in sinais)
    mensagens = [
        {"role": "system", "content": f"Você é a IA ALFA, especialista em prevenção de golpes digitais. Sinais encontrados:\n{contexto_sinais}\n\nFontes:\n{contexto_fontes}"},
        {"role": "user", "content": pergunta}
    ]
    resposta = requests.post(OLLAMA_URL, json={"model": MODELO_IA, "messages": mensagens, "stream": False}, timeout=120)
    resposta.raise_for_status()
    return resposta.json()["message"]["content"]

if "historico_alfa" not in st.session_state:
    st.session_state.historico_alfa = []
if "ultima_resposta" not in st.session_state:
    st.session_state.ultima_resposta = ""

st.markdown('<div class="alfa-titulo">IA ALFA</div>', unsafe_allow_html=True)
st.markdown('<div class="alfa-descricao">ANTIGOLPES • ASSISTENTE DE SEGURANÇA DIGITAL</div>', unsafe_allow_html=True)
components.html(globo_html, height=335, scrolling=False, key="globo_header")

st.markdown("### 🔎 Analisar mensagem")
with st.form("formulario_analise"):
    pergunta = st.text_area("Mensagem ou pergunta", placeholder="Exemplo: Seu banco bloqueou sua conta...", height=160)
    enviar = st.form_submit_button("🛡️ ANALISAR AGORA")

if enviar and pergunta.strip():
    pergunta = pergunta.strip()
    sinais = analisar_golpe(pergunta)
    with st.spinner("Analisando a mensagem..."):
        fontes = pesquisar_internet(pergunta)
        try:
            resposta = consultar_ia(pergunta, sinais, fontes)
        except Exception:
            resposta = "Não foi possível consultar a IA local. Verifique se o Ollama está aberto."
    
    st.session_state.ultima_resposta = resposta
    st.session_state.historico_alfa.append({"pergunta": pergunta, "resposta": resposta})
    st.rerun()

if st.session_state.ultima_resposta:
    st.markdown("---")
    st.markdown("### 🔊 Última resposta")
    st.markdown(st.session_state.ultima_resposta)
