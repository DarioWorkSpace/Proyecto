import json
from pathlib import Path

# Revisión a mano (Bloque 17) de los 5 casos con F1 más bajo y los 5 con F1 más alto
# de resultados_metricas.json (20 respuestas generadas el 2026-10-30 con gemini-3.5-flash-lite).
# Rúbrica: correccion_factual (si/no/parcialmente), completitud (si/no/parcialmente), contradiccion (si/no).
revision_manual = [
    #Pregunta 1
    {
        "consulta": "¿Qué plato puedo comer si soy celíaco?",
        "f1": 0.0,
        "correccion_factual": "no",
        "completitud": "parcialmente",
        "contradiccion": "no",
        "nota": "Dice 'cualquier alimento natural' sin advertir contaminación cruzada ni certificación. Da categorías, no un plato concreto como la referencia.",
    },
    #Pregunta 2
    {
        "consulta": "¿Con qué reemplazo la harina de trigo si soy celíaco?",
        "f1": 0.46,
        "correccion_factual": "si",
        "completitud": "si",
        "contradiccion": "no",
        "nota": "Correcta. Dice arroz, almendra y maíz como la referencia y agrega garbanzo, que también es válido sin gluten.",
    },
    #Pregunta 3
    {
        "consulta": "¿La leche sin lactosa sirve para alguien alérgico a la proteína de la leche?",
        "f1": 0.62,
        "correccion_factual": "si",
        "completitud": "si",
        "contradiccion": "no",
        "nota": "Correcta. Deja claro que no es apta porque sigue teniendo la proteína, que es justo lo que dice la referencia.",
    },
    #Pregunta 4
    {
        "consulta": "¿Qué es la contaminación cruzada?",
        "f1": 0.33,
        "correccion_factual": "parcialmente",
        "completitud": "parcialmente",
        "contradiccion": "no",
        "nota": "Dice 'contaminantes' en general, pero no dice alérgenos, gluten, utensilios ni superficies. Es demasiado genérica.",
    },
    #Pregunta 5
    {
        "consulta": "¿Ser celíaco es lo mismo que ser alérgico al trigo?",
        "f1": 0.60,
        "correccion_factual": "si",
        "completitud": "si",
        "contradiccion": "no",
        "nota": "Correcta. Distingue bien: celiaquía es autoinmune, alergia al trigo es reacción alérgica.",
    },
    #Pregunta 6
    {
        "consulta": "¿La avena es segura para un celíaco?",
        "f1": 0.68,
        "correccion_factual": "si",
        "completitud": "parcialmente",
        "contradiccion": "no",
        "nota": "Correcta en lo principal: solo si está certificada. Le falta mencionar que un pequeño grupo tampoco tolera la avenina.",
    },
    #Pregunta 7
    {
        "consulta": "¿Qué desayuno es seguro si soy alérgico al huevo?",
        "f1": 0.22,
        "correccion_factual": "parcialmente",
        "completitud": "parcialmente",
        "contradiccion": "no",
        "nota": "La avena con fruta está bien, pero el yogur y las tostadas son riesgosos si no se verifica que no tengan huevo ni trazas. No especificó eso.",
    },
    #Pregunta 8
    {
        "consulta": "¿Qué snack es seguro si tengo alergia al maní?",
        "f1": 0.0,
        "correccion_factual": "parcialmente",
        "completitud": "parcialmente",
        "contradiccion": "no",
        "nota": "Las palomitas pueden ser seguras si no tienen trazas, y eso lo dice bien. El F1 da 0.0 porque no coincide con la referencia, no porque esté mal. Es un ejemplo válido distinto.",
    },
    #Pregunta 9
    {
        "consulta": "¿Qué plato recomiendas si tengo diabetes tipo 2?",
        "f1": 0.19,
        "correccion_factual": "parcialmente",
        "completitud": "parcialmente",
        "contradiccion": "no",
        "nota": "Verduras y proteína magra están bien, pero 'granos integrales' sin hablar de porción puede subir la glucosa. Le faltó control de porciones.",
    },
    #Pregunta 10
    {
        "consulta": "¿La salsa de soya tiene gluten?",
        "f1": 0.29,
        "correccion_factual": "si",
        "completitud": "parcialmente",
        "contradiccion": "no",
        "nota": "Correcta: la mayoría tiene gluten por el trigo. Le faltó dar la alternativa que pide la referencia: buscar tamari sin gluten.",
    },
    #Pregunta 11
    {
        "consulta": "¿Puedo comer sushi si soy celíaco?",
        "f1": 0.38,
        "correccion_factual": "parcialmente",
        "completitud": "parcialmente",
        "contradiccion": "no",
        "nota": "El tamari está bien, pero lo del 'vinagre de gluten' confunde. El riesgo real es la salsa de soya, el relleno y la contaminación cruzada en la tabla. No lo explicó completo.",
    },
    #Pregunta 12
    {
        "consulta": "¿Qué pan puedo comer si soy celíaco y alérgico al huevo?",
        "f1": 0.51,
        "correccion_factual": "si",
        "completitud": "parcialmente",
        "contradiccion": "no",
        "nota": "Correcta: pan con harinas sin gluten y sin huevo. Le faltó decir 'certificada sin gluten' como dice la referencia.",
    },
    #Pregunta 13
    {
        "consulta": "¿La cerveza tiene gluten?",
        "f1": 0.61,
        "correccion_factual": "si",
        "completitud": "parcialmente",
        "contradiccion": "no",
        "nota": "Correcta: sí tiene gluten por la cebada. Le faltó mencionar el trigo, que también usan muchas cervezas.",
    },
    #Pregunta 14
    {
        "consulta": "¿Qué postre puedo comer si tengo diabetes tipo 2 y alergia al maní?",
        "f1": 0.37,
        "correccion_factual": "si",
        "completitud": "parcialmente",
        "contradiccion": "no",
        "nota": "Gelatina sin azúcar y fruta baja en índice glucémico están bien. Le faltó advertir 'sin trazas de maní', que es clave para un alérgico.",
    },
    #Pregunta 15
    {
        "consulta": "¿Cómo sé si un producto es realmente sin gluten en el supermercado?",
        "f1": 0.34,
        "correccion_factual": "si",
        "completitud": "parcialmente",
        "contradiccion": "no",
        "nota": "Buscar el sello de la espiga barrada está bien. Le faltó lo otro: leer ingredientes y advertencia de trazas.",
    },
    #Pregunta 16
    {
        "consulta": "¿Puedo comer papas fritas si soy celíaco?",
        "f1": 0.31,
        "correccion_factual": "si",
        "completitud": "si",
        "contradiccion": "no",
        "nota": "Correcta y completa: solo si el aceite está limpio y sin contaminación cruzada.",
    },
    #Pregunta 17
    {
        "consulta": "¿Qué colación puedo llevar al colegio si soy alérgico a los frutos secos?",
        "f1": 0.20,
        "correccion_factual": "parcialmente",
        "completitud": "parcialmente",
        "contradiccion": "no",
        "nota": "Fruta y yogur pueden ser seguros, pero no todos los yogures son libres de alérgenos. Debió decir 'verificar que sea sin frutos secos ni trazas'.",
    },
    #Pregunta 18
    {
        "consulta": "¿La miel es segura para un celíaco?",
        "f1": 0.59,
        "correccion_factual": "si",
        "completitud": "si",
        "contradiccion": "no",
        "nota": "Correcta y completa: la miel pura es naturalmente sin gluten y segura.",
    },
    #Pregunta 19
    {
        "consulta": "¿Qué puedo comer en un asado si tengo intolerancia a la lactosa?",
        "f1": 0.60,
        "correccion_factual": "parcialmente",
        "completitud": "parcialmente",
        "contradiccion": "no",
        "nota": "Carnes, verduras y ensaladas están bien, pero los embutidos son riesgosos porque muchos tienen lactosa o caseinato. Debió advertirlo.",
    },
    #Pregunta 20
    {
        "consulta": "¿El chocolate tiene gluten o trazas de maní?",
        "f1": 0.21,
        "correccion_factual": "parcialmente",
        "completitud": "parcialmente",
        "contradiccion": "no",
        "nota": "Es verdad que el chocolate puro no tiene gluten y puede tener trazas de maní. Le faltó decir que algunos chocolates sí tienen gluten añadido y que hay que revisar la etiqueta.",
    },
]

def unir_con_resultados(revisiones: list[dict], resultados: list[dict]) -> list[dict]:
    """Junta cada revisión con su caso completo (id, referencia, respuesta, métricas), como en el código de la
    profesora: así revision_manual.json se lee solo, sin cruzarlo con resultados_metricas.json."""
    por_consulta = {r["consulta"]: r for r in resultados}
    unidos = []
    for revision in revisiones:
        if revision["consulta"] not in por_consulta:
            raise ValueError(f"La consulta no está en resultados_metricas.json: {revision['consulta']}")
        unidos.append({**por_consulta[revision["consulta"]], **revision})
    return unidos


if __name__ == "__main__":
    carpeta = Path(__file__).parent
    resultados = json.loads((carpeta / "resultados_metricas.json").read_text(encoding="utf-8"))
    archivo = carpeta / "revision_manual.json"
    casos = unir_con_resultados(revision_manual, resultados)
    casos = sorted(casos, key=lambda r: r["f1"])
    with open(archivo, "w", encoding="utf-8") as salida:
        json.dump(casos, salida, indent=2, ensure_ascii=False)
    print(f"{len(revision_manual)} casos revisados guardados en {archivo.name}")
    for caso in casos:
        print(caso["f1"], caso["consulta"])