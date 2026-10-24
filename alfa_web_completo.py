import streamlit as st

st.set_page_config(
    page_title="IA ALFA Mundo Digital",
    page_icon="🌐",
    layout="wide"
)

st.markdown("""
<style>
    .stApp {
        background: radial-gradient(circle at top, #0f2347 0%, #030712 80%);
        color: #ffffff;
    }
    .header-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        margin-top: 1.5rem;
        margin-bottom: 1.5rem;
    }
    .globo-3d-gigante {
        width: 150px;
        height: 150px;
        border-radius: 50%;
        background: radial-gradient(circle at 35% 35%, #6bd5ff, #087bff 55%, #020713 100%);
        box-shadow: 0 0 50px #00b9ff, inset -15px -15px 30px rgba(0,0,0,0.8);
        margin-bottom: 20px;
        animation: floatAndGlow 4s ease-in-out infinite alternate;
    }
    @keyframes floatAndGlow {
        0% { transform: translateY(0px) scale(1); box-shadow: 0 0 35px #087bff; }
        100% { transform: translateY(-12px) scale(1.03); box-shadow: 0 0 65px #00b9ff; }
    }
    .main-title {
        text-align: center;
        color: #6bd5ff;
        font-size: 2.8rem;
        font-weight: 900;
        margin: 0;
        text-shadow: 0 0 25px #087bff;
        letter-spacing: 2px;
    }
    .sub-title {
        text-align: center;
        color: #a5d8ff;
        font-size: 1.2rem;
        margin-top: 8px;
        margin-bottom: 2rem;
        font-weight: 600;
    }
    .stTextArea textarea {
        background-color: #0b192d;
        color: #ffffff;
        border: 1px solid #3677b8;
        border-radius: 12px;
        font-size: 16px;
    }
    .stButton button, .stFormSubmitButton button {
        background: linear-gradient(90deg, #087bff, #00b9ff);
        color: white;
        border: none;
        border-radius: 10px;
        font-weight: bold;
        font-size: 18px;
        padding: 14px;
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

st.markdown("""
<div class="header-container">
    <div class="globo-3d-gigante"></div>
    <h1 class="main-title">🌐 IA ALFA MUNDO DIGITAL</h1>
    <p class="sub-title">SISTEMA GLOBAL DE ANÁLISE E VOZ AUTOMÁTICA 🎙️ 🔊</p>
</div>
""", unsafe_allow_html=True)

st.markdown("### 🔎 Analisar Mensagem Suspeita")

pergunta = st.text_area(
    "Cole aqui a mensagem, SMS, e-mail ou conversa suspeita:",
    placeholder="Exemplo: Seu banco bloqueou sua conta. Clique no link para recadastrar sua senha...",
    height=150
)

if st.button("🌐 ANALISAR E OUVIR AGORA 🎙️ 🔊"):
    if pergunta.strip():
        sinais = analisar_golpe(pergunta)
        
        st.markdown("---")
        st.markdown("### 📊 Resultado da Análise Global")
        
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
        
        audio_html = f"""
        <div style="margin-top: 20px; padding: 20px; background: linear-gradient(135deg, #0b192d, #102747); border-radius: 14px; border: 2px solid #00b9ff; box-shadow: 0 0 25px rgba(0, 185, 255, 0.3); display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 15px;">
            <div style="display: flex; align-items: center; gap: 12px;">
                <span style="font-size: 32px; filter: drop-shadow(0 0 10px #00b9ff);">🎙️</span>
                <span style="font-size: 32px; filter: drop-shadow(0 0 10px #00b9ff);">🔊</span>
                <div>
                    <div style="color: #6bd5ff; font-weight: bold; font-size: 18px;">Voz e Áudio da IA ALFA</div>
                    <div style="color: #a5d8ff; font-size: 14px;">Aperte o botão ao lado para ouvir o relatório em voz alta!</div>
                </div>
            </div>
            <button onclick="falarVozIA()" style="background: linear-gradient(90deg, #00b9ff, #087bff); color: #ffffff; border: none; padding: 12px 24px; border-radius: 8px; font-weight: bold; cursor: pointer; font-size: 16px; box-shadow: 0 0 15px rgba(0, 185, 255, 0.5);">
                🔊 OUVIR RELATÓRIO 🎙️
            </button>
        </div>

        <script>
            function falarVozIA() {{
                if ('speechSynthesis' in window) {{
                    window.speechSynthesis.cancel();
                    var fala = new SpeechSynthesisUtterance("{texto_limpo}");
                    fala.lang = 'pt-BR';
                    fala.rate = 1.0;
                    fala.pitch = 1.0;
                    fala.volume = 1.0;
                    window.speechSynthesis.speak(fala);
                }}
            }}
            setTimeout(falarVozIA, 300);
        </script>
        """
        st.markdown(audio_html, unsafe_allow_html=True)
    else:
        st.warning("Por favor, cole uma mensagem para que o sistema possa analisar.")
