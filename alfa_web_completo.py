import io
import streamlit as st
from google import genai
from gtts import gTTS

st.set_page_config(
    page_title="IA ALFA - Identificador de Golpes",
    page_icon="🔎",
    layout="wide",
)

st.title("IA ALFA - Identificador de Golpes")
st.subheader("Proteção contra fraudes, phishing e golpes financeiros")
st.write(
    "Cole uma mensagem suspeita para receber uma análise "
    "e orientações de segurança."
)

texto_usuario = st.text_area(
    "Mensagem, e-mail ou texto suspeito",
    placeholder="Cole aqui a mensagem que você recebeu...",
    height=180,
)

if st.button("ANALISAR AGORA", type="primary"):
    if not texto_usuario.strip():
        st.warning("Digite ou cole uma mensagem antes de analisar.")
    else:
        try:
            api_key = st.secrets["GEMINI_API_KEY"]
            client = genai.Client(api_key=api_key)

            prompt = f"""
Você é a IA ALFA, assistente de prevenção contra golpes digitais.
Analise a mensagem abaixo em português brasileiro.

Apresente:
1. Nível de atenção: baixo, moderado ou alto.
2. Sinais suspeitos encontrados.
3. Possíveis riscos.
4. O que a pessoa deve fazer com segurança.

Não afirme que uma mensagem é fraude sem evidências.
Não abra links nem solicite senhas, códigos ou dados bancários.
Explique que a análise é orientativa e não confirma uma fraude.

Mensagem para analisar:
{texto_usuario}
"""

            with st.spinner("A IA ALFA está analisando..."):
                resposta = client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=prompt,
                )

            texto_resposta = resposta.text

            if texto_resposta:
                st.success("Análise concluída!")
                st.markdown(texto_resposta)

                st.subheader("Ouvir resposta")
                try:
                    audio = io.BytesIO()
                    gTTS(text=texto_resposta, lang="pt-br").write_to_fp(audio)
                    audio.seek(0)
                    st.audio(audio, format="audio/mp3")
                except Exception:
                    st.info(
                        "Não foi possível gerar o áudio agora. "
                        "A análise escrita continua disponível."
                    )
            else:
                st.warning(
                    "A IA não retornou uma resposta. Tente novamente."
                )

        except KeyError:
            st.error(
                "A chave GEMINI_API_KEY não foi encontrada nos Secrets "
                "do Streamlit. Configure-a no painel do aplicativo."
            )
        except Exception as erro:
            st.error("Não foi possível concluir a análise.")
            st.caption(f"Detalhes técnicos: {erro}")

st.divider()
st.caption(
    "IA ALFA Antigolpes — ferramenta de orientação. "
    "Confirme informações pelos canais oficiais antes de agir."
)
