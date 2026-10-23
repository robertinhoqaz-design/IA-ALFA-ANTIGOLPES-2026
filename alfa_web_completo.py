
import streamlit as st
import streamlit.components.v1 as components
import requests
import re
import html
import ipaddress
try:
    import pyttsx3
except ImportError:
    pyttsx3 = None

try:
    from ddgs import DDGS
except ImportError:
    DDGS = None


# =====================================
# CONFIGURAÇÃO
# =====================================

st.set_page_config(
    page_title="IA ALFA Antigolpes",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

OLLAMA_URL = "http://localhost:11434/api/chat"
MODELO_IA = "qwen2.5:0.5b"


# =====================================
# VISUAL NOVO
# =====================================

st.markdown("""
<style>
.stApp {
    background: linear-gradient(145deg, #07101e, #102747, #07101e);
    color: #f0f6ff;
}

header[data-testid="stHeader"] {
    background: transparent;
}

section.main > div.block-container {
    width: 96%;
    max-width: 1250px;
    padding: 1.5rem 1rem 3rem 1rem;
    margin: auto;
}

h1, h2, h3, p, label {
    color: #edf5ff;
}

.alfa-titulo {
    text-align: center;
    font-size: clamp(30px, 5vw, 48px);
    font-weight: 900;
    color: #6bd5ff;
    text-shadow: 0 0 16px #087bff;
    margin: 0;
}

.alfa-descricao {
    text-align: center;
    color: #b8d8ff;
    font-size: 16px;
    margin: 8px 0 20px 0;
}

.alfa-status {
    text-align: center;
    color: #78ffbc;
    font-size: 13px;
    margin-bottom: 15px;
}

.painel {
    background: rgba(11, 29, 53, 0.92);
    border: 1px solid #28578b;
    border-radius: 15px;
    padding: 18px;
    margin: 12px 0;
}

.stTextArea textarea {
    background: #0b192d;
    color: white;
    border: 1px solid #3677b8;
    border-radius: 12px;
    font-size: 16px;
}

.stButton button,
.stFormSubmitButton button {
    width: 100%;
    min-height: 45px;
    background: linear-gradient(90deg, #087bff, #00b9ff);
    color: white;
    border: none;
    border-radius: 10px;
    font-weight: bold;
}

.stButton button:hover,
.stFormSubmitButton button:hover {
    border: 1px solid #9ce7ff;
    color: white;
}

div[data-testid="stChatMessage"] {
    background: rgba(14, 34, 61, 0.9);
    border: 1px solid #244b76;
    border-radius: 12px;
}

div[data-testid="stSidebar"] {
    background: #081426;
}

hr {
    border-color: #294a70;
}

@media (max-width: 600px) {
    section.main > div.block-container {
        width: 100%;
        padding: 1rem 0.65rem 2rem 0.65rem;
    }
}
</style>
""", unsafe_allow_html=True)


# =====================================
# GLOBO ANIMADO — MANTIDO
# =====================================

globo_html = """
<!DOCTYPE html>
<html>
<head>
<style>
html, body {
    margin: 0;
    padding: 0;
    background: transparent;
    overflow: hidden;
}
.palco {
    height: 330px;
    display: flex;
    align-items: center;
    justify-content: center;
}
.globo {
    width: 245px;
    height: 245px;
    max-width: 70vw;
    max-height: 70vw;
    border-radius: 50%;
    position: relative;
    overflow: hidden;
    background:
      radial-gradient(circle at 30% 25%,
      #a5edff, #1689ff 23%, #0750b5 52%,
      #06183e 78%, #020916);
    box-shadow:
      0 0 25px #168bff,
      0 0 60px rgba(0, 125, 255, 0.5),
      inset -18px -15px 35px #020816,
      inset 10px 8px 22px rgba(130, 225, 255, 0.5);
    animation: flutuar 4s ease-in-out infinite;
}
.grade {
    position: absolute;
    inset: -20%;
    border: 1px solid rgba(120, 224, 255, 0.5);
    border-radius: 50%;
    animation: girar 12s linear infinite;
}
.g2 {
    transform: rotateY(55deg);
    animation: girar2 9s linear infinite;
}
.g3 {
    transform: rotateY(115deg);
    animation: girar 15s linear infinite reverse;
}
.linha {
    position: absolute;
    width: 140%;
    height: 1px;
    left: -20%;
    background: rgba(117, 221, 255, 0.4);
}
.l1 { top: 28%; }
.l2 { top: 50%; }
.l3 { top: 72%; }
.ponto {
    position: absolute;
    width: 6px;
    height: 6px;
    background: #d5f8ff;
    border-radius: 50%;
    box-shadow: 0 0 12px #58d9ff;
}
.p1 { top: 24%; left: 35%; }
.p2 { top: 43%; left: 72%; }
.p3 { top: 65%; left: 30%; }
.p4 { top: 73%; left: 61%; }
.p5 { top: 35%; left: 48%; }
@keyframes girar {
    from { transform: rotate(0deg); }
    to { transform: rotate(360deg); }
}
@keyframes girar2 {
    from { transform: rotateY(55deg) rotate(0deg); }
    to { transform: rotateY(55deg) rotate(360deg); }
}
@keyframes flutuar {
    0%, 100% { translate: 0 0; }
    50% { translate: 0 -8px; }
}
</style>
</head>
<body>
<div class="palco">
  <div class="globo">
    <div class="grade"></div>
    <div class="grade g2"></div>
    <div class="grade g3"></div>
    <div class="linha l1"></div>
    <div class="linha l2"></div>
    <div class="linha l3"></div>
    <div class="ponto p1"></div>
    <div class="ponto p2"></div>
    <div class="ponto p3"></div>
    <div class="ponto p4"></div>
    <div class="ponto p5"></div>
  </div>
</div>
</body>
</html>
"""


# =====================================
# REGRAS ANTIGOLPES
# =====================================

def analisar_golpe(texto):
    texto = texto.lower()
    sinais = []

    regras = [
        (
            ["pix", "transferência", "transferencia", "depósito",
             "deposito"],
            "Menção a Pix, depósito ou transferência."
        ),
        (
            ["senha", "token", "código de segurança",
             "codigo de seguranca", "código de acesso"],
            "Menção a senha ou código de segurança."
        ),
        (
            ["prêmio", "premio", "ganhou", "sorteio",
             "dinheiro grátis", "dinheiro gratis"],
            "Possível promessa de prêmio ou dinheiro."
        ),
        (
            ["urgente", "imediatamente", "última chance",
             "ultima chance", "agora mesmo"],
            "Pressão para agir rapidamente."
        ),
        (
            ["conta bloqueada", "cartão bloqueado",
             "cartao bloqueado", "conta suspensa"],
            "Possível ameaça de bloqueio de conta ou cartão."
        ),
        (
            ["clique aqui", "acesse o link", "confirme seus dados"],
            "Pedido para clicar em link ou confirmar dados."
        ),
        (
            ["taxa para liberar", "pague a taxa",
             "taxa antecipada", "taxa de liberação"],
            "Possível cobrança antecipada."
        ),
        (
            ["cpf", "dados bancários", "dados bancarios",
             "número do cartão", "numero do cartao"],
            "Menção a dados pessoais ou bancários."
        ),
        (
            ["anydesk", "teamviewer", "acesso remoto"],
            "Pedido de acesso remoto ao computador ou celular."
        )
    ]

    for palavras, descricao in regras:
        if any(p in texto for p in palavras):
            sinais.append(descricao)

    if re.search(r"https?://|www\.", texto):
        sinais.append(
            "Existe um endereço de internet. Verifique o domínio antes de abrir."
        )

    if not sinais:
        sinais.append(
            "Nenhum sinal conhecido foi identificado pelas regras básicas. "
            "Isso não garante que a mensagem seja segura."
        )

    return sinais

# =====================================
# PROTEÇÃO DE CRIANÇAS E ADOLESCENTES
# =====================================

def analisar_sinais_protecao(texto):
    texto = texto.lower()
    sinais = []

    regras_protecao = [
        (
            [
                "não conte para seus pais",
                "nao conte para seus pais",
                "mantenha em segredo",
                "isso fica entre nós",
                "isso fica entre nos"
            ],
            "Possível tentativa de impor segredo a uma criança."
        ),
        (
            [
                "mande uma foto íntima",
                "mande uma foto intima",
                "envie fotos sem roupa",
                "foto sem roupa",
                "mostre seu corpo"
            ],
            "Possível solicitação de imagem íntima."
        ),
        (
            [
                "encontro escondido",
                "não avise seus pais",
                "nao avise seus pais",
                "venha sozinho",
                "venha sozinha"
            ],
            "Possível tentativa de marcar encontro escondido."
        ),
        (
            [
                "vou te dar presentes",
                "te dou dinheiro se",
                "em troca de fotos",
                "comprei créditos para você",
                "comprei creditos para voce"
            ],
            "Possível oferta de dinheiro ou presentes em contexto suspeito."
        ),
        (
            [
                "apague nossa conversa",
                "apaga as mensagens",
                "não mostre esta conversa",
                "nao mostre esta conversa"
            ],
            "Possível tentativa de ocultar a conversa."
        ),
        (
            [
                "sou adulto, mas",
                "qual sua idade",
                "quantos anos você tem",
                "quantos anos voce tem"
            ],
            "Pergunta sobre idade ou diferença de idade: avaliar o contexto."
        )
    ]

    for palavras, descricao in regras_protecao:
        if any(palavra in texto for palavra in palavras):
            sinais.append(descricao)

    if sinais:
        nivel = "ATENÇÃO: revisar os indícios"
    else:
        nivel = "Nenhum sinal previsto nas regras foi encontrado"

    return nivel, sinais


# =====================================
# PESQUISA PÚBLICA
# =====================================

def pesquisar_internet(consulta):
    fontes = []

    if DDGS is None:
        return fontes

    try:
        with DDGS() as busca:
            resultados = busca.text(
                consulta + " golpe fraude Brasil",
                region="br-pt",
                max_results=5
            )

            for item in resultados:
                fontes.append({
                    "titulo": item.get("title", "Resultado"),
                    "url": item.get("href", ""),
                    "resumo": item.get("body", "")
                })
    except Exception:
        pass

    return fontes


# =====================================
# CONSULTAR A IA LOCAL
# =====================================

def consultar_ia(pergunta, sinais, fontes):
    contexto_fontes = ""

    for fonte in fontes:
        contexto_fontes += (
            "\nTítulo: " + fonte["titulo"] +
            "\nResumo: " + fonte["resumo"] +
            "\nEndereço: " + fonte["url"] + "\n"
        )

    contexto_sinais = "\n".join("- " + s for s in sinais)

    mensagens = [
        {
            "role": "system",
            "content": (
                "Você é a IA ALFA, especialista em prevenção de golpes "
                "digitais. Responda em português brasileiro, de forma clara "
                "e simples. Não afirme que existe fraude sem provas. "
                "Explique os riscos e recomende confirmar solicitações "
                "por canais oficiais. Nunca solicite senhas ou códigos.\n\n"
                "Sinais encontrados:\n" + contexto_sinais +
                "\n\nResultados públicos disponíveis:\n" + contexto_fontes
            )
        },
        {
            "role": "user",
            "content": pergunta
        }
    ]

    resposta = requests.post(
        OLLAMA_URL,
        json={
            "model": MODELO_IA,
            "messages": mensagens,
            "stream": False
        },
        timeout=120
    )

    resposta.raise_for_status()
    return resposta.json()["message"]["content"]


# =====================================
# VOZ
# =====================================

def ler_resposta(texto):
    if pyttsx3 is None:
        return False, "A biblioteca pyttsx3 não está instalada."

    try:
        motor = pyttsx3.init()
        motor.setProperty("rate", 175)
        motor.say(texto[:2000])
        motor.runAndWait()
        motor.stop()
        return True, ""
    except Exception as erro:
        return False, str(erro)


# =====================================
# MEMÓRIA DA PÁGINA
# =====================================

if "historico_alfa" not in st.session_state:
    st.session_state.historico_alfa = []

if "ultima_resposta" not in st.session_state:
    st.session_state.ultima_resposta = ""

if "ultima_fonte" not in st.session_state:
    st.session_state.ultima_fonte = []

if "voz_automatica" not in st.session_state:
    st.session_state.voz_automatica = False


# =====================================
# CABEÇALHO
# =====================================

st.markdown(
    '<div class="alfa-titulo">IA ALFA</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="alfa-descricao">'
    'ANTIGOLPES • ASSISTENTE DE SEGURANÇA DIGITAL'
    '</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="alfa-status">● CENTRAL DE ANÁLISE</div>',
    unsafe_allow_html=True
)

components.html(globo_html, height=335, scrolling=False)


# =====================================
# CONFIGURAÇÕES
# =====================================

with st.expander("⚙️ Configurações de voz"):
    st.session_state.voz_automatica = st.checkbox(
        "Ler as respostas automaticamente",
        value=st.session_state.voz_automatica
    )

st.markdown("### 🔎 Analisar mensagem")

st.write(
    "Cole abaixo um texto suspeito, mensagem de WhatsApp ou e-mail. "
    "Não inclua senhas nem códigos pessoais."
)


# =====================================
# CAMPO DE ANÁLISE
# =====================================

with st.form("formulario_analise"):
    pergunta = st.text_area(
        "Mensagem ou pergunta",
        placeholder=(
            "Exemplo: Seu banco bloqueou sua conta. "
            "Clique neste link e informe sua senha..."
        ),
        height=160
    )

    enviar = st.form_submit_button("🛡️ ANALISAR AGORA")


if enviar:
    pergunta = pergunta.strip()

    if not pergunta:
        st.warning("Digite uma mensagem antes de analisar.")
    else:
        sinais = analisar_golpe(pergunta)
        nivel_protecao, sinais_protecao = analisar_sinais_protecao(pergunta)
        with st.spinner("Analisando a mensagem..."):
            fontes = pesquisar_internet(pergunta)

            try:
                resposta = consultar_ia(pergunta, sinais, fontes)
            except requests.exceptions.ConnectionError:
                resposta = (
                    "Não consegui conectar à IA local.\n\n"
                    "Verifique se o Ollama está aberto e se o modelo "
                    "qwen2.5:0.5b está instalado. Os sinais básicos "
                    "continuam disponíveis abaixo."
                )
            except requests.exceptions.Timeout:
                resposta = (
                    "A IA demorou para responder. Tente novamente. "
                    "O computador pode estar ocupado."
                )
            except Exception as erro:
                resposta = (
                    "Não foi possível consultar a IA local. "
                    "Confira se o Ollama está funcionando.\n\n"
                    "Detalhe: " + str(erro)[:250]
                )

        resposta_completa = (
            resposta
            + "\n\n---\n\n"
            + "### Sinais encontrados\n"
            + "\n".join("- " + sinal for sinal in sinais)
            + "\n\n**Atenção:** esta análise não comprova fraude. "
              "Confirme informações importantes por um canal oficial."
        )
        resposta_completa += (
            "\n\n---\n\n"
            "### 🛡️ Proteção de crianças e adolescentes\n\n"
            + nivel_protecao
        )

        if sinais_protecao:
            resposta_completa += (
                "\n\n" +
                "\n".join("- " + sinal for sinal in sinais_protecao)
            )
        st.session_state.historico_alfa.append({
            "pergunta": pergunta,
            "resposta": resposta_completa,
            "fontes": fontes
        })

        st.session_state.ultima_resposta = resposta
        st.session_state.ultima_fonte = fontes

        if st.session_state.voz_automatica:
            sucesso, erro_voz = ler_resposta(resposta)

            if not sucesso:
                st.warning("A leitura automática não funcionou: " + erro_voz)

        st.rerun()


# =====================================
# RESULTADOS
# =====================================

if st.session_state.ultima_resposta:
    st.markdown("---")
    st.markdown("### 🔊 Voz e última resposta")

    if st.button("🔊 Ler última resposta"):
        sucesso, erro_voz = ler_resposta(
            st.session_state.ultima_resposta
        )

        if sucesso:
            st.success("Leitura concluída.")
        else:
            st.error("Não foi possível ler a resposta: " + erro_voz)

    if st.button("🌐 Ver fontes da última pesquisa"):
        if st.session_state.ultima_fonte:
            for fonte in st.session_state.ultima_fonte:
                st.markdown("**" + fonte["titulo"] + "**")

                url = fonte["url"]
                if url.startswith(("https://", "http://")):
                    st.markdown(f"[Abrir resultado]({url})")

                st.write(fonte["resumo"])
        else:
            st.info(
                "Nenhuma fonte foi encontrada. "
                "Verifique se a biblioteca ddgs está instalada."
            )


# =====================================
# HISTÓRICO
# =====================================

st.markdown("---")
st.markdown("### 📋 Histórico das análises")

if st.session_state.historico_alfa:
    for item in reversed(st.session_state.historico_alfa):
        with st.expander("Análise: " + item["pergunta"][:65]):
            st.markdown(item["resposta"])

            if item["fontes"]:
                st.markdown("**Fontes públicas:**")
                for fonte in item["fontes"]:
                    url = fonte["url"]
                    titulo = html.escape(fonte["titulo"])

                    if url.startswith(("https://", "http://")):
                        st.markdown(f"[{titulo}]({url})")
                    else:
                        st.write(fonte["titulo"])
else:
    st.info("Suas análises aparecerão aqui.")


# =====================================
# RODAPÉ
# =====================================

st.markdown("---")
st.caption(
    "IA ALFA ANTIGOLPES • Ferramenta de apoio à prevenção. "
    "Resultados podem estar incompletos; confirme em fontes oficiais."
)
