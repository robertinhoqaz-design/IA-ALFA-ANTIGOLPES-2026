import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="IA ALFA Mundo Digital",
    page_icon="🌐",
    layout="wide"
)

# Estilo para colar no topo e zerar qualquer espaco em branco
st.markdown("""
<style>
    /* Remove barra superior e espacos extras do Streamlit */
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

def analisar_golpe(texto):
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
    return sinais

# Topo colado perfeitamente no topo
st.markdown("""
<div class="header-container">
    <div class="globo-3d-gigante"></div>
    <h1 class="main-title">🌐 IA ALFA MUNDO DIGITAL</h1>
    <p class="sub-title">SISTEMA GLOBAL DE ANÁLISE E VOZ INTELIGENTE 🎙️ 🔊</p>
</div>
""", unsafe_allow_html=True)

st.markdown("### 🔎 Analisar Mensagem Suspeita")

pergunta = st.text_area(
    "Cole aqui a mensagem, SMS, e-mail ou conversa suspeita:",
    placeholder="Exemplo: Seu banco bloqueou sua conta. Clique no link para recadastrar sua senha...",
    height=130
)

if st.button("🌐 ANALISAR AGORA", type="primary", use_container_width=True):
    if pergunta.strip():
        sinais = analisar_golpe(pergunta)
        
        st.markdown("---")
        st.markdown("### 📊 Resultado da Análise Global")
        
        texto_falar = ""
        if sinais:
            st.error("⚠️ **ALERTA: SINAIS TÍPICOS DE GOLPE DETECTADOS!**")
            st.write("Identificamos os seguintes padrões suspeitos nesta mensagem:")
            texto_falar = "Atenção! Alerta de golpe detectado. Identificamos os seguintes padrões suspeitos na mensagem: "
            for s in sinais:
                st.markdown(f"- 🔴 **{s}**")
                texto_falar += f"{s}. "
            st.warning("👉 **Recomendação:** Não clique em links, não envie dinheiro por Pix e não forneça dados pessoais ou senhas.")
            texto_falar += "Recomendação: Não clique em links, não envie dinheiro por Pix e não forneça dados pessoais."
        else:
            st.success("✅ **NENHUM SINAL DIRETO DE GOLPE IDENTIFICADO PELAS REGRAS.**")
            st.info("💡 **Dica de segurança:** Mesmo que nada crítico tenha sido detectado, lembre-se de nunca compartilhar dados confidenciais.")
            texto_falar = "Nenhum sinal direto de golpe foi identificado. Lembre-se de nunca compartilhar dados confidenciais."

        texto_limpo = texto_falar.replace('"', '').replace("'", "").replace('\n', ' ')
        
        # Componente HTML com botão interativo direto para disparar a fala sem bloqueio
        audio_componente = f"""
        <div style="margin-top: 15px; padding: 18px; background: linear-gradient(135deg, #0b192d, #102747); border-radius: 12px; border: 2px solid #00b9ff; box-shadow: 0 0 20px rgba(0, 185, 255, 0.3); display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 12px;">
            <div style="display: flex; align-items: center; gap: 10px;">
                <span style="font-size: 28px;">🎙️</span>
                <span style="font-size: 28px;">🔊</span>
                <div>
                    <div style="color: #6bd5ff; font-weight: bold; font-size: 16px;">Voz Sintetizada Ativa</div>
                    <div style="color: #a5d8ff; font-size: 13px;">Clique no botão para ouvir o relatório:</div>
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
        st.warning("Por favor, cole uma mensagem para que o sistema possa analisar.")
