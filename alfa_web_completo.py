import streamlit as st

st.set_page_config(
    page_title="IA ALFA Antigolpes",
    page_icon="🛡️",
    layout="wide"
)

# Estilo Futurista de Alta Definição
st.markdown('''
<style>
    .stApp {
        background: radial-gradient(circle at top, #102747 0%, #07101e 70%);
        color: #ffffff;
    }
    
    /* Globo 3D Holográfico Centralizado */
    .header-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        margin-top: 1rem;
        margin-bottom: 1rem;
    }
    .globo-original {
        width: 100px;
        height: 100px;
        background: radial-gradient(circle, rgba(76,201,240,0.2) 0%, rgba(0,0,0,0) 70%);
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        box-shadow: 0 0 25px #087bff;
        margin-bottom: 15px;
    }
    .globo-svg {
        width: 65px;
        height: 65px;
        filter: drop-shadow(0px 0px 10px #4cc9f0);
    }
    
    .main-title {
        text-align: center;
        color: #4cc9f0;
        font-size: 2.5rem;
        font-weight: 900;
        margin: 0;
        text-shadow: 0 0 18px #087bff;
        letter-spacing: 1.5px;
    }
    .sub-title {
        text-align: center;
        color: #a5d8ff;
        font-size: 1.1rem;
        margin-top: 5px;
        margin-bottom: 2rem;
        font-weight: 500;
    }

    /* Estilo da caixa de texto e botões */
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
        font-size: 17px;
        padding: 12px;
    }
</style>
''', unsafe_allow_html=True)

def analisar_golpe(texto):
    texto = texto.lower()
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
        if any(p in texto for p in palavras):
            sinais.append(descricao)
    return sinais

# Topo Original Centralizado com Globo Neon Holográfico
st.markdown('''
<div class="header-container">
    <div class="globo-original">
        <svg class="globo-svg" viewBox="0 0 24 24" fill="none" stroke="#4cc9f0" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round">
            <circle cx="12" cy="12" r="10"></circle>
            <line x1="2" y1="12" x2="22" y2="12"></line>
            <path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"></path>
        </svg>
    </div>
    <h1 class="main-title">🛡️ IA ALFA ANTIGOLPES</h1>
    <p class="sub-title">🌐 SISTEMA GLOBAL DE SEGURANÇA DIGITAL E VOZ INTELIGENTE 🎙️</p>
</div>
''', unsafe_allow_html=True)

st.markdown("### 🔎 Analisar Mensagem Suspeita")

with st.form("formulario_analise"):
    pergunta = st.text_area(
        "Cole aqui a mensagem, SMS, e-mail ou conversa suspeita:",
        placeholder="Exemplo: Seu banco bloqueou sua conta. Clique no link para recadastrar sua senha...",
        height=150
    )
    enviar = st.form_submit_button("🛡️ ANALISAR E OUVIR RESULTADO 🎙️")

if enviar:
    if pergunta.strip():
        sinais = analisar_golpe(pergunta)
        
        st.markdown("---")
        st.markdown("### 📊 Resultado da Análise de Segurança")
        
        texto_resultado = ""
        if sinais:
            st.error("⚠️ **ALERTA: SINAIS TÍPICOS DE GOLPE DETECTADOS!**")
            st.write("Identificamos os seguintes padrões suspeitos nesta mensagem:")
            texto_resultado = "Atenção! Alerta de golpe detectado. Identificamos os seguintes padrões suspeitos na mensagem: "
            for s in sinais:
                st.markdown(f"- 🔴 **{s}**")
                texto_resultado += f"{s}. "
            st.warning("👉 **Recomendação:** Não clique em links, não envie dinheiro por Pix e não forneça dados pessoais ou senhas.")
            texto_resultado += "Recomendação: Não clique em links, não envie dinheiro por Pix e não forneça dados pessoais."
        else:
            st.success("✅ **NENHUM SINAL DIRETO DE GOLPE IDENTIFICADO PELAS REGRAS PADRÃO.**")
            st.info("💡 **Dica de segurança:** Mesmo que nada crítico tenha sido detectado, lembre-se de nunca compartilhar dados confidenciais se não tiver certeza da identidade do remetente.")
            texto_resultado = "Nenhum sinal direto de golpe foi identificado. Lembre-se de nunca compartilhar dados confidenciais."

        texto_seguro = texto_resultado.replace('"', '\\"').replace("\n", " ")
        
        # Painel de Áudio com Microfone Integrado
        audio_html = f"""
        <div style="margin-top: 20px; padding: 16px; background: linear-gradient(135deg, #0b192d, #102747); border-radius: 12px; border: 1px solid #00b9ff; box-shadow: 0 0 15px rgba(0, 185, 255, 0.2);">
            <div style="display: flex; align-items: center; gap: 12px; margin-bottom: 10px;">
                <span style="font-size: 24px;">🎙️</span>
                <span style="color: #4cc9f0; font-weight: bold; font-size: 16px;">Sintetizador de Voz IA ALFA</span>
            </div>
            <button onclick="falarTexto()" style="background: linear-gradient(90deg, #00b9ff, #087bff); color: #ffffff; border: none; padding: 10px 20px; border-radius: 8px; font-weight: bold; cursor: pointer; font-size: 15px; display: flex; align-items: center; gap: 8px;">
                🔊 Ouvir Relatório Novamente
            </button>
        </div>
        <script>
            function falarTexto() {{
                if ('speechSynthesis' in window) {{
                    window.speechSynthesis.cancel();
                    var msg = new SpeechSynthesisUtterance("{texto_seguro}");
                    msg.lang = 'pt-BR';
                    msg.rate = 1.0;
                    window.speechSynthesis.speak(msg);
                }}
            }}
            setTimeout(falarTexto, 600);
        </script>
        """
        st.markdown(audio_html, unsafe_allow_html=True)
    else:
        st.warning("Por favor, cole uma mensagem para que a IA ALFA possa analisar.")
