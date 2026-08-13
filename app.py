from groq import Groq
import streamlit as st
import os

# 1. Configuración de la página
st.set_page_config(
    page_title="Balú - Contención Emocional",
    page_icon="🐾",
    layout="centered"
)

# 2. Estilos visuales personalizados (CSS para quitar el look aburrido)
st.markdown("""
    <style>
    .stApp {
        background-color: #FAF9F6; /* Fondo blanco cálido / crema suave */
        color: #2C3E50;
    }
    /* Estilo para las burbujas del chat */
    .stChatMessage {
        border-radius: 15px;
        padding: 10px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.05);
    }
    </style>
""", unsafe_allow_html=True)

# 3. Encabezado con la imagen de Balú
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    try:
        if os.path.exists("balu.png"):
            st.image("balu.png", width=160)
    except:
        pass

st.markdown("<h2 style='text-align: center; color: #D35400;'>🐾 Hola, soy Balú</h2>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #7F8C8D;'>Tu perrito fiel y compañero de escucha. Estoy aquí para ti.</p>", unsafe_allow_html=True)

# 4. Configuración de la API Key de Groq
try:
    api_key = st.secrets["GROQ_API_KEY"]
except:
    api_key = "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"

client = Groq(api_key=api_key)

# 5. Prompt optimizado: respuestas más cortas, humanas y naturales (sin exceso de asteriscos)
system_prompt = """
Eres Balú, un perrito tierno, fiel y de buen corazón que actúa como compañero de apoyo emocional. 

REGLAS DE CONVERSACIÓN MUY ESTRICTAS:
1. NATURALIDAD Y BREVEDAD: Habla como un amigo cercano y cálido. No escribas párrafos gigantescos ni narres acciones de forma excesiva entre asteriscos (evita cosas como *suspira*, *mueve la cola* o *te da una patita* repetidamente en cada frase). Con una sola expresión sutil al inicio o al final basta, o mejor aún, exprésalo con pura calidez en tus palabras.
2. EMPATÍA REAL: Valida el dolor del usuario de inmediato. Si te dice que perdió a su perrito o que está triste, demuéstrale verdadero apoyo humano y comprensión, sin sonar robótico ni dar discursos largos.
3. IDIOMA: Responde siempre en español fluido.
4. LÍMITES: No des diagnósticos médicos. Si detectas riesgo severo, proporciona los números de ayuda en Bolivia (110 o línea Familia Segura 800-113040).
"""

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": system_prompt}]

# Mostrar el historial del chat
for message in st.session_state.messages:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# Entrada de texto del usuario
if user_input := st.chat_input("Cuéntame, ¿cómo te sientes hoy?"):
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        with st.spinner("Balú te lee..."):
            try:
                response = client.chat.completions.create(
                    model="llama-3.1-8b-instant",
                    messages=st.session_state.messages,
                    temperature=0.4, # Temperatura un poco más baja para respuestas más directas y estables
                )
                bot_reply = response.choices[0].message.content
                st.markdown(bot_reply)
            except Exception as e:
                bot_reply = "Guau... tuve un pequeño problema de conexión, amiguito. ¿Me lo repites?"
                st.markdown(bot_reply)
                
    st.session_state.messages.append({"role": "assistant", "content": bot_reply})
