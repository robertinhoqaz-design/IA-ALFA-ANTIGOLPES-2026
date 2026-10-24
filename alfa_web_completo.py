import streamlit as st
import streamlit.components.v1 as components
import requests
import json

st.set_page_config(
    page_title="IA ALFA Mundo Digital",
    page_icon="🌐",
    layout="wide"
)

# Estilo visual futurista e limpo
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
    .stChatInputContainer {
        background-color: #0b192d !important;
        border-radius: 12px !important;
    }
</style>
""", unsafe_allow_html=True)

# Inicializa o histórico de mensagens da conversa na sessão
if "mensagens" not in st.session_state:
    st.session_state.mensagens = [
        {"role": "assistant", "content": "Olá! Sou a **IA ALFA**, sua inteligência artificial global avançada. Como posso ajudar você hoje com consultas, análises ou perguntas gerais?"}
    ]

# Função para consultar o Gemini com suporte a histórico e raciocínio avançado
def consultar_gemini_avancado(historico):
    api_key = st.secrets.get("GEMINI_API_KEY", "")
    
    if not api_key:
        return "⚠️ **Aviso:** Configure sua chave `GEMINI_API_KEY` nos segredos do Streamlit Cloud para ativar consultas avançadas ilimitadas. No momento, estou operando no modo de regras locais."

    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
    headers = {"Content-Type": "application/json"}
    
    # Prepara o payload com todo o histórico da conversa para manter o contexto
    contents = []
    for m in historico:
        role = "user" if m["role"] == "user" else "model"
        contents.append({"role": role, "parts": [{"text": m["content"]}]})

    payload = {
        "contents": contents,
        "system_instruction": {
            "parts": [{"text": "Você é a IA ALFA, uma inteligência artificial global polivalente de alta performance. Responda sempre em português do Brasil de forma clara, técnica quando necessário, prestativa e amigável."}]
        }
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=15)
        if response.status_code == 200:
            data = response.json()
            return data["candidates"][0]["content"]["parts"][0]["text"]
        else:
            return f"Erro na API do Gemini (Código {response.status_code}): Verifique sua chave de acesso."
    except Exception as e:
        return f"Erro de conexão: {str(e)}"

# Topo limpo com o Globo 3D
st.markdown("""
<div class="header-container">
    <div class="globo-3d-gigante"></div>
    <h1 class="main-title">🌐 IA ALFA MUNDO DIGITAL</h1>
    <p class="sub-title">SISTEMA GLOBAL DE CONSULTAS E VOZ AVANÇADA 🎙️ 🔊</p>
</div>
""", unsafe_allow_html=True)

st.markdown("### 💬 Conversas e Consultas Avançadas em Tempo Real")

# Exibe o histórico de mensagens em formato de chat moderno
for msg in st.session_state.mensagens:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# Entrada de chat contínua (estilo ChatGPT/Gemini)
pergunta_usuario = st.chat_input("Digite sua consulta, pergunta ou cole uma mensagem suspeita...")

if pergunta_usuario:
    # Adiciona a pergunta do usuário ao histórico
    st.session_state.mensagens.append({"role": "user", "content": pergunta_usuario})
    with st.chat_message("user"):
        st.write(pergunta_usuario)

    # Processa a resposta com a IA avançada
    with st.chat_message("assistant"):
        with st.spinner("IA ALFA processando consulta avançada..."):
            resposta_ia = consultar_gemini_avancado(st.session_state.mensagens)
        st.write(resposta_ia)
        
        # Adiciona a resposta da IA ao histórico
        st.session_state.mensagens.append({"role": "assistant", "content": resposta_ia})

        # Limpa o texto para o sintetizador de voz reproduzir corretamente
        texto_limpo = resposta_ia.replace('"', '').replace("'", "").replace('\n', ' ')
        
        # Painel de Voz Integrado
        audio_componente = f"""
        <div style="margin-top: 15px; padding: 15px; background: linear-gradient(135deg, #0b192d, #102747); border-radius: 12px; border: 2px solid #00b9ff; box-shadow: 0 0 15px rgba(0, 185, 255, 0.3); display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 10px;">
            <div style="display: flex; align-items: center; gap: 8px;">
                <span style="font-size: 24px;">🎙️</span>
                <span style="font-size: 24px;">🔊</span>
                <div style="color: #6bd5ff; font-weight: bold; font-size: 15px;">Voz Ativa</div>
            </div>
            <button onclick="falar()" style="background: linear-gradient(90deg, #00b9ff, #087bff); color: #ffffff; border: none; padding: 10px 20px; border-radius: 8px; font-weight: bold; cursor: pointer; font-size: 15px; box-shadow: 0 0 10px rgba(0, 185, 255, 0.5);">
                🔊 OUVIR RESPOSTA
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
                }}
            }}
        </script>
        """
        components.html(audio_componente, height=90)
