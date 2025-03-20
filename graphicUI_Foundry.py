import streamlit as st
import urllib.request
import json
import requests
import ssl
import os

def allowSelfSignedHttps(allowed):
    if allowed and not os.environ.get('PYTHONHTTPSVERIFY', '') and getattr(ssl, '_create_unverified_context', None):
        ssl._create_default_https_context = ssl._create_unverified_context

allowSelfSignedHttps(True)

API_URL = "https://jaimevadell-0624-axuek.eastus2.inference.ml.azure.com/score"
API_KEY = "EEjHVYb7tNPNtE9iHYs0wpZUEzgThD3wxhcjenMsAFbmugBTbqrIJQQJ99BCAAAAAAAAAAAAINFRAZML4FGS"

st.title("Chat con AI Foundry")

# Inicializa historial en la sesion
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Mostrar historial previo
for i, msg in enumerate(st.session_state.chat_history):
    role = "assistant" if i % 2 == 1 else "user"
    with st.chat_message(role):
        st.write(msg)

# Entrada del usuario
user_input = st.chat_input("Escribe tu mensaje...")
if user_input:
    # Guardamos el mensaje del usuario
    st.session_state.chat_history.append(user_input)
    with st.chat_message("user"):
        st.write(user_input)
    # Cuerpo de la petición SIN 'inputs'

    data = {
        "chat_history": [],
        "question": user_input
    }
    body = str.encode(json.dumps(data))
    headers = {'Content-Type':'application/json', 'Accept': 'application/json', 'Authorization':('Bearer '+ API_KEY)}
    req = urllib.request.Request(API_URL, body, headers)
    # Llamada a la API
    try:
        response = urllib.request.urlopen(req)

        result = response.read().decode("utf-8")  # 🔹 Convertir la respuesta en string
        try:
            result_json = json.loads(result)  # Convertimos a JSON
            answer = result_json.get("answer", "⚠️ No se encontró respuesta en el JSON")  # Extraer "answer"
        except json.JSONDecodeError:
            answer = "⚠️ Error al procesar la respuesta del servidor"

        st.session_state.chat_history.append(answer)  # Guardar solo la respuesta, no el JSON completo

        with st.chat_message("assistant"):
            st.write(answer)
    except urllib.error.HTTPError as error:
        print("The request failed with status code: " + str(error.code))

        # Print the headers - they include the requert ID and the timestamp, which are useful for debugging the failure
        print(error.info())
        print(error.read().decode("utf8", 'ignore'))
