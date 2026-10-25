import consumir_gemini
import time
import json
from datetime import datetime
resultados_guardados = [] # Lista para almacenar los resultados de cada intento


# Mis 3 modelos
modelo1 = "gemini-3.1-flash-lite-preview"
modelo2 = "gemini-3.5-flash-lite"
modelo3 = "gemini-3.8-flash"
modelos = [modelo1, modelo2, modelo3]

# Las 2 preguntas que me dijiste
pregunta_simple = "Hazme un menú ficticio de 3 platos. Máximo 15 palabras por plato. Formato: Nombre, ingredientes. Sin explicacion y dime cuál es el plato más recomendado en una frase corta."
pregunta_compleja = "Hazme un menú ficticio de 3 platos. Formato: Nombre, ingredientes (no mas de 8). Luego responde: Soy celíaco, ¿cuál de estos platos del menú NO me recomiendas y cuáles SÍ? Dime unicamente cual es el ingrediente que podria afectarme."

def evaluar_modelo(pregunta, modelos):
    for modelo in modelos:
        print(f"\n{'='*60}")
        print(f"MODELO: {modelo} | PREGUNTA: {pregunta[:50]}...")
        print(f"{'='*60}")
        for i in range(1, 5): # 4 veces cada modelo
            print(f"\n--- Intento {i}/4 con {modelo} ---")
            try:
                # Le pasamos pregunta + modelo
                resultado, latencia, costo = consumir_gemini.obtener_dato_de_prueba(pregunta, modelo, system_instruction="Se breve y conciso", response_schema=None)
                print(resultado)

                #Guardamos los resultados en un json -----------------------------
                resultados_guardados.append({"modelo": modelo, "intento": i, "respuesta": resultado, "latencia": latencia, "costo": costo})

                # Almacenamos la informacion en un json para evaluar nuestros modelos ------------------
                with open("src/resultado_evaluacion_modelos.json", "w", encoding="utf-8") as f:
                    json.dump(resultados_guardados, f, ensure_ascii=False, indent=2)
                    time.sleep(4) # para no saturar la API
        
            except Exception as error:
                print(f"No se pudo completar: {error}")
                resultados_guardados.append({"modelo": modelo, "intento": i, "respuesta": f"ERROR: {error}", "latencia": 0, "costo": 0})
                with open("src/resultado_evaluacion_modelos.json", "w", encoding="utf-8") as f:
                    json.dump(resultados_guardados, f, ensure_ascii=False, indent=2)
                time.sleep(5)
                continue

if __name__ == "__main__":
    print("\n\n### PRUEBA 1: PREGUNTA SENCILLA ###")
    evaluar_modelo(pregunta_simple, modelos)

    print("\n\n### PRUEBA 2: PREGUNTA COMPLEJA CELIACO ###")
    evaluar_modelo(pregunta_compleja, modelos)
    
    print(f"\nSe guardaron {len(resultados_guardados)} respuestas en src/resultado_evaluacion_modelos.json")