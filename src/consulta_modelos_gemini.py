import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv() # lee tu archivo .env donde guardaste tu API KEY
genai.configure(api_key=os.getenv("GEMINI_API_KEY")) # se autentica con Google

# Pide a Google: "dame la lista de todos los modelos que puedo usar con mi API KEY"
for m in genai.list_models():
    if "3.1" in m.name or "3.5" in m.name or "3.8" in m.name:
        print(m.name) # imprime solo los 3.x