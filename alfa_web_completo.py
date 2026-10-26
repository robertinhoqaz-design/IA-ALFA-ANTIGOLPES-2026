import io
from gtts import gTTS
import streamlit as st
from google import genai

st.set_page_config(
    page_title="Projeto Alfa - Identificador de Golpes",
    page_icon="🛡️",
    layout="wide",
)

st.title("🛡️ Projeto Alfa: Identificador de Golpes")
st.write(
    "Cole abaixo a mensagem, texto ou relato suspeito para verificar se é"
    " golpe."
)

texto_usuario = st.text_area(
    "Digite ou cole o texto suspeito aqui:",
    placeholder=(
        "Exemplo: Seu banco bloqueou sua conta. Clique neste link e informe"
        " sua senha..."
    ),
    height=160,
)

if st.button("🛡️ ANALISAR AGORA"):
  if not texto_usuario.strip():
    st.warning("Por favor, insira um texto para analisar.")
  else:
    with st.spinner("Analisando com Inteligência Artificial..."):
      try:
        client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])

        prompt_sistema = (
            "Você é o Alfa, um assistente especialista em segurança digital e"
            " em identificar golpes financeiros, fraudes em redes sociais e"
            " ligações maliciosas. Analise o texto fornecido pelo usuário, a"
            "ponte os riscos de golpe de forma clara e direta, e oriente o"
            " usuário sobre o que fazer."
        )

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=f"{prompt_sistema}\n\nTexto suspeito: {texto_usuario}",
        )

        resposta = response.text

        st.success("Análise concluída!")
        st.markdown(resposta)

        st.subheader("🔊 Ouvir Resposta")
        tts = gTTS(text=resposta, lang="pt")
        sound_file = io.BytesIO()
        tts.write_to_fp(sound_file)
        sound_file.seek(0)
        st.audio(sound_file, format="audio/mp3")

      except Exception as e:
        st.error(f"Ocorreu um erro ao processar a solicitação: {e}")
