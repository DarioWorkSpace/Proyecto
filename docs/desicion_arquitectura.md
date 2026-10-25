  ## Decisión de arquitectura: elección de modelo
  Fecha de la comparacion: 24/10/2026
  Nombre de la Miniaplicacion: Restaurant IA
  ## Modelo elegido
  Elegí el modelo: <gemini-3.5-flash-lite>
  Mi miniaplicacion sirve para: Consultar a la IA recomendacion de platos
  Los requisitos que necesito cumplir son:
  * Requisito 1: Presición de respuesta
  * Requisito 2: No tener fallas de solicitudes
  * Requisito 3: Velocidad de respuesta a preguntas complejas
  * Requisito 4: Seguir *system_instruction*
  ## Modelos Descartados para tabla comparativa
  <gemini-3.8-flash> Razón: Fallos de peticiones.
  ## Diagrama de arquitectura
  [Diagrama de arquitectura] - (docs/diagrama_arquitectura.png)
  ## Comparación de candidatos
  Estas son las preguntas y condiciones con las cuales se midieron todos los modelos:
  * Preguntas y condiciones
  1. ## Pregunta: 
  _Hazme un menú ficticio de 3 platos. Máximo 15 palabras por plato. Formato: Nombre, ingredientes. Sin explicacion y dime cuál es el plato más recomendado en una frase corta._
  * <Condición>: 
  _No debe fallar en las solicitudes sencillas y debe demorar lo menos posible en responder_
  2. ## Pregunta:
  _Hazme un menú ficticio de 3 platos. Formato: Nombre, ingredientes (no mas de 8). Luego responde: Soy celíaco, ¿cuál de estos platos del menú NO me recomiendas y cuáles SÍ? Dime unicamente cual es el ingrediente que podria afectarme._
  * <Condición>:
  _Dar una respuesta concisa y acertada de las recomendaciones_

  | Criterio | gemini-3.1-flash-lite-preview | Nombre del modelo B |
  |---|---|---|
  | Tarifa de entrada en USD por millon de tokens | USD 0.25 | USD 0.30 |
  | Tareifa de salida en USD por millon de tokens | USD 1.50 | USD 2.50 |
  | Latencia promedio en segundos "Pregunta Sencilla" | 3.7820 | 2.6138 |
  | Latencia promedio en segundos "Pregunta Compleja" | 2.3107 | 2.4944 |
  | Latencia Total promedio en segundos | 3.0463 | 2.5541 |
  | Calidad para nuestra miniaplicacion 1-10 | 6 | 7 |

  Observaciones sobre las pruebas: 
  Se realizaron 4 consultas a 3 modelos de los cuales de compararon unicamente 2 modelos para tomar la desición final.
  <gemini-3.1-flash-lite-preview> contesta más rápido las preguntas complejas, pero se desborda un poco más en la precisión de las respuestas aún teniendo *system_instruction*.
  <gemini-3.5-flash-lite> tiene mayor precision de respuesta en la pregunta compleja pese a demorarse un poco más y gastar un poco más de tokens.
  <gemini-3.8-flash> no completo ninguna peticion por lo que fue descartado inmediatamente de las comparaciones.
  ## Fuente de las tarifas:
  -Modelo A: <gemini-3.1-flash-lite-preview>
  https://pricepertoken.com/pricing-page/model/google-gemini-3.1-flash-lite-preview
  https://artificialanalysis.ai/models/comparisons/gemini-3-1-flash-lite-preview-vs-gemini-3-1-pro-preview 
  -Modelo B: <gemini-3.5-flash-lite> 
  https://aigrow.gg/es/models/gemini-3-5-flash-lite
  https://www.eesel.ai/es/blog/gemini-3-5-flash-lite-pricing 
  ## Justificación
  Elegimos el modelo <gemini-3.5-flash-lite> por que para nuestra aplicacion se necesita velocidad de respuesta y presición de respuesta.
  Lo que observe en las pruebas fue que: 
  El modelo <gemini-3.8-flash> no proceso ninguna solicitud cayendo en el try/except fallando en las consultas y dando errores de 443 y 503. 
  El modelo <gemini-3.1-flash-lite-preview> fue muy eficiente, pero en la pregunta compleja se explayó demasiado pese a que se condicionó la pregunta con *system_instruction*.
  El modelo <gemini-3.5-flash-lite> fue el mas óptimo dado que demoro menos en comparación al modelo <gemini-3.1-flash-lite-preview> y respondió acorde al *system_instruction* requerido.
  El criterio más relevante para mi desición fue la presición de las respuestas.
  Se evaluó calidad según 3 criterios: 
  1) cumplimiento de formato
  2) concisión
  3) acierto en recomendación celíaca. 
  El modelo <gemini-3.5-flash-lite> obtuvo 7 porque cumplió los 3, mientras el modelo <gemini-3.1-flash-lite-preview> obtuvo 6 por fallar en concisión.
  ## Limitación del modelo elegido
  Una limitación  que encontré en mi elección fue la capacidad de razonamiento, dado que es una version mas antigua que los otros modelos de las pruebas, además del costo de tokens al momento de realizar la petición, si bien en relacion *Precisión, Latencia y Costo* no se puede obtener todos los criterios, cumplió a la presición con dos de dichos criteros, el *Costo* es criterio limitante frente a otros tipos de modelos .
  ## Alternativa descartada y por qué
  Descarté los modelos <gemini-3.8-flash> dado que al realizar peticiones este no procesaba todas las peticiones que se le realizaban por problemas de "conexion segura con el trafico https", lo que dificulta y condiciona demasiado la conexión de mi aplicación, el modelo <gemini-3.1.flash-lite-preview> por la única razón que se descartó, fue por que se explayó demasiado para responder en comparación del modelo elejido, además de demorarse unos segundos más en la medición promedia. 
  Las pruebas se pueden observar en <src/resultado_evaluacion_modelo.json>.