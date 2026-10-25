BANCO_DE_PROMPT = [

    {
        "nombre": "simple",
        "system_instruction": "Eres un chef, Responde corto y en formato pedido",
        "ejemplo_usuario": "Hazme un menú ficticio de 3 platos. Máximo 15 palabras por plato. Formato: Nombre, ingredientes. Sin explicacion y dime cuál es el plato más recomendado en una frase corta",
        "claves_esperadas": ["platos", "recomendado"],
        "response_schema": {
            "type": "OBJECT",
            "properties": {
                "platos": {"type": "array", "items": {"type": "string"}},
                "recomendado": {"type": "string"}
            },
            "required": ["platos", "recomendado"]
        }
    },
    {
        "nombre": "compleja",
        "system_instruction": "Eres un nutricionista experto.",
        "ejemplo_usuario": "Hazme un menú ficticio de 3 platos. Formato: Nombre, ingredientes (no mas de 8). Luego responde: Soy celíaco, ¿cuál de estos platos del menú NO me recomiendas y cuáles SÍ? Dime unicamente cual es el ingrediente que podria afectarme.",
        "claves_esperadas": ["no_recomendado", "si_recomendado", "ingrediente"],
        "response_schema": {
            "type": "OBJECT",
            "properties": {
                "no_recomendado": {"type": "string"},
                "si_recomendado": {"type": "array", "items": {"type": "string"}},
                "ingrediente": {"type": "string"}
            },
            "required": ["no_recomendado", "si_recomendado", "ingrediente"]
        }
    }

]