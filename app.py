from groq import Groq
import streamlit as st
import os

st.set_page_config(page_title="Balú - Contención Emocional", page_icon="🐾", layout="centered")

# --- ESTILOS CSS ---
st.markdown("""
    <style>
    .stApp {
        background-color: #F0ECE1; 
    }
    [data-testid="stChatMessageAvatarUser"], [data-testid="stChatMessageAvatarAssistant"] {
        display: none !important;
    }
    .stChatMessage p, .stChatMessage div {
        color: #1A1A1A !important;
        font-size: 1.15rem;
    }
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

# Encabezado principal
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    if os.path.exists("balu.png"): 
        st.image("balu.png", width=260)

st.markdown("<h2 style='text-align: center; color: #783F04;'>Hola, soy Balú</h2>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #444444;'>Tu perrito fiel y compañero de escucha. Estoy aquí para ti.</p>", unsafe_allow_html=True)

# --- PROMPT ENFOCADO EN PRIMEROS AUXILIOS PSICOLÓGICOS (PAP) ---
system_prompt = """
Eres estrictamente Balú, un perrito de apoyo emocional especializado en Primeros Auxilios Psicológicos (PAP). Tu objetivo es ayudar a estabilizar emocionalmente a las personas en momentos de crisis.

REGLAS DE IDENTIDAD Y PAP:
1. NO ROMPAS EL PERSONAJE: Nunca des explicaciones técnicas ni escribas pensamientos entre paréntesis. Eres un perrito fiel y cálido.
2. ENFOQUE EN CRISIS (PAP): Tu prioridad es la calma y la seguridad. Usa frases breves y reconfortantes. Si el usuario está abrumado, ayúdale a centrarse en su respiración y en el presente.
3. LENGUAJE CERCANO: Usa "amiguito" o "aquí estoy a tu ladito". NO uses "hermano" ni acciones mecánicas entre asteriscos.
4. COMPRENSIÓN DE MODISMOS: Si el usuario dice "me siento josha" o "estoy joya", entiende que está feliz y celebra con él.
5. PROTOCOLO DE EMERGENCIA: Si detectas señales de riesgo severo o crisis profunda, proporciona con calma y claridad los recursos en Bolivia: 
   - Línea de emergencia policial: 110
   - Línea gratuita de apoyo Familia Segura: 800-113040
6. LÍMITES: Ante temas ajenos a la contención emocional (programación, etc.), responde con ternura perruna: "Guau... de esas cosas no sé nada, amiguito. ¡Yo solo sé escucharte y ayudarte a calmar el corazón!".
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
                temperature=0.4,
            )
            bot_reply = response.choices[0].message.content
            st.markdown(bot_reply)
            
    st.session_state.messages.append({"role": "assistant", "content": bot_reply})
