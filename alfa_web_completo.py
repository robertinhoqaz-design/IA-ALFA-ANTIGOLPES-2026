import streamlit as st
import streamlit.components.v1 as components
import requests
import json

st.set_page_config(
    page_title="IA ALFA Mundo Digital",
    page_icon="🌐",
    layout="wide"
)

# Estilo visual moderno e limpo
st.markdown("""
<style>
    header[data-testid="stHeader"] {
        display: none !important;
    }
    .main .block-container {
        padding-top: 0.5rem !important;
        padding-bottom: 2rem !important;
        max-width: 1100px;
    }
    .stApp {
        background: radial-gradient(circle at top, #0f2347 0%, #030712 80%);
        color: #ffffff;
    }
    .header-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        margin-top: 0rem;
        margin-bottom: 1rem;
    }
    .globo-3d-gigante {
        width: 130px;
        height: 130px;
        border-radius: 50%;
        background: radial-gradient(circle at 35% 35%, #6bd5ff, #087bff 55%, #020713 100%);
        box-shadow: 0 0 50px #00b9ff, inset -15px -15px 30px rgba(0,0,0,0.8);
        margin-bottom: 12px;
        animation: floatAndGlow 4s ease-in-out infinite alternate;
    }
    @keyframes floatAndGlow {
        0% { transform: translateY(0px) scale(1); box-shadow: 0 0 35px #087bff; }
        100% { transform: translateY(-8px) scale(1.03); box-shadow: 0 0 60px #00b9ff; }
    }
    .main-title {
        text-align: center;
        color: #6bd5ff;
        font-size: 2.4rem;
        font-weight: 900;
        margin: 0;
        text-shadow: 0 0 25px #087bff;
        letter-spacing: 2px;
    }
    .sub-title {
        text-align: center;
        color: #a5d8ff;
        font-size: 1.05rem;
        margin-top: 4px;
        margin-bottom: 1.2rem;
        font-weight: 600;
    }
    .stTextArea textarea {
        background-color: #0b192d;
        color: #ffffff;
        border: 1px solid #3677b8;
        border-radius: 12px;
        font-size: 16px;
    }
</style>
""", unsafe_allow_html=True)

# Função para consultar a API oficial do Gemini (via Streamlit Secrets)
def perguntar_ao_gemini(pergunta):
    # Tenta buscar a chave de API configurada no Streamlit Cloud
    api_key = st.secrets.get("GEMINI_API_KEY", "")
    
    if not api_key:
        # Se não houver chave configurada, usa o modo inteligente de regras de golpe + fallback explicativo
        return analisar_modo_local(pergunta)

    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
    headers = {"Content-Type": "application/json"}
    payload = {
        "contents": [{
            "parts": [{"text": f"Você é a IA ALFA, uma inteligência artificial global avançada, útil e polivalente. Responda à seguinte pergunta de forma clara, prestativa e em português do Brasil: {pergunta}"}]
        }]
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=10)
        if response.status_code == 200:
            data = response.json()
            return data["candidates"][0]["content"]["parts"][0]["text"]
        else:
            return "Erro ao conectar com a API do Gemini. Verifique sua chave nas configurações do Streamlit Cloud."
    except Exception as e:
        return f"Ocorreu um erro de conexão: {str(e)}"

def analisar_modo_local(texto):
    texto_lower = texto.lower()
    sinais = []
    regras = [
        (["pix", "transferência", "transferencia", "depósito", "deposito"], "Menção a Pix, depósito ou transferência bancária."),
        (["senha", "token", "código de segurança", "codigo de seguranca"], "Solicitação de senha, token ou código de acesso."),
        (["prêmio", "premio", "ganhou", "sorteio", "resgate"], "Promessa de prêmio, dinheiro fácil ou sorteio."),
        (["urgente", "imediatamente", "última chance", "bloqueio hoje"], "Pressão psicológica para você agir rapidamente sem pensar."),
        (["conta bloqueada", "cartão bloqueado", "cancelamento"], "Ameaça de bloqueio ou cancelamento de conta/cartão."),
        (["clique aqui", "acesse o link", "link abaixo", "http", "https"], "Incentivo para clicar em links externos suspeitos.")
    ]
    for palavras, descricao in regras:
        if any(p in texto_lower for p in palavras):
            sinais.append(descricao)
            
    if sinais:
        resultado = "⚠️ ALERTA DE SEGURANÇA: Detectamos possíveis sinais de golpe! Padrões encontrados: " + ", ".join(sinais) + ". Recomendação: Não clique em links e não envie dinheiro."
        return resultado
    else:
        return f"Olá! Como assistente IA ALFA, analisei sua mensagem ('{texto}') e não encontrei sinais diretos de fraude. Se esta for uma pergunta geral, lembre-se de configurar a sua chave GEMINI_API_KEY nos segredos do Streamlit Cloud para respostas livres ilimitadas sobre qualquer assunto!"

# Topo limpo
st.markdown("""
<div class="header-container">
    <div class="globo-3d-gigante"></div>
    <h1 class="main-title">🌐 IA ALFA MUNDO DIGITAL</h1>
    <p class="sub-title">SISTEMA GLOBAL DE INTELIGÊNCIA E VOZ 🎙️ 🔊</p>
</div>
""", unsafe_allow_html=True)

st.markdown("### 💬 Pergunte ou Analise Qualquer Coisa")

pergunta = st.text_area(
    "Digite sua dúvida, pergunta geral ou cole uma mensagem suspeita:",
    placeholder="Exemplo: Explique como funciona a gravidade, ou verifique se esta mensagem é golpe...",
    height=130
)

if st.button("🌐 PERGUNTAR E OUVIR", type="primary", use_container_width=True):
    if pergunta.strip():
        with st.spinner("A IA ALFA está processando sua resposta..."):
            resposta_ia = perguntar_ao_gemini(pergunta)
        
        st.markdown("---")
        st.markdown("### 📊 Resposta da IA ALFA")
        st.write(resposta_ia)

        texto_limpo = resposta_ia.replace('"', '').replace("'", "").replace('\n', ' ')
        
        audio_componente = f"""
        <div style="margin-top: 15px; padding: 18px; background: linear-gradient(135deg, #0b192d, #102747); border-radius: 12px; border: 2px solid #00b9ff; box-shadow: 0 0 20px rgba(0, 185, 255, 0.3); display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 12px;">
            <div style="display: flex; align-items: center; gap: 10px;">
                <span style="font-size: 28px;">🎙️</span>
                <span style="font-size: 28px;">🔊</span>
                <div>
                    <div style="color: #6bd5ff; font-weight: bold; font-size: 16px;">Voz Sintetizada Ativa</div>
                    <div style="color: #a5d8ff; font-size: 13px;">Clique no botão para ouvir a resposta:</div>
                </div>
            </div>
            <button onclick="falar()" style="background: linear-gradient(90deg, #00b9ff, #087bff); color: #ffffff; border: none; padding: 12px 24px; border-radius: 8px; font-weight: bold; cursor: pointer; font-size: 16px; box-shadow: 0 0 12px rgba(0, 185, 255, 0.5);">
                🔊 OUVIR EM VOZ ALTA
            </button>
        </div>

        <script>
            function falar() {{
                if ('speechSynthesis' in window) {{
                    window.speechSynthesis.cancel();
                    var msg = new SpeechSynthesisUtterance("{texto_limpo}");
                    msg.lang = 'pt-BR';
                    msg.rate = 1.0;
                    window.speechSynthesis.speak(msg);
                }} else {{
                    alert('Seu navegador não suporta leitura de voz.');
                }}
            }}
        </script>
        """
        components.html(audio_componente, height=110)
    else:
        st.warning("Por favor, digite uma pergunta ou mensagem.")
