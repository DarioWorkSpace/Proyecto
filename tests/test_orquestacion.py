from unittest.mock import MagicMock
from langchain_core.runnables import RunnableLambda
from langchain_core.messages import AIMessage

from src.enrutamiento import (
    construir_cadena_con_enrutamiento,
    construir_cadena_queja_segura,
    procesar_mensaje_seguro,
    paso_clasificacion,
)

#----------------------------------------------------
def test_clasificacion_normaliza_antes_de_comparar():
    modelo_falso = MagicMock()
    modelo_falso.return_value = AIMessage(content=" Queja \n")
    resultado = paso_clasificacion(modelo_falso).invoke(
        {"mensaje": "algo salió mal"}
    )
    assert resultado == "queja"

#----------------------------------------------------
def test_cadena_queja_usa_fallback_ante_fallo_del_modelo():
    def fallar_a_proposito(x):
        raise ConnectionError("simulado")
    cadena_queja_falsa = RunnableLambda(fallar_a_proposito)
    cadena_queja_segura = construir_cadena_queja_segura(
        cadena_queja_falsa
    )


    resultado = cadena_queja_segura.invoke(
        {"mensaje": "esto no funciona"}
    )

    assert resultado == "Gracias por tu mensaje. Un miembro de nuestro equipo te va a responder pronto."

#-------------------

def test_procesar_mensaje_seguro_no_propaga_excepciones():
    clasificacion_falsa = MagicMock()
    clasificacion_falsa.side_effect = ConnectionError(
        "simulado"
    )

    cadena_falsa = construir_cadena_con_enrutamiento(
        paso_clasificacion=clasificacion_falsa,
    )

    resultado = procesar_mensaje_seguro(
        cadena_falsa, "mensaje de prueba"
    )

    assert "no pudimos procesar" in resultado.lower()