import io
from gtts import gTTS
import streamlit as st
from google import genai

st.set_page_config(
    page_title="Projeto Alfa - Identificador de Golpes",
    page_icon="­ƒøí´©Å",
    layout="wide",
)

st.title("­ƒøí´©Å Projeto Alfa: Identificador de Golpes")
st.write(
    "Cole abaixo a mensagem, texto ou relato suspeito para verificar se ├®"
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

if st.button("­ƒøí´©Å ANALISAR AGORA"):
  if not texto_usuario.strip():
    st.warning("Por favor, insira um texto para analisar.")
  else:
    with st.spinner("Analisando com Intelig├¬ncia Artificial..."):
      try:
        client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])

        prompt_sistema = (
            "Voc├¬ ├® o Alfa, um assistente especialista em seguran├ºa digital e"
            " em identificar golpes financeiros, fraudes em redes sociais e"
            " liga├º├Áes maliciosas. Analise o texto fornecido pelo usu├írio, a"
            "ponte os riscos de golpe de forma clara e direta, e oriente o"
            " usu├írio sobre o que fazer."
        )

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=f"{prompt_sistema}\n\nTexto suspeito: {texto_usuario}",
        )

        resposta = response.text

        st.success("An├ílise conclu├¡da!")
        st.markdown(resposta)

        st.subheader("­ƒöè Ouvir Resposta")
        tts = gTTS(text=resposta, lang="pt")
        sound_file = io.BytesIO()
        tts.write_to_fp(sound_file)
        sound_file.seek(0)
        st.audio(sound_file, format="audio/mp3")

      except Exception as e:
        st.error(f"Ocorreu um erro ao processar a solicita├º├úo: {e}")
