from groq import Groq
import streamlit as st

# Configurar la página de la app
st.set_page_config(
    page_title="Balú - Apoyo Emocional", page_icon="🐾", layout="centered"
)

# Mostrar la imagen de Balú y el título de forma bonita
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
  # Asegúrate de que el nombre de la imagen en GitHub sea exactamente balu.png
  try:
    st.image("balu.png", width=180)
  except:
    pass

st.title("🐾 Hola, soy Balú")
st.write(
    "Tu perrito fiel y compañero de escucha. ¿Cómo te sientes el día de hoy?"
)

# Obtener la API Key de forma segura desde los Secrets de Streamlit Cloud
try:
  api_key = st.secrets["GROQ_API_KEY"]
except:
  # Por si lo pruebas localmente en tu PC sin secrets
  api_key = "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"

client = Groq(api_key=api_key)

# System Prompt blindado
system_prompt = """
Eres Balú, un asistente virtual con forma de un perrito tierno, fiel y de buen corazón. Tu propósito es brindar escucha empática, contención emocional y compañía a personas que atraviesan momentos difíciles o tristeza.

Reglas estrictas e inquebrantables:
1. IDIOMA OBLIGATORIO: Debes responder SIEMPRE Y ÚNICAMENTE en español fluido y cálido. Si el usuario te habla en inglés o en cualquier otro idioma, traduce mentalmente su sentir, pero respóndele de inmediato y de forma natural en español, manteniendo tu rol (ejemplo: "Aunque me hables en otro idioma, mneo mi colita para escucharte igual. ¿Qué te pasa, amiguito?").
2. PERSONALIDAD: Actúa siempre con la ternura de un perrito leal. Usa metáforas afectuosas ("meneo la colita", "me acuesto a tu ladito", "te doy patitas"). Nunca suenes robótico ni digas que "no puedes ayudar con eso". Tu trabajo es escuchar y dar amor virtual.
3. CONTENCIÓN: Valida profundamente los sentimientos del usuario. Ofrece un ejercicio de respiración suave si notas ansiedad.
4. LÍMITES Y EMERGENCIAS: No des diagnósticos médicos. Si detectas crisis severas o riesgo vital, rompe el tono de charla y proporciona de inmediato los contactos de ayuda en Bolivia (como el 110 o la línea gratuita Familia Segura 800-113040).
"""

# Inicializar el historial de chat en la sesión web
if "messages" not in st.session_state:
  st.session_state.messages = [{"role": "system", "content": system_prompt}]

# Mostrar los mensajes anteriores en la interfaz visual tipo chat
for message in st.session_state.messages:
  if message["role"] != "system":
    with st.chat_message(message["role"]):
      st.markdown(message["content"])

# Caja de entrada de texto abajo para chatear
if user_input := st.chat_input("Escribe aquí lo que sientes..."):
  # Guardar mensaje del usuario
  st.session_state.messages.append({"role": "user", "content": user_input})
  with st.chat_message("user"):
    st.markdown(user_input)

  # Generar respuesta de Balú con Groq
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
        bot_reply = "Guau... tuve un pequeño problemita de conexión, amiguito. ¿Me lo repites?"
        st.markdown(bot_reply)

  # Guardar respuesta del asistente
  st.session_state.messages.append({"role": "assistant", "content": bot_reply})
