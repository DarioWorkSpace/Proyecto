from dotenv import load_dotenv
import os
from langchain_google_genai import ChatGoogleGenerativeAI #Crea un modelo de lenguaje de Google Gemini
from langchain_core.prompts import PromptTemplate #la plantilla para el prompt dinámico
from langchain_core.output_parsers import StrOutputParser #Para parsear las respuesas
from langchain_core.runnables import (RunnableBranch, RunnablePassthrough, RunnableLambda) #Bifurcaciones/Branches/Ramificaciones

import logging #Generar un archivo de log con los errores que se presentan

logging.basicConfig(
    level=logging.WARNING,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    filename="error.log",
    filemode="a",
    encoding="utf-8",
    force=True
)
logger = logging.getLogger(__name__)

load_dotenv()

modelo = ChatGoogleGenerativeAI(model="gemini-3.1-flash-lite" )

plantilla_clasificacion = PromptTemplate.from_template(
    "Clasifica el siguiente mensaje de soporte en una sola palabra"
    "Pregunta, queja o sugerencia. Responde con solo esa palabra. \n\n {mensaje}"
)

paso_clasificacion = (
    plantilla_clasificacion
    | modelo
    | StrOutputParser()
    | RunnableLambda(lambda texto: texto.strip().lower()) #Elimina espacios y pasa a minúsculas
)
#Paso Clasificacion Agregado por Seba
def paso_clasificacion(modelo):
    return (
        plantilla_clasificacion
        | modelo
        | StrOutputParser()
        | RunnableLambda(lambda texto: texto.strip().lower())
    )

#Agregado por seba
def construir_cadena_queja_segura(cadena_queja):
	return cadena_queja.with_fallbacks([respuesta_generica])

#Agregado por seba
def construir_cadena_con_enrutamiento(
    paso_clasificacion,
    cadena_queja=None,
    cadena_sugerencia=None,
    cadena_pregunta=None,
):
    cadena_queja = cadena_queja or RunnablePassthrough()
    cadena_sugerencia = cadena_sugerencia or RunnablePassthrough()
    cadena_pregunta = cadena_pregunta or RunnablePassthrough()

    paso_normalizado = paso_clasificacion | RunnableLambda(lambda t: t.strip().lower())

    #Agregado por IA
    # Si lo que me pasan es una cadena real de LangChain, la normalizo con |
    # Si es un Mock del test, lo envuelvo en RunnableLambda para que lance el error
    from langchain_core.runnables import Runnable
    if isinstance(paso_clasificacion, Runnable):
        paso_normalizado = paso_clasificacion | RunnableLambda(lambda t: t.strip().lower() if isinstance(t, str) else t)
    else:
        def clasificar_y_normalizar(x):
            resultado = paso_clasificacion(x)
            if hasattr(resultado, "content"):
                resultado = resultado.content
            return str(resultado).strip().lower()
        paso_normalizado = RunnableLambda(clasificar_y_normalizar)


    bifurcacion = RunnableBranch(
        (lambda x: x["categoria"] == "queja", cadena_queja),
        (lambda x: x["categoria"] == "sugerencia", cadena_sugerencia),
        cadena_pregunta,
    )
    return (
        RunnablePassthrough.assign(categoria=paso_normalizado)
        | bifurcacion
    )

# mensaje_prueba = "Mi plato no llegó a tiempo y estaba frío."
# clasificacion = paso_clasificacion.invoke(
#     {"mensaje": mensaje_prueba}
# )

# print(clasificacion)

cadena_pregunta = (
    PromptTemplate.from_template("Responde esta pregunta técnica con precisión y detalle: \n\n {mensaje}")
    | modelo
    | StrOutputParser()
)

cadena_queja = (
    PromptTemplate.from_template("Responde esta queja con empatía, reconociendo el problema antes de ofrecer una solución: \n\n {mensaje}")
    | modelo
    | StrOutputParser()
)

cadena_sugerencia = (
    PromptTemplate.from_template("Agradece esta sugerencia y explica cómo se evaluará dentro del producto: \n\n {mensaje}")
    | modelo
    | StrOutputParser()
)

# caminos = RunnableBranch(
#     (condicion_1, rama_1), #if
#     (condicion_2, rama_2), #elif
#     (condicion_3, rama_3), #elif
#     rama_por_defecto #else
# )
#Cada condición debe ser una función lambda

#x = {"clasificacion": "queja" , "mensaje" : "Mi plato no llegó a tiempo y estaba frío."}
bifurcacion = RunnableBranch(
    (lambda x: x["clasificacion"] == "queja", cadena_queja),
    (lambda x: x["clasificacion"] == "sugerencia", cadena_sugerencia),
    cadena_pregunta #Por defecto, si no es queja ni sugerencia, se asume que es pregunta
)

#Fallback: cadena de respaldo. Captura las caídas de mi LLM (RateLimite, 401, APIConectionError, respuestas vacias))
def fallback_con_log(x):
    logger.warning("Cadena principal falló. Activando respuesta genérica")
    return "Gracias por tu mensaje. Un miembro de nuestro equipo te va a responder pronto."

respuesta_generica = RunnableLambda(
    fallback_con_log
)

cadena_con_enrutamiento = (
    RunnablePassthrough.assign(clasificacion=paso_clasificacion)
    | bifurcacion
)

cadena_robusta = cadena_con_enrutamiento.with_fallbacks([respuesta_generica], exception_key="error")

def procesar_mensaje_seguro(cadena, mensaje):
    try:
        return cadena.invoke({"mensaje": mensaje})
    except Exception as error:
        logger.error("Error procesando mensaje:%s", error)
        return "No pudimos procesar tu mensaje en este momento. Por favor, intenta de nuevo más tarde."

if __name__ == "__main__":
    mensaje = "Soy alérgico a los frutos secos."
    respuesta = procesar_mensaje_seguro(cadena_robusta, mensaje)
    print(respuesta)

# print(resultado)

#Entrada inicial: {"mensaje": "Mi plato no llegó a tiempo y estaba frío."}
#                   |
#                   v
#RunnablePassthrough
#   1: Pasa el mensaje a paso_clasificacion -> Return "queja"
#   2: Fusiono clasificacion y mensaje
#   3: Return {"mensaje": "Mi plato no llegó a tiempo y estaba frío.", "clasificacion": "queja"}
#                   |
#                   v
# bifurcacion (RunnableBranch)
#   ¿clasificacion == "queja"? -> True
#   Pasa el mensaje a cadena_queja
#   cadena_queja.invoke({"mensaje": "Mi plato no llegó a tiempo y estaba frío.", "clasificacion": "queja"})
#   Return respuesta final generada