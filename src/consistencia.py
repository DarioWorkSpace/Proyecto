import json
import time
from banco.py import BANCO_DE_PROMPT
from consumir_gemini import armar_solicitud, enviar_peticion, extraer_texto, parsear_respuesta_json

registro = {}

try:
    for prompt in BANCO_DE_PROMPT:
        exitos = 0
        intentos = 3
        for inteto in range (intentos):
            url, body = armar_solicitud( prompt["ejemplo_usuario"], "gemini-3.1-flash-lite", prompt["system_instruction"], prompt["response_schema"] )
            respuesta = enviar_peticion(url, body)
            texto = extraer_texto(respuesta)
            try:
                datos = parsear_respuesta_json(texto, prompt["claves_esperadas"])
                exitos+= 1
                print(f"Respuesta: {datos}")
            except ValueError as error:
                print(f"Intento {intentos+1} fallo: {error}")
            time.sleep(4) # para no saturar la API
        print(f"{prompt['nombre']}: {exitos}/{intentos} respuestas válidas")
        registro[prompt["nombre"]] = {"exitos": exitos, "intentos": intentos}

    #Cuando termine de recorrer los prompts quiero guardar esa info en registro_resultados.json
    with open("src/registro_resultados.json", "w", encoding="utf-8") as archivo:
        json.dump(registro, archivo, indent=2, ensure_ascii=False)

except (ValueError, RuntimeError) as error:
    print("No se pudo completar la operación:", error)