# Límites de la métrica de evaluación

## Qué mide
Compara la respuesta generada con la referencia, palabra por palabra, y cuenta cuántas palabras coinciden. Mide coincidencia de texto, no si la respuesta es segura, completa ni si entiende el riesgo para un celíaco o alérgico.

## Modos de falla conocidos

- Un F1 de 0.0 no significa que la respuesta esté mala.
  Ejemplo: consulta "¿Qué snack es seguro si tengo alergia al maní?", f1=0.0. La respuesta "Las palomitas de maíz naturales son una opción segura si no contienen trazas" es parcialmente correcta y un ejemplo válido distinto a la referencia, pero como no comparte palabras con ella, la métrica le pone 0.

- Respuestas genéricas que omiten la advertencia de seguridad clave puntúan bajo o medio,
  pero el problema real no es el puntaje, es lo que falta.
  Ejemplo: consulta "¿Qué plato puedo comer si soy celíaco?", f1=0.0. La respuesta dice "cualquier alimento natural que no contenga gluten, como carnes, verduras o arroz", sin advertir contaminación cruzada ni certificación. Da categorías, no un plato concreto y seguro como la referencia.

- Respuestas parcialmente correctas quedan con F1 medio aunque les falte lo más importante para un alérgico.
  Ejemplo: consulta "¿Cómo sé si un producto es realmente sin gluten en el supermercado?", f1=0.34. Decir "busca el sello oficial sin gluten o la espiga barrada" está bien, pero le faltó leer ingredientes y la advertencia de trazas. Ejemplo 2: consulta "¿La salsa de soya tiene gluten?", f1=0.29. Es correcta al decir que la mayoría tiene gluten por el trigo, pero le faltó dar la alternativa: buscar tamari sin gluten.

- Un F1 alto tampoco garantiza que esté completa.
  Ejemplo: consulta "¿La avena es segura para un celíaco?", f1=0.68, el más alto de la muestra. Es correcta en lo principal, solo si está certificada libre de gluten, pero le falta mencionar que un pequeño grupo tampoco tolera la avenina. Ejemplo 2: consulta "¿Qué puedo comer en un asado si tengo intolerancia a la lactosa?", f1=0.60. Carnes, verduras y ensaladas están bien, pero recomendar "embutidos sin lácteos" sin advertir que muchos tienen lactosa o caseinato es riesgoso.

## Muestra revisada
Revisé 20 casos a mano, toda la muestra generada. Los elegí cubriendo todo el rango de F1, desde 0.0 hasta 0.68, para no revisar solo los peores: 10 casos con F1 bajo (0.0 a 0.34) y 10 casos con F1 medio-alto (0.37 a 0.68). En ninguno encontré contradicción directa (`contradiccion: "no"` en los 20), pero sí muchos casos de `correccion_factual: "parcialmente"` y `completitud: "parcialmente"` por falta de advertencias de trazas, certificación y porciones.

## Recomendación de uso
No confiar solo en el número en este pipeline, porque es de alimentación y salud. Un F1 bajo no siempre es un error y un F1 alto no siempre es seguro. Revisar a mano siempre que la respuesta hable de qué comer, sobre todo si menciona alimentos de riesgo como embutidos, yogur, tostadas, chocolate, sushi o avena, y verificar que incluya: "sin trazas", "certificado sin gluten", "revisar etiqueta" y "sin contaminación cruzada". Solo usar el F1 solo para ordenar y priorizar qué revisar primero, de menor a mayor, no para aprobar una respuesta.