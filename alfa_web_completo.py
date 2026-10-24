import streamlit as st

st.set_page_config(
    page_title="IA ALFA Mundo Digital",
    page_icon="🌐",
    layout="wide"
)

# Estilo Futurista com Globo 3D Esférico e Painel de Áudio + Microfone Integrados
st.markdown('''
<style>
    .stApp {
        background: radial-gradient(circle at top, #0d1b3a 0%, #030712 75%);
        color: #ffffff;
    }
    
    /* Globo Esférico 3D Limpo no Centro */
    .header-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        margin-top: 1rem;
        margin-bottom: 1rem;
    }
    .globo-3d-clean {
        width: 100px;
        height: 100px;
        border-radius: 50%;
        background: radial-gradient(circle at 30% 30%, #4cc9f0, #087bff 60%, #030712 100%);
        box-shadow: 0 0 35px #00b9ff, inset -10px -10px 20px rgba(0,0,0,0.6);
        margin-bottom: 15px;
        animation: floatGlobo 3s ease-in-out infinite alternate;
    }
    @keyframes floatGlobo {
        0% { transform: translateY(0px); box-shadow: 0 0 25px #087bff; }
        100% { transform: translateY(-8px); box-shadow: 0 0 45px #00b9ff; }
    }
    
    .main-title {
        text-align: center;
        color: #4cc9f0;
        font-size: 2.5rem;
        font-weight: 900;
        margin: 0;
        text-shadow: 0 0 20px #087bff;
        letter-spacing: 1.5px;
    }
    .sub-title {
        text-align: center;
        color: #a5d8ff;
        font-size: 1.1rem;
        margin-top: 8px;
        margin-bottom: 2rem;
        font-weight: 500;
    }

    /* Caixa de Entrada e Botão */
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

# Cabeçalho com Globo 3D Esférico Limpo
st.markdown('''
<div class="header-container">
    <div class="globo-3d-clean"></div>
    <h1 class="main-title">🌐 IA ALFA MUNDO DIGITAL</h1>
    <p class="sub-title">SISTEMA GLOBAL DE ANÁLISE E VOZ AUTOMÁTICA 🎙️ 🔊</p>
</div>
''', unsafe_allow_html=True)

st.markdown("### 🔎 Analisar Mensagem Suspeita")

with st.form("formulario_analise"):
    pergunta = st.text_area(
        "Cole aqui a mensagem, SMS, e-mail ou conversa suspeita:",
        placeholder="Exemplo: Seu banco bloqueou sua conta. Clique no link para recadastrar sua senha...",
        height=150
    )
    enviar = st.form_submit_button("🌐 ANALISAR E OUVIR AGORA 🎙️ 🔊")

if enviar:
    if pergunta.strip():
        sinais = analisar_golpe(pergunta)
        
        st.markdown("---")
        st.markdown("### 📊 Resultado da Análise Global")
        
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
            st.success("✅ **NENHUM SINAL DIRETO DE GOLPE IDENTIFICADO PELAS REGRAS.**")
            st.info("💡 **Dica de segurança:** Mesmo que nada crítico tenha sido detectado, lembre-se de nunca compartilhar dados confidenciais.")
            texto_resultado = "Nenhum sinal direto de golpe foi identificado. Lembre-se de nunca compartilhar dados confidenciais."

        texto_seguro = texto_resultado.replace('"', '\\"').replace("\n", " ")
        
        # Painel Unificado de Microfone 🎙️ + Áudio 🔊 com Design Elegante
        audio_html = f"""
        <div style="margin-top: 20px; padding: 18px; background: linear-gradient(135deg, #0b192d, #102747); border-radius: 14px; border: 1px solid #4cc9f0; box-shadow: 0 0 20px rgba(76, 201, 240, 0.25); display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 12px;">
            <div style="display: flex; align-items: center; gap: 10px;">
                <span style="font-size: 28px; filter: drop-shadow(0 0 8px #00b9ff);">🎙️</span>
                <span style="font-size: 28px; filter: drop-shadow(0 0 8px #00b9ff);">🔊</span>
                <div>
                    <div style="color: #4cc9f0; font-weight: bold; font-size: 17px;">Sintetizador de Áudio e Voz</div>
                    <div style="color: #a5d8ff; font-size: 13px;">Leitura automática ativada</div>
                </div>
            </div>
            <button onclick="falarTexto()" style="background: linear-gradient(90deg, #00b9ff, #087bff); color: #ffffff; border: none; padding: 10px 22px; border-radius: 8px; font-weight: bold; cursor: pointer; font-size: 15px; box-shadow: 0 0 10px rgba(0, 185, 255, 0.4);">
                🔊 Reproduzir Novamente
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
            setTimeout(falarTexto, 500);
        </script>
        """
        st.markdown(audio_html, unsafe_allow_html=True)
    else:
        st.warning("Por favor, cole uma mensagem para que o sistema possa analisar.")
