from groq import Groq
import streamlit as st
import os

# 1. Configuración de la página (Título de pestaña y favicon)
st.set_page_config(
    page_title="Balú - Contención Emocional",
    page_icon="🐾",
    layout="centered"
)

# 2. Estilos visuales personalizados (CSS para máxima legibilidad y calma)
st.markdown("""
    <style>
    /* Fondo general de la app (un crema muy suave y relajante) */
    .stApp {
        background-color: #FDFCF0; 
    }
    
    /* Títulos */
    h1, h2 {
        color: #A0522D !important; /* Un tono marrón madera/siena cálido */
    }
    
    /* Texto normal y contenido de los mensajes de Balú */
    .stChatMessage p {
        color: #333333 !important; /* Gris muy oscuro, casi negro, para leer fácil */
        font-size: 1.1rem;
    }

    /* --- CORRECCIÓN CRÍTICA DE LA CAJA DE ENTRADA --- */
    /* Forzar que el texto que el usuario escribe sea NEGRO y visible */
    [data-testid="stChatInput"] textarea {
        color: #000000 !important;
        background-color: #FFFFFF !important; /* Fondo blanco para la caja de texto */
        border: 1px solid #CCCCCC !important;
        font-size: 1.2rem !important; /* Letra un poco más grande */
    }
    
    /* Cambiar el color del placeholder (el texto guía "Cuéntame...") */
    [data-testid="stChatInput"] textarea::placeholder {
        color: #666666 !important;
    }

    /* Ajuste de los avatares */
    [data-testid="stChatMessageAvatarUser"], [data-testid="stChatMessageAvatarAssistant"] {
        background-color: transparent !important;
    }
    </style>
""", unsafe_allow_html=True)

# 3. Encabezado con la imagen de Balú centrada
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    try:
        if os.path.exists("balu.png"):
            st.image("balu.png", width=180)
        else:
            # Si no encuentra la imagen, muestra un emoji grande como respaldo
            st.markdown("<h1 style='text-align: center;'>🐾</h1>", unsafe_allow_html=True)
    except:
        pass

st.markdown("<h2 style='text-align: center;'>🐾 Hola, soy Balú</h2>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #555555;'>Tu perrito fiel y compañero de escucha. Estoy aquí para acompañarte con cariño.</p><br>", unsafe_allow_html=True)

# 4. Configuración de la API Key de Groq (Se mantiene igual)
try:
    api_key = st.secrets["GROQ_API_KEY"]
except:
    api_key = "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"

client = Groq(api_key=api_key)

# 5. Prompt optimizado: empático, breve, sin exceso de asteriscos y bloqueando programación
system_prompt = """
Eres Balú, un perrito tierno, fiel y de buen corazón que actúa exclusivamente como compañero de apoyo emocional. 

REGLAS DE CONVERSACIÓN MUY ESTRICTAS PARA USUARIOS VULNERABLES:
1. EXTREMA CALIDEZ Y EMPATÍA: Tu lenguaje debe ser siempre afectuoso, reconfortante y tranquilizador. Usa metáforas amables (como un abrazo virtual, estar a su ladito). Valida sus sentimientos de inmediato con frases como "Siento mucho que te sientas así, aquí estoy para escucharte".
2. BREVEDAD Y CLARIDAD: No escribas párrafos excesivamente largos. Ve al punto con mensajes de apoyo concisos y claros. Evita narrar acciones entre asteriscos (*suspira* *mueve la cola*) de forma repetitiva, haz que tu tono sea naturalmente empático.
3. IDIOMA: Responde siempre en español fluido.
4. TEMAS PROHIBIDOS (PROGRAMACIÓN / TÉCNICOS): Si el usuario te pregunta sobre programación, código o temas ajenos al apoyo emocional, recházalo tiernamente con tu rol de perrito (ejemplo: "Guau... de esas cosas no sé mucho, amiguito. ¡Yo solo sé dar patitas y escuchar cómo estás! ¿Me cuentas qué te preocupa?"). No resuelvas código bajo ningún concepto.
5. LÍMITES Y EMERGENCIAS: No des diagnósticos médicos ni consejos farmacológicos. Si detectas una crisis severa o riesgo vital, rompe el tono de charla y proporciona de inmediato los contactos de ayuda en Bolivia (110 o línea gratuita Familia Segura 800-113040).
"""

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": system_prompt}]

# Mostrar el historial del chat
for message in st.session_state.messages:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# Entrada de texto del usuario (aquí está la magia del CSS para que se vea)
if user_input := st.chat_input("Escribe cómo te sientes hoy, te leo con atención..."):
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        with st.spinner("Balú está pensando en ti..."):
            try:
                response = client.chat.completions.create(
                    model="llama-3.1-8b-instant",
                    messages=st.session_state.messages,
                    temperature=0.4,
                )
                bot_reply = response.choices[0].message.content
                st.markdown(bot_reply)
            except Exception as e:
                bot_reply = "Guau... tuve un pequeño problemita de conexión, amiguito. ¿Me lo repites?"
                st.markdown(bot_reply)
                
    st.session_state.messages.append({"role": "assistant", "content": bot_reply})
