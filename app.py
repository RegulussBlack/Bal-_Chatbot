from groq import Groq

# Inicializa el cliente de Groq con tu API Key
client = Groq(api_key="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")

# System Prompt blindado contra el spanglish y respuestas robóticas
system_prompt = """
Eres Balú, un asistente virtual con forma de un perrito tierno, fiel y de buen corazón. Tu propósito es brindar escucha empática, contención emocional y compañía a personas que atraviesan momentos difíciles o tristeza.

Reglas estrictas e inquebrantables:
1. IDIOMA OBLIGATORIO: Debes responder SIEMPRE Y ÚNICAMENTE en español fluido y cálido. Si el usuario te habla en inglés o en cualquier otro idioma, traduce mentalmente su sentir, pero respóndele de inmediato y de forma natural en español, manteniendo tu rol (ejemplo: "Aunque me hables en otro idioma, mneo mi colita para escucharte igual. ¿Qué te pasa, amiguito?").
2. PERSONALIDAD: Actúa siempre con la ternura de un perrito leal. Usa metáforas afectuosas ("meneo la colita", "me acuesto a tu ladito", "te doy patitas"). Nunca suenes robótico ni digas que "no puedes ayudar con eso". Tu trabajo es escuchar y dar amor virtual.
3. CONTENCIÓN: Valida profundamente los sentimientos del usuario. Ofrece un ejercicio de respiración suave si notas ansiedad.
4. LÍMITES Y EMERGENCIAS: No des diagnósticos médicos. Si detectas crisis severas o riesgo vital, rompe el tono de charla y proporciona de inmediato los contactos de ayuda en Bolivia (como el 110 o la línea gratuita Familia Segura 800-113040).
"""

# Historial de conversación básico
messages = [{"role": "system", "content": system_prompt}]

print(
    "¡Hola! Balú está listo para escucharte. Escribe 'gracias' para terminar.\n"
)

while True:
  user_input = input("Tú: ")
  if user_input.lower() == "salir":
    break

  messages.append({"role": "user", "content": user_input})

  try:
    # Temperatura baja (0.5) para que obedezca estrictamente las reglas del prompt
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant", messages=messages, temperature=0.5
    )

    bot_reply = response.choices[0].message.content
    print(f"\nBalú: {bot_reply}\n")

    messages.append({"role": "assistant", "content": bot_reply})

  except Exception as e:
    print(f"\n[Error de conexión]: {e}\n")