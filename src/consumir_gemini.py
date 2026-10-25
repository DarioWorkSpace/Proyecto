import os
import requests
from google import genai
from dotenv import load_dotenv
import json
import re
import time
#system_instruction = "Eres un asistente útil y creativo. Responde de manera concisa y clara."
pregunta=""

load_dotenv()

#Constantes
API_KEY = os.getenv("GEMINI_API_KEY")
#MODELO = "gemini-3.6-flash"
URL_BASE = "https://generativelanguage.googleapis.com/v1beta/models/"

#Funcion para crear la solicitud
def armar_solicitud(pregunta, modelo ,system_instruction ,response_schema=None):
    if not pregunta:
        raise ValueError("La pregunta no puede estar vacía")
    url = f"{URL_BASE}{modelo}:generateContent?key={API_KEY}"

    body = {
        "system_instruction": {"text": system_instruction},
        "contents":
        [{"parts": [{"text": pregunta}]}]
    }

    if system_instruction:
        body["system_instruction"] = {
            "parts": [
                {"text": system_instruction}
            ]
        }

    if response_schema is not None:
        body["generationConfig"] = {
            "responseMimeType": "application/json",
            "responseSchema": response_schema

        }
    return url, body

#Funcion para envíar la petición
def enviar_peticion(url, body):
    try:
        respuesta = requests.post(url, json=body, timeout=30)
    except requests.exceptions.ConnectionError:
        raise RuntimeError("No se pudo conectar con el servicio. Intenta de nuevo en unos segundos.")

    if respuesta.status_code in(401, 403):
        raise ValueError(f"Credencial inválida o sin permiso. Revisa tu GEMINI_API_KEY")
    if respuesta.status_code >= 500:
        raise TimeoutError(f"El proveedor no pudo procesar la petición, Hay que esperar y reintentar")
    if respuesta.status_code == 429:
        segundos = respuesta.headers.get("Retry-After")
        mensaje = f"Límite excedido. Reintentar en {segundos}s." if segundos else "Límite excedido."
        raise TimeoutError(mensaje)

    
    if respuesta.status_code != 200:
        raise RuntimeError(f"Error en la petición. Status Code: {respuesta.status_code}: {respuesta.text}")
    
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

def obtener_dato_de_prueba(pregunta,modelo,system_instruction="", response_schema=None):

    response_schema = {
        "type": "object",
        "properties": {
            "platos": {"type": "array", "items": {"type": "string"}},
            "recomendado": {"type": "string"}
        },
        "required": ["platos", "recomendado"]
    }

    url, body = armar_solicitud(pregunta, modelo, system_instruction, response_schema)
    inicio = time.perf_counter() #Empezar contador
    datos = enviar_peticion(url, body)
    fin = time.perf_counter() #Detener contador
    latencia = fin - inicio

    print(f"Latencia: {latencia:.2f} segundos") #.2f para mostrar solo 2 decimales
    costo = calcular_costo(datos, 0.00000075, 0.00000375)
    print(f"Costo estimado de la operación: ${costo:.6f} USD")
    return extraer_texto(datos), latencia, costo

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

def parsear_respuesta_json(texto, claves_requeridas=None):
    """
    claves_requeridas = ["categoria", "nivel"]
    """
    texto_limpio = texto.strip()
    texto_limpio = re.sub(r"^```(?:json)?\s*", "", texto_limpio)
    texto_limpio = re.sub(r"\s*```$", "", texto_limpio)
    try:
        datos = json.loads(texto_limpio)
    except json.JSONDecodeError:
        raise ValueError("La respuesta del modelo no es JSON válido")

    if claves_requeridas:
        faltantes = [clave for clave in claves_requeridas if clave not in datos]
        if faltantes:
            raise ValueError("La respuesta no tiene la estructura esperada.")
    return datos



#if __name__ == "__main__":
