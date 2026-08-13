from groq import Groq
import streamlit as st
import os

st.set_page_config(page_title="Balú - Contención Emocional", page_icon="🐾", layout="centered")

# --- ESTILOS CSS DEFINITIVOS PARA ALTA VISIBILIDAD ---
st.markdown("""
    <style>
    /* Fondo general gris arena muy suave (nada de blancos agresivos) */
    .stApp {
        background-color: #F0ECE1; 
    }
    
    /* Forzar que CUALQUIER texto de los mensajes sea negro y legible */
    .stChatMessage p, .stChatMessage div {
        color: #1A1A1A !important;
        font-size: 1.1rem;
    }

    /* FORZAR QUE LA CAJA DE TEXTO INFERIOR SEA BLANCA CON LETRAS NEGRAS */
    [data-testid="stChatInput"] textarea {
        color: #000000 !important;
        background-color: #FFFFFF !important;
        font-size: 1.1rem !important;
    }
    
    /* Color del texto guía dentro de la caja */
    [data-testid="stChatInput"] textarea::placeholder {
        color: #555555 !important;
    }
    </style>
""", unsafe_allow_html=True)

# Encabezado
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    if os.path.exists("balu.png"): 
        st.image("balu.png", width=140)

st.markdown("<h2 style='text-align: center; color: #783F04;'>Hola, soy Balú</h2>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #444444;'>Tu perrito fiel y compañero de escucha. Estoy aquí para ti.</p>", unsafe_allow_html=True)

# --- PROMPT BREVE Y DIRECTO ---
system_prompt = """
Eres Balú, un perrito de apoyo emocional. 
REGLAS ESTRICTAS:
1. BREVEDAD: Sé muy directo. No escribas más de 3 o 4 líneas. Evita párrafos largos.
2. SIN ASTERISCOS: Prohibido narrar acciones (nada de *suspira*, *mueve la cola*). Habla con palabras cálidas y reales.
3. LÍMITES: Si te preguntan de programación u otros temas, responde con ternura: "Guau... de eso no sé nada, amiguito, ¡yo solo sé escuchar cómo estás!".
"""

client = Groq(api_key=st.secrets.get("GROQ_API_KEY", "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"))

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": system_prompt}]

for message in st.session_state.messages:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

if user_input := st.chat_input("Escribe aquí cómo te sientes..."):
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=st.session_state.messages,
            temperature=0.3,
            max_tokens=150
        )
        bot_reply = response.choices[0].message.content
        st.markdown(bot_reply)
    st.session_state.messages.append({"role": "assistant", "content": bot_reply})
