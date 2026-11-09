from collections import Counter
from pipeline_limpieza import procesar_texto
from cliente import consultar_modelo
import json
import cliente
from pathlib import Path

def contar_coincidencias(
    tokens_referencia: list[str],
    tokens_respuesta: list[str],
) -> int:
    """Cuenta las coincidencias entre referencia y respuesta."""
    conteo_referencia = Counter(tokens_referencia)
    conteo_respuesta = Counter(tokens_respuesta)
    interseccion = conteo_referencia & conteo_respuesta
    return sum(interseccion.values())

def calcular_precision_cobertura_f1(
    tokens_referencia: list[str],
    tokens_respuesta: list[str],
) -> dict[str, float]:
    """Calcula precisión, cobertura y F1 de dos listas de tokens."""
    coincidencias = contar_coincidencias(
        tokens_referencia, tokens_respuesta
    )

    if not tokens_respuesta or not tokens_referencia:
        return {"precision": 0.0, "cobertura": 0.0, "f1": 0.0}

    precision = coincidencias / len(tokens_respuesta)
    cobertura = coincidencias / len(tokens_referencia)

    if precision + cobertura == 0:
        f1 = 0.0
    else:
        f1 = 2 * precision * cobertura / (precision + cobertura)

    resultado = {
        "precision": precision,
        "cobertura": cobertura,
        "f1": f1,
    }

    return resultado

#---------------------------------------------------------------------

def calcular_metricas(texto_referencia, texto_respuesta):

    tokens_referencia = procesar_texto(texto_referencia)

    tokens_respuesta = procesar_texto(texto_respuesta)

    return calcular_precision_cobertura_f1(
        tokens_referencia, tokens_respuesta
    )

casos = [
    #Pregunta 1
    (
        "¿Qué plato puedo comer si soy celíaco?",
        "Un plato seguro para celíacos es la ensalada de quinoa con vegetales.",
    ),
    #Pregunta 2
    (
        "¿Con qué reemplazo la harina de trigo si soy celíaco?",
        "Puedes reemplazar la harina de trigo con harina de arroz, almendra o maíz.",
    ),
    #Pregunta 3
    (
        "¿La leche sin lactosa sirve para alguien alérgico a la proteína de la leche?",
        "No, la leche sin lactosa aún contiene proteínas de la leche y no es segura para alérgicos.",
    ),
    #Pregunta 4
    (
        "¿Qué es la contaminación cruzada?",
        "La contaminación cruzada es la transferencia de alérgenos entre alimentos.",
    ),
    #Pregunta 5
    (
        "¿Ser celíaco es lo mismo que ser alérgico al trigo?",
        "No, ser celíaco es una enfermedad autoinmune, mientras que la alergia al trigo es una reacción alérgica.",
    ),
    #Pregunta 6
    (
        "¿La avena es segura para un celíaco?",
        "No, solo es segura si no contiene gluten y está certificada como libre de gluten.",
    ),
    #Pregunta 7
    (
        "¿Qué desayuno es seguro si soy alérgico al huevo?",
        "Un desayuno seguro para alérgicos al huevo puede incluir avena con frutas y leche vegetal.",
    ),
    #Pregunta 8
    (
        "¿Qué snack es seguro si tengo alergia al maní?",
        "Un snack seguro para alérgicos al maní puede ser frutas, vegetales o nueces sin maní.",
    ),
    #Pregunta 9
    (
        "¿Qué plato recomiendas si tengo diabetes tipo 2?",
        "Un plato recomendado para personas con diabetes tipo 2 es una ensalada de verduras con proteína magra.",
    ),
    #Pregunta 10
    (
        "¿La salsa de soya tiene gluten?",
        "Sí, la salsa de soya tradicional contiene gluten, pero existen versiones sin gluten disponibles.",
    ),
    # Pregunta 11
    (
        "¿Puedo comer sushi si soy celíaco?",
        "Sí, puedes comer sushi si el arroz, la salsa de soya y el relleno son sin gluten y no hay contaminación cruzada.",
    ),
    # Pregunta 12
    (
        "¿Qué pan puedo comer si soy celíaco y alérgico al huevo?",
        "Puedes comer pan sin gluten y sin huevo, hecho con harina de arroz o maíz certificada sin gluten.",
    ),
    # Pregunta 13
    (
        "¿La cerveza tiene gluten?",
        "Sí, la cerveza común tiene gluten porque se hace con cebada o trigo.",
    ),
    # Pregunta 14
    (
        "¿Qué postre puedo comer si tengo diabetes tipo 2 y alergia al maní?",
        "Puedes comer fruta fresca o gelatina sin azúcar, sin maní y sin trazas de maní.",
    ),
    # Pregunta 15
    (
        "¿Cómo sé si un producto es realmente sin gluten en el supermercado?",
        "Debes revisar que el envase diga sin gluten y leer la lista de ingredientes y la advertencia de trazas.",
    ),
    # Pregunta 16
    (
        "¿Puedo comer papas fritas si soy celíaco?",
        "Sí, solo si las papas se fríen en aceite limpio que no se haya usado para alimentos con gluten.",
    ),
    # Pregunta 17
    (
        "¿Qué colación puedo llevar al colegio si soy alérgico a los frutos secos?",
        "Puedes llevar fruta, yogur sin frutos secos o sándwich con ingredientes sin frutos secos ni trazas.",
    ),
    # Pregunta 18
    (
        "¿La miel es segura para un celíaco?",
        "Sí, la miel pura es segura para un celíaco porque no tiene gluten.",
    ),
    # Pregunta 19
    (
        "¿Qué puedo comer en un asado si tengo intolerancia a la lactosa?",
        "Puedes comer carne a la parrilla, verduras asadas y ensaladas sin queso ni salsas con lactosa.",
    ),
    # Pregunta 20
    (
        "¿El chocolate tiene gluten o trazas de maní?",
        "Algunos chocolates tienen gluten o trazas de maní, debes revisar la etiqueta y buscar uno sin gluten y sin trazas de maní.",
    ),

]

resultados = []

for consulta, referencia in casos:

    respuesta = consultar_modelo(consulta, system_instruction="Responde en español con una definición breve, en una sola oración de máximo 15 palabras. Sin listas, ejemplos ni introducciones.")

    metricas = calcular_metricas(referencia, respuesta)

    print("Consulta:", consulta)
    print("Referencia:", referencia)
    print("Respuesta:", respuesta)
    print("Métricas:", metricas)
    print("\n")
    
    resultados.append({
        "consulta": consulta,
        "respuesta": respuesta,
        **metricas,
    })

resultados = sorted(resultados, key=lambda r: r["f1"])

ruta = Path(__file__).parent / "resultados_metricas.json"
with open(ruta, "w", encoding="utf-8") as archivo:

    json.dump(resultados, archivo, indent=2, ensure_ascii=False)

def resumir_metricas(resultados):

    if not resultados:
        return {
            "precision_promedio": 0,
            "cobertura_promedio": 0,
            "f1_promedio": 0,
        }

    n = len(resultados)

    return {
        "precision_promedio": sum(
            r["precision"] for r in resultados
        ) / n,

        "cobertura_promedio": sum(
            r["cobertura"] for r in resultados
        ) / n,

        "f1_promedio": sum(r["f1"] for r in resultados) / n,
    }
print("Promedios")
print(resumir_metricas(resultados))

peores_casos = sorted(resultados, key=lambda r: r["f1"])

for caso in peores_casos[:3]:

    print(caso["consulta"], caso["f1"])


#Descomentar ctrl +k crtl + u
# referencia = procesar_texto(
#     "Python es un lenguaje de programación interpretado."
# )

# texto_respuesta = consultar_modelo("¿Qué es Python?",
#                                    system_instruction="Responde en español con una definición breve, en una sola oración de máximo 15 palabras. Sin listas, ejemplos ni introducciones.")

# respuesta = procesar_texto(texto_respuesta)
# resultado = calcular_precision_cobertura_f1(referencia, respuesta)

# print("Respuesta:", texto_respuesta)
# print("Tokens de referencia:", len(referencia))
# print("Tokens de respuesta:", len(respuesta))
# print(resultado)
