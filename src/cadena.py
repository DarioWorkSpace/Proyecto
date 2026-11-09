from dotenv import load_dotenv
import os
from langchain_google_genai import ChatGoogleGenerativeAI #Crea un modelo de lenguaje de Google Gemini
from langchain_core.prompts import PromptTemplate #la plantilla para el prompt dinámico
from langchain_core.output_parsers import StrOutputParser #Para parsear las respuesas
from langchain_core.prompts import ChatPromptTemplate #Plantilla 

load_dotenv()

modelo = ChatGoogleGenerativeAI(model="gemini-3.1-flash" )
#respuesta = modelo.invoke("¿Que es un token?")
#print(respuesta.content)

plantilla = PromptTemplate.from_template("Explica el concepto de {tema} en un parrrafo, para alguien que recien comienza en {area}.") #Se puede agregar system_instructions

#prompt = plantilla.invoke({"tema": "tokenización", "area": "procesamiento de texto"})

#print(prompt.text)

cadena_simple = plantilla | modelo | StrOutputParser()
respuesta = cadena_simple.invoke({"tema": "embeddings", "area": "búsqueda semántica"})
print(respuesta.content)

plantilla_conrol = ChatPromptTemplate.from_messages([
    ("system", "Eres un experto en el área correspondiente, vas a responder siempre con texto simple para el usuario."), 
    ("user", "Explica el concepto de {tema} en un parrafo, para alguien que recien commienza en {area}?")
])
