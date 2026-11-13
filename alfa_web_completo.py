import streamlit as st

import os

import streamlit.components.v1 as components

import requests

from openai import OpenAI

import re

import html

import ipaddress

import json

try:

    import pyttsx3

except ImportError:

    pyttsx3 = None



try:

    from ddgs import DDGS

except ImportError:

    DDGS = None





# =====================================

# CONFIGURACAO

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

 # GLOBO ANIMADO  MANTIDO

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

            ["pix", "transferencia", "transferencia", "deposito",

             "deposito"],

            "Menssao a Pix, deposito ou transferencia."

        ),

        (

            ["senha", "token", "codigo de seguransa",

             "codigo de seguranca", "codigo de acesso"],

            "Menssao a senha ou codigo de seguransa."

        ),

        (

            ["premio", "premio", "ganhou", "sorteio",

             "dinheiro gratis", "dinheiro gratis"],

            "Possivel promessa de premio ou dinheiro."

        ),

        (

            ["urgente", "imediatamente", "ultima chance",

             "ultima chance", "agora mesmo"],

            "Pressao para agir rapidamente."

        ),

        (

            ["conta bloqueada", "cartao bloqueado",

             "cartao bloqueado", "conta suspensa"],

            "Possivel ameassa de bloqueio de conta ou cartao."

        ),

        (

            ["clique aqui", "acesse o link", "confirme seus dados"],

            "Pedido para clicar em link ou confirmar dados."

        ),

        (

            ["taxa para liberar", "pague a taxa",

             "taxa antecipada", "taxa de liberasso"],

            "Possivel cobranca antecipada."

        ),

        (

            ["cpf", "dados bancarios", "dados bancarios",

             "numero do cartao", "numero do cartao"],

            "Mensao a dados pessoais ou bancarios."

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

            "Existe um endereco de internet. Verifique o dominio antes de abrir."

        )



    if not sinais:

        sinais.append(

            "Nenhum sinal conhecido foi identificado pelas regras basicas. "

            "Isso nao garante que a mensagem seja segura."

        )



    return sinais



# =====================================

# PROTECAO DE CRIANCAS E ADOLESCENTES

# =====================================



def analisar_sinais_protecao(texto):

    texto = texto.lower()

    sinais = []



    regras_protecao = [

        (

            [

                "nao conte para seus pais",

                "nao conte para seus pais",

                "mantenha em segredo",

                "isso fica entre nas",

                "isso fica entre nos"

            ],

            "Possivel tentativa de impor segredo a uma crianca."

        ),

        (

            [

                "mande uma foto intima",

                "mande uma foto intima",

                "envie fotos sem roupa",

                "foto sem roupa",

                "mostre seu corpo"

            ],

            "Possivel solicitacao de imagem intima."

        ),

        (

            [

                "encontro escondido",

                "nao avise seus pais",

                "nao avise seus pais",

                "venha sozinho",

                "venha sozinha"

            ],

            "Possivel tentativa de marcar encontro escondido."

        ),

        (

            [

                "vou te dar presentes",

                "te dou dinheiro",

                "compro presentes",

                "nao precisa contar",

                "nao precisa contar"

            ],

            "Possivel tentativa de ganhar confianca oferecendo vantagens."

        ),

        (

            [

                "qual sua idade",

                "onde voce mora",
                
                "esta sozinho",

                 
            ],

            "Pergunta pessoal que pode exigir atencao de um responsavel."

        )

    ]



    for palavras, descricao in regras_protecao:

        if any(p in texto for p in palavras):

            sinais.append(descricao)



    return sinais
    # =====================================
    # PROTECAO DE CRIANCAS E ADOLESCENTES
    # =====================================

def analisar_sinais_protecao(texto):

    texto = texto.lower()

    sinais = []

    regras_protecao = [

        (
            [
                "nao conte para seus pais",
                "nao conte para seus pais",
                "mantenha em segredo",
                "isso fica entre nas",
                "isso fica entre nos"
            ],

            "Possivel tentativa de impor segredo a uma criancas."
        ),

        (
            [
                "mande uma foto intima",
                "mande uma foto intima",
                "envie fotos sem roupa",
                "foto sem roupa",
                "mostre seu corpo"
            ],

            "Possivel solicitacao de imagem intima."
        ),

        (
            [
                "encontro escondido",
                "nao avise seus pais",
                "nao avise seus pais",
                "venha sozinho",
                 
            ],

            "Possivel tentativa de marcar encontro escondido."
        ),

        (
            [
                "vou te dar presentes",
                "te dou dinheiro se",
                "em troca de fotos",
                 "comprei creditos para voce",
                 
            ],

            "Possivel oferta de dinheiro ou presentes em contexto suspeito."
        ),

        (
            [
                "apague nossa conversa",
                "apaga as mensagens",
                "nao mostre esta conversa",
                 
            ],

            "Possivel tentativa de ocultar a conversa."
        ),

        (
            [
                "sou adulto, mas",
                "qual sua idade",
                "quantos anos voce tem",
                 
            ],

            "Pergunta sobre idade ou diferensa de idade: avaliar o contexto."
        )

    ]

    for palavras, descricao in regras_protecao:

        if any(palavra in texto for palavra in palavras):

            sinais.append(descricao)

    if sinais:

        nivel = "ATENCAO: revisar os indicios"

    else:

        nivel = "Nenhum sinal previsto nas regras foi encontrado"

    return nivel, sinais


# =====================================
# PESQUISA BIBLICA
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
            "\ntitulo: " + fonte["titulo"] +
            "\nResumo: " + fonte["resumo"] +
            "\nEndereso: " + fonte["url"] + "\n"
        )

    contexto_sinais = "\n".join("- " + s for s in sinais)

    mensagens = [
        {
            "role": "system",
            "content": (
             "Voce a IA ALFA, uma assistente especializada em prevencao de golpes digitais no Brasil. "
"Sua prioridade e analisar golpes por Pix, WhatsApp, SMS, e-mail, telefone e links suspeitos e localisar de onde vem pelo gps google. "
"Responda sempre em portugues brasileiro, de forma clara, educada e objetiva. "
"Nao mude de assunto e nao invente informacoes. "
"Nao fale sobre jogos, brincadeiras ou jogo da velha, a menos que o usuario pergunte diretamente. "
"Quando receber uma mensagem suspeita, explique os riscos e como se proteger. "
"Nao afirme que existe fraude sem evidencias. "
"Nunca pensa senhas, codigos de segurancas ou dados bancarios.\n\n"
"Sinais encontrados:\n" + contexto_sinais +
"\n\nResultados autenticos disponiveis:\n" + contexto_fontes
            )
        },
        {
            "role": "user",
            "content": pergunta
        }
    ]

    usar_gpt = os.getenv("IA_ALFA_GPT") == "1"

    try:
        usar_gpt = usar_gpt or str(st.secrets.get("IA_ALFA_GPT", "0")) == "1"
    except Exception:
        pass

    if usar_gpt:
        cliente = OpenAI(
            api_key=st.secrets["openai"]["api_key"]
        )

        resposta = cliente.chat.completions.create(
            model="gpt-4o-mini",
            messages=mensagens,
            timeout=120
        )

        return resposta.choices[0].message.content

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

        return False, "A biblioteca pyttsx3 nao esta instalada."

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
# MEMORIA DA PAGINA
# =====================================

if "historico_alfa" not in st.session_state:

    st.session_state.historico_alfa = []

if "ultima_resposta" not in st.session_state:

    st.session_state.ultima_resposta = ""

if "ultima_fonte" not in st.session_state:

    st.session_state.ultima_fonte = []


# =====================================
#  # CABECALHO
# =====================================

st.markdown(

    '<div class="alfa-titulo">IA ALFA</div>',

    unsafe_allow_html=True

)

st.markdown(

    '<div class="alfa-descricao">'

    'ANTIGOLPES A ASSISTENTE DE SEGURANCA DIGITAL'

    '</div>',

    unsafe_allow_html=True

)

st.markdown(

    '<div class="alfa-status">A CENTRAL DE ANALISE</div>',

    unsafe_allow_html=True

)

components.html(globo_html, height=335, scrolling=False)


# =====================================
# CONFIGURACOES
# =====================================

with st.expander("as Configuracoes de voz"):

    st.write("Use o botao de voz abaixo para ouvir a resposta pelo navegador.")

    st.markdown("### 🔎 Analisar mensagem")

st.write(
    "Cole abaixo um texto suspeito, mensagem de WhatsApp ou e-mail. "
    "Nao inclua senhas nem codigos pessoais."
)


# =====================================
# CAMPO DE ANALISE
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

    enviar = st.form_submit_button( "🛡️ ANALISAR AGORA")


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

                    "Nao consegui conectar a IA local.\n\n"

                    "Verifique se o Ollama esta aberto e se o modelo "

                    "qwen2.5:0.5b esta instalado. Os sinais basicos "

                    "continuam disponiveis abaixo."

                )

            except requests.exceptions.Timeout:

                resposta = (

                    "A IA demorou para responder. Tente novamente. "

                    "O computador pode estar ocupado."

                )

            except Exception as erro:

                resposta = (

                    "Nao foi possivel consultar a IA local. "

                    "Confira se o Ollama esta funcionando.\n\n"

                    "Detalhe: " + str(erro)[:250]

                )

        resposta_completa = (

            resposta

            + "\n\n---\n\n"

            + "### Sinais encontrados\n"

            + "\n".join("- " + sinal for sinal in sinais)

            + "\n\n**Atencao:** esta analise nao comprova fraude. "

              "Confirme informacoes importantes por um canal oficial."

        )

        resposta_completa += (

            "\n\n---\n\n"

             "### 🛡️ Protecao de criancas e adolescentes\n\n"

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

        st.session_state.ultima_resposta = resposta_completa

        st.session_state.ultima_fonte = fontes

        st.rerun()


# =====================================
# RESULTADOS
# =====================================

if st.session_state.ultima_resposta:

    st.markdown("---")

    st.markdown("### 🔊 Resultado da análise")

    st.markdown(st.session_state.ultima_resposta)

    st.markdown("### 🔊 Ouvir resposta")

    texto_para_voz = json.dumps(

        st.session_state.ultima_resposta,

        ensure_ascii=False

    )

    components.html(

        f"""

        <button id="botao_voz_alfa"

            style="padding:12px 18px;border:0;border-radius:10px;

                   background:linear-gradient(90deg,#087bff,#00b9ff);

                   color:white;font-weight:bold;cursor:pointer;width:100%;">

            " 🔊 Ouvir resposta da IA ALFA"

        </button>

        <script>

        const textoAlfa = {texto_para_voz};

        const botaoAlfa = document.getElementById("botao_voz_alfa");

        botaoAlfa.addEventListener("click", function() {{

            if (!("speechSynthesis" in window)) {{

                alert("A voz nao esta disponivel neste navegador.");

                return;

            }}

            window.speechSynthesis.cancel();

            const fala = new SpeechSynthesisUtterance(textoAlfa.replace(/\*/g, "").replace(/#/g, ""));

            fala.lang = "pt-BR";

            fala.rate = 0.95;

            window.speechSynthesis.speak(fala);

        }});

        </script>

        """,

        height=65,

        scrolling=False

    )

    if st.button( "🌐 Ver fontes da última pesquisa"):

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

                "Verifique se a biblioteca ddgs estÃ¡ instalada."

            )


# =====================================
# HISTORICO
# =====================================

st.markdown("---")

st.markdown("###  📋 Historico das analises")

if st.session_state.historico_alfa:

    for item in reversed(st.session_state.historico_alfa):

        with st.expander("analise: " + item["pergunta"][:65]):

            st.markdown(item["resposta"])

            if item["fontes"]:

                st.markdown("**Fontes pÃºblicas:**")

                for fonte in item["fontes"]:

                    url = fonte["url"]

                    titulo = html.escape(fonte["titulo"])

                    if url.startswith(("https://", "http://")):

                        st.markdown(f"[{titulo}]({url})")

                    else:

                        st.write(fonte["titulo"])

else:

    st.info("Suas analises aparecerrao aqui.")


# =====================================
# RODAPE
# =====================================

 
# =====================================
# PAGAMENTOS IA ALFA
# =====================================

st.markdown("---")
st.subheader("🔐 Acesso premium IA ALFA")
st.write("Acesse a IA ALFA por 24 horas.")
st.markdown("### R$ 10,00")

st.link_button(
    "💚 PAGAR COM PICPAY",
    "https://link.picpay.com/p/17945998796af76bc7e329a",
    use_container_width=True
)

st.link_button(
    "💙 PAGAR COM MERCADO PAGO",
    "https://mpago.la/2gVZnyS",
    use_container_width=True
)


    


st.markdown("---")

st.caption(

    "IA ALFA ANTIGOLPES e Ferramenta de apoio a prevencao. "

    "Resultados podem estar incompletos; confirme e ligue para policia 190."

)


