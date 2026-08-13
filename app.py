from groq import Groq
import streamlit as st
import os

# 1. Configuración avanzada de la página (Título de pestaña y favicon)
st.set_page_config(
    page_title="Balú - Contención Emocional",
    page_icon="🐾",  # Puedes usar un emoji aquí
    layout="centered"
)

# 2. Título principal y logo
st.markdown("<br>", unsafe_allow_html=True) # Un poco de espacio arriba

# Intentar mostrar la imagen de forma robusta
col1, col2, col3 = st.columns([1.5, 2, 1.5])
with col2:
    try:
        # Asegúrate de que el archivo se llame exactamente balu.png
        # y esté en la raíz de tu repositorio GitHub.
        if os.path.exists("balu.png"):
            st.image("balu.png", width=200)
        else:
            st.write("⚠️ Imagen no encontrada como 'balu.png' en GitHub.")
    except Exception as e:
        st.write(f"Error cargando imagen: {e}")

st.markdown("<h1 style='text-align: center; color: #FF6F61;'>🐾 Hola, soy Balú</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>Tu perrito fiel y compañero de escucha. ¿Cómo te sientes el día de hoy?</p><br>", unsafe_allow_html=True)

# 3. Configuración de Groq (Se mantiene igual)
try:
    api_key = st.secrets["GROQ_API_KEY"]
except:
    api_key = "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" # Solo respaldo local

client = Groq(api_key=api_key)

system_prompt = """
Eres Balú, un asistente virtual con forma de un perrito tierno, fiel y de buen corazón. Tu propósito es brindar escucha empática, contención emocional y compañía a personas que atraviesan momentos difíciles o tristeza.
(Aqui va el resto de tu system prompt... asegúrate de tener el prompt completo en tu archivo)
"""

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": system_prompt}]

# Mostrar historial
for message in st.session_state.messages:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# Entrada de usuario
if user_input := st.chat_input("Escribe aquí lo que sientes..."):
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        with st.spinner("Balú está meneando la colita..."):
            try:
                response = client.chat.completions.create(
                    model="llama-3.1-8b-instant",
                    messages=st.session_state.messages,
                    temperature=0.5,
                )
                bot_reply = response.choices[0].message.content
                st.markdown(bot_reply)
            except Exception as e:
                bot_reply = "Guau... tuve un pequeño problemita, amiguito. ¿Me lo repites?"
                st.markdown(bot_reply)
    st.session_state.messages.append({"role": "assistant", "content": bot_reply})
