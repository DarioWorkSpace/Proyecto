import os
import requests
from dotenv import load_dotenv

import time

load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")
MODELO = "gemini-3.6-flash"
URL_BASE = "https://generativelanguage.googleapis.com/v1beta/models/"

#Funcion para crear la solicitud
def armar_solicitud(pregunta):
    if not pregunta:
        raise ValueError("La pregunta no puede estar vacía")
    url = f"{URL_BASE}{MODELO}:generateContent?key={API_KEY}"
    body = {
        "contents":
        [{"parts": [{"text": pregunta}]}]
    }
    return url, body

#Funcion para envíar la petición
def enviar_peticion(url, body):
    try:
        respuesta = requests.post(url, json=body, timeout=30)
    except requests.exceptions.ConnectionError:
        raise RuntimeError("No se pudo conectar con el servicio. Intenta de nuevo en unos segundos.")

    if respuesta.status_code != 200:
            raise RuntimeError(f"Error en la petición.Status Code: {respuesta.status_code}") 
    
    try:
        return respuesta.json()
    except requests.exceptions.JSONDecodeError:
     	raise RuntimeError("La respuesta del servicio no llegó en el formato esperado.")
       

#Funcion procesa y extrae dato
def extraer_texto(datos):
    try:
        return datos["candidates"][0]["content"]["parts"][0]["text"]
    except (KeyError, IndexError):
     	raise RuntimeError("La respuesta no trae el texto generado en el lugar esperado.")

def obtener_dato_de_prueba(pregunta):
    url, body = armar_solicitud(pregunta)
    inicio = time.perf_counter() #Empezar contador
    datos = enviar_peticion(url, body)
    fin = time.perf_counter() #Detener contador
    latencia = fin - inicio
    print(f"Latencia: {latencia:.2f} segundos") #.2f para mostrar solo 2 decimales
    costo = calcular_costo(datos, 0.00000075, 0.00000375)
    print(f"Costo estimado de la operación: ${costo:.6f} USD")
    return extraer_texto(datos)

def calcular_costo(datos, precio_entrada, precio_salida):
    uso = datos["usageMetadata"]
    tokens_entrada = uso["promptTokenCount"]
    tokens_salida = uso["candidatesTokenCount"]
    tokens_razonamiento = uso.get("thoughtsTokenCount", 0)
    costo = (
        tokens_entrada * precio_entrada
        + (tokens_salida + tokens_razonamiento) * precio_salida
    )
    return costo

try:
     resultado = obtener_dato_de_prueba("Confirma en una frase corta que esta conexión  funciona")
     print(resultado)
except (ValueError, RuntimeError) as error:
     print("No se pudo completar la operación:", error)


