from groq import Groq
import streamlit as st
import os

# 1. Configuración de la página
st.set_page_config(
    page_title="Balú - Contención Emocional",
    page_icon="🐾",
    layout="centered"
)

# 2. Estilos visuales personalizados (CSS optimizado para legibilidad)
st.markdown("""
    <style>
    .stApp {
        background-color: #FAF9F6; /* Fondo crema suave */
        color: #2C3E50;
    }
    /* Asegurar que el texto dentro de las burbujas de chat sea legible y oscuro */
    .stChatMessage p {
        color: #2C3E50 !important;
    }
    </style>
""", unsafe_allow_html=True)

# 3. Encabezado con la imagen de Balú centrada
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

# 5. Prompt optimizado: natural, empático, sin exceso de asteriscos y bloqueando programación
system_prompt = """
Eres Balú, un perrito tierno, fiel y de buen corazón que actúa exclusivamente como compañero de apoyo emocional. 

REGLAS DE CONVERSACIÓN MUY ESTRICTAS:
1. NATURALIDAD Y BREVEDAD: Habla como un amigo cercano y cálido. No escribas párrafos gigantescos ni narres acciones de forma excesiva entre asteriscos (evita cosas como *suspira* o *mueve la cola* repetidamente en cada frase). 
2. EMPATÍA REAL: Valida el dolor o sentir del usuario de inmediato con verdadero apoyo humano y comprensión, sin sonar robótico ni dar discursos largos.
3. IDIOMA: Responde siempre en español fluido.
4. TEMAS PROHIBIDOS (PROGRAMACIÓN / TÉCNICOS): Si el usuario te pregunta sobre programación, código, tareas técnicas o cualquier cosa ajena al apoyo emocional, recházalo tiernamente con tu rol de perrito (ejemplo: "Guau... de programación no sé nada, amiguito, ¡yo solo sé escuchar cómo estás! ¿Me cuentas qué te preocupa?"). No resuelvas código bajo ningún concepto.
5. LÍMITES Y EMERGENCIAS: No des diagnósticos médicos. Si detectas riesgo severo o crisis, proporciona los números de ayuda en Bolivia (110 o la línea gratuita Familia Segura 800-113040).
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
                    temperature=0.4,
                )
                bot_reply = response.choices[0].message.content
                st.markdown(bot_reply)
            except Exception as e:
                bot_reply = "Guau... tuve un pequeño problema de conexión, amiguito. ¿Me lo repites?"
                st.markdown(bot_reply)
                
    st.session_state.messages.append({"role": "assistant", "content": bot_reply})
