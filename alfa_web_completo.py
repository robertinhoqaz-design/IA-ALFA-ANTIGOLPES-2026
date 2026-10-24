import streamlit as st
import requests

st.set_page_config(page_title="IA ALFA Antigolpes", page_icon="🛡️", layout="wide")

st.markdown("<h1 style='text-align: center; color: #6bd5ff;'>🛡️ IA ALFA ANTIGOLPES</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>Assistente de Segurança Digital</p>", unsafe_allow_html=True)

st.markdown("---")
pergunta = st.text_area("Cole aqui a mensagem suspeita para analisar:", height=150)

if st.button("ANALISAR AGORA"):
    if pergunta.strip():
        st.success("Análise concluída com sucesso! Mensagem recebida.")
    else:
        st.warning("Por favor, digite ou cole uma mensagem para analisar.")
