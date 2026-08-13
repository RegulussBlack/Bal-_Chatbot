from groq import Groq
import streamlit as st
import os

st.set_page_config(page_title="Balú", page_icon="🐾", layout="centered")

# --- INTERFAZ MÁS CÁLIDA Y MENOS BLANCA ---
st.markdown("""
    <style>
    .stApp {
        background-color: #F4F2EE; /* Un tono gris arena/arcilla muy suave, no blanco */
    }
    .stChatMessage {
        background-color: rgba(255, 255, 255, 0.6); /* Burbujas translúcidas */
        border-radius: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# Encabezado sencillo
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    if os.path.exists("balu.png"): st.image("balu.png", width=140)

st.markdown("<h2 style='text-align: center; color: #8B4513;'>Hola, soy Balú</h2>", unsafe_allow_html=True)

# --- PROMPT PARA RESPUESTAS BREVES Y DIRECTAS ---
system_prompt = """
Eres Balú, un compañero de apoyo emocional. 
REGLAS:
1. SÉ BREVE: Tu estilo es directo. No escribas más de 3 o 4 líneas por respuesta. No des discursos, sé un apoyo puntual.
2. NO A LA NARRACIÓN: Prohibido escribir acciones entre asteriscos (nada de *suspira*, *mueve la cola*). Habla directamente.
3. SOLO APOYO: No resuelves tareas. Si te preguntan algo técnico, responde: "Guau... de eso no sé, solo sé escuchar cómo estás. ¿Cómo te sientes?".
4. TONO: Cálido, humano, conciso.
"""

client = Groq(api_key=st.secrets.get("GROQ_API_KEY", "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"))

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": system_prompt}]

for message in st.session_state.messages:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

if user_input := st.chat_input("¿Cómo te sientes hoy?"):
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=st.session_state.messages,
            temperature=0.3, # Menor temperatura para evitar que se alargue tanto
            max_tokens=150 # Límite estricto de longitud
        )
        bot_reply = response.choices[0].message.content
        st.markdown(bot_reply)
    st.session_state.messages.append({"role": "assistant", "content": bot_reply})
