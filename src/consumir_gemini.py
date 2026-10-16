import os
import requests
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")
MODELO = "gemini-3.6-flash"
URL_BASE = "https://generativelanguage.googleapis.com/v1beta/models/"

#Funcion para crear la solicitud
def crear_solicitud(pregunta):
    url = f"{URL_BASE}{MODELO}:generateContent?key={API_KEY}"
    body = {
        "contents":
        [{"parts": [{"text": pregunta}]}]
    }
    return url, body

#Funcion para envíar la petición
def enviar_peticion(url, body):
    respuesta = requests.post(url, json=body)
    return respuesta.json()

#Funcion procesa y extrae dato
def extraer_texto(datos):
    return datos["candidates"][0]["content"]["parts"][0]["text"]

def obtener_dato_de_prueba(pregunta):
    url, body = crear_solicitud(pregunta)
    datos = enviar_peticion(url, body)
    return extraer_texto(datos)

print(obtener_dato_de_prueba("Confirma en una frase corta que esta conexión  funciona"))