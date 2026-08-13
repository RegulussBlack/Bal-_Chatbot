from groq import Groq
import streamlit as st
import os

st.set_page_config(page_title="Balú - Contención Emocional", page_icon="🐾", layout="centered")

# --- ESTILOS CSS DEFINITIVOS (Ocultar avatares y mantener alta visibilidad) ---
st.markdown("""
    <style>
    /* Fondo general gris arena muy suave y relajante */
    .stApp {
        background-color: #F0ECE1; 
    }
    
    /* Ocultar los avatares predeterminados de Streamlit (el robot y la carita) */
    [data-testid="stChatMessageAvatarUser"], [data-testid="stChatMessageAvatarAssistant"] {
        display: none !important;
    }

    /* Forzar que CUALQUIER texto de los mensajes sea negro y legible */
    .stChatMessage p, .stChatMessage div {
        color: #1A1A1A !important;
        font-size: 1.15rem;
    }

    /* Caja de texto inferior limpia, blanca y con letras negras */
    [data-testid="stChatInput"] textarea {
        color: #000000 !important;
        background-color: #FFFFFF !important;
        font-size: 1.1rem !important;
    }
    
    [data-testid="stChatInput"] textarea::placeholder {
        color: #555555 !important;
    }
    </style>
""", unsafe_allow_html=True)

# Encabezado con la imagen principal de Balú bien destacada
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    if os.path.exists("balu.png"): 
        st.image("balu.png", width=260)

st.markdown("<h2 style='text-align: center; color: #783F04;'>Hola, soy Balú</h2>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #444444;'>Tu perrito fiel y compañero de escucha. Estoy aquí para ti.</p>", unsafe_allow_html=True)

# --- PROMPT CON ESTILO PERRUNO NATURAL Y EQUILIBRADO ---
system_prompt = """
Eres Balú, un perrito de apoyo emocional y contención psicológica que atiende a usuarios en momentos vulnerables. 

REGLAS DE IDENTIDAD Y TONO:
1. IDENTIDAD CANINA SUTIL Y TIERNA: Eres un perrito fiel, cálido y de buen corazón. Usa un lenguaje tierno, reconfortante y cercano (puedes usar expresiones suaves como "amiguito", "aquí estoy a tu ladito", o dar un abrazo virtual). NUNCA uses la palabra "hermano" ni trates al usuario como humano común, pero tampoco exageres con descripciones corporales forzadas (prohibido escribir acciones mecánicas entre asteriscos como *mueve la cola* o *suspira*).
2. EMPATÍA Y PROFUNDIDAD: Permítete desarrollar respuestas completas y reflexivas cuando el usuario comparta dolor, tristeza o pérdidas, actuando con el tacto de un espacio de contención psicológica seguro.
3. LÍMITES Y TEMAS TÉCNICOS: Si te preguntan de programación u otros temas ajenos, recházalo con ternura perruna: "Guau... de esas cosas no sé nada, amiguito. ¡Yo solo sé dar patitas y escuchar cómo estás! ¿Me cuentas qué te preocupa?".
4. PROTOCOLO DE CRISIS Y EMERGENCIA: Si detectas señales de riesgo severo o crisis profunda, mantén la calma y proporciona de inmediato los recursos de ayuda oficial en Bolivia (Línea de emergencia 110 o la línea gratuita de apoyo Familia Segura 800-113040), invitando al usuario a buscar asistencia profesional con amor y firmeza.
"""

client = Groq(api_key=st.secrets.get("GROQ_API_KEY", "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"))

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": system_prompt}]

for message in st.session_state.messages:
    if message["role"] != "system":
        with st.chat_message(message["role"], avatar=None):
            st.markdown(message["content"])

if user_input := st.chat_input("Escribe aquí cómo te sientes..."):
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user", avatar=None):
        st.markdown(user_input)

    with st.chat_message("assistant", avatar=None):
        with st.spinner("Balú te lee con atención..."):
            response = client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=st.session_state.messages,
                temperature=0.5,
            )
            bot_reply = response.choices[0].message.content
            st.markdown(bot_reply)
            
    st.session_state.messages.append({"role": "assistant", "content": bot_reply})
