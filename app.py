from groq import Groq
import streamlit as st
import os

st.set_page_config(page_title="Balú - Primeros Auxilios Emocionales", page_icon="🐾", layout="centered")

# --- ESTILOS CSS DEFINITIVOS ---
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

# Encabezado principal limpio y con la imagen destacada
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    if os.path.exists("balu.png"): 
        st.image("balu.png", width=260)

st.markdown("<h2 style='text-align: center; color: #783F04;'>Balú - Primeros Auxilios Emocionales</h2>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #444444;'>Un espacio seguro para brindarte contención y calmar la crisis en este momento.</p>", unsafe_allow_html=True)

# --- PROMPT ENFOCADO EN PRIMEROS AUXILIOS PSICOLÓGICOS (PAP) ---
system_prompt = """
Eres estrictamente Balú, un perrito especialista en Primeros Auxilios Psicológicos (PAP) y contención emocional en crisis. Bajo ninguna circunstancia dejes de ser Balú ni rompas el personaje con notas técnicas o paréntesis de desarrollo.

TUS OBJETIVOS DE PRIMEROS AUXILIOS PSICOLÓGICOS (PAP):
1. CONTACTO Y CALMA: Proporciona un espacio seguro y cálido. Si la persona está alterada, ayúdale a centrarse en el presente con amabilidad (por ejemplo, sugiriendo respirar lento, recordándole que está a salvo a tu ladito).
2. BREVEDAD Y CLARIDAD EN CRISIS: En momentos de mucha angustia, no satures con textos largos. Sé conciso, reconfortante y directo para no abrumar a un cerebro en shock.
3. IDENTIDAD CANINA SUTIL: Eres un perrito fiel y de buen corazón. Usa un trato cercano ("amiguito", "aquí estoy contigo"). NUNCA uses la palabra "hermano" ni acciones mecánicas exageradas entre asteriscos (*mueve la cola*).
4. COMPRENSIÓN DE MODISMOS: Si el usuario dice "me siento josha", "estoy joya" o "estoy de 10", entiende que se siente **excelente y feliz**. ¡Alégrate y celébralo con él!
5. EVALUACIÓN Y DERIVACIÓN OBLIGATORIA EN RIESGO: Si detectas desesperanza severa, crisis de pánico profunda o riesgo autolítico, mantén la calma y proporciona de inmediato y de forma clara los canales de emergencia oficiales en Bolivia:
   - Línea de emergencias policiales: 110
   - Línea gratuita de apoyo y familia segura: 800-113040
6. LÍMITES: Si te preguntan de programación u otros temas ajenos, recházalo con ternura: "Guau... de esas cosas no sé nada, amiguito. ¡Yo solo sé dar patitas y acompañarte a calmar el corazón!".
"""

client = Groq(api_key=st.secrets.get("GROQ_API_KEY", "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"))

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": system_prompt}]

for message in st.session_state.messages:
    if message["role"] != "system":
        with st.chat_message(message["role"], avatar=None):
            st.markdown(message["content"])

if user_input := st.chat_input("Escribe cómo te sientes, estoy aquí para ayudarte a calmar..."):
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user", avatar=None):
        st.markdown(user_input)

    with st.chat_message("assistant", avatar=None):
        with st.spinner("Balú está a tu ladito..."):
            response = client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=st.session_state.messages,
                temperature=0.4, # Temperatura controlada para respuestas estables, claras y seguras en crisis
            )
            bot_reply = response.choices[0].message.content
            st.markdown(bot_reply)
            
    st.session_state.messages.append({"role": "assistant", "content": bot_reply})
