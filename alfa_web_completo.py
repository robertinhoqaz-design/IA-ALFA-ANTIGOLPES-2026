import streamlit as st

st.set_page_config(
    page_title="IA ALFA Antigolpes",
    page_icon="🛡️",
    layout="wide"
)

st.markdown('''
<style>
    .stApp {
        background-color: #0b132b;
        color: #ffffff;
    }
    .main-title {
        text-align: center;
        color: #4cc9f0;
        font-size: 2.3rem;
        font-weight: 800;
        margin-bottom: 0.1rem;
    }
    .sub-title {
        text-align: center;
        color: #4895ef;
        font-size: 1rem;
        margin-bottom: 1.5rem;
    }
    .stTextArea textarea {
        background-color: #1c2541;
        color: #ffffff;
        border: 1px solid #3a506b;
        border-radius: 8px;
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

st.markdown('<h1 class="main-title">🌐 🛡️ 🎤 IA ALFA ANTIGOLPES</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">ASSISTENTE DE SEGURANÇA DIGITAL GLOBAL</p>', unsafe_allow_html=True)

st.markdown("### 🔎 Analisar Mensagem Suspeita")

with st.form("formulario_analise"):
    pergunta = st.text_area(
        "Cole aqui a mensagem, SMS, e-mail ou conversa suspeita:",
        placeholder="Exemplo: Seu banco bloqueou sua conta. Clique no link para recadastrar sua senha...",
        height=150
    )
    enviar = st.form_submit_button("🛡️ ANALISAR E LER AGORA")

if enviar:
    if pergunta.strip():
        sinais = analisar_golpe(pergunta)
        
        st.markdown("---")
        st.markdown("### 📊 Resultado da Análise de Segurança")
        
        texto_resultado = ""
        if sinais:
            st.error("⚠️ **ALERTA: SINAIS TÍPICOS DE GOLPE DETECTADOS!**")
            st.write("Identificamos os seguintes padrões suspeitos nesta mensagem:")
            texto_resultado = "Atenção! Alerta de golpe detectado. Identificamos os seguintes padrões suspeitos nesta mensagem: "
            for s in sinais:
                st.markdown(f"- 🔴 **{s}**")
                texto_resultado += f"{s}. "
            st.warning("👉 **Recomendação:** Não clique em links, não envie dinheiro por Pix e não forneça dados pessoais ou senhas.")
            texto_resultado += "Recomendação: Não clique em links, não envie dinheiro por Pix e não forneça dados pessoais ou senhas."
        else:
            st.success("✅ **NENHUM SINAL DIRETO DE GOLPE IDENTIFICADO PELAS REGRAS PADRÃO.**")
            st.info("💡 **Dica de segurança:** Mesmo que nada crítico tenha sido detectado, lembre-se de nunca compartilhar dados confidenciais se não tiver certeza da identidade de quem enviou a mensagem.")
            texto_resultado = "Nenhum sinal direto de golpe foi identificado pelas regras padrão. Dica de segurança: Lembre-se de nunca compartilhar dados confidenciais."

        texto_seguro = texto_resultado.replace('"', '\\"').replace("\n", " ")
        
        audio_html = f"""
        <div style="margin-top: 15px; padding: 10px; background-color: #1c2541; border-radius: 8px; border: 1px solid #4cc9f0;">
            <p style="margin: 0 0 8px 0; color: #4cc9f0; font-weight: bold;">🎤 Leitura por Voz da IA ALFA:</p>
            <button onclick="falarTexto()" style="background-color: #4cc9f0; color: #0b132b; border: none; padding: 8px 16px; border-radius: 6px; font-weight: bold; cursor: pointer;">
                🔊 Ouvir Alerta Novamente
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
        st.warning("Por favor, cole uma mensagem para que a IA ALFA possa analisar.")
