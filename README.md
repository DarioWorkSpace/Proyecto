# Plantilla de repositorio base — Especialización en Desarrollo con IA Generativa (Accenture)

Esta es la estructura base que vas a usar como punto de partida para tu proyecto en este programa. Es la misma estructura que vas a ir ampliando bloque a bloque, hasta llegar a la aplicación completa que entregas en el Gate 3.

## Requisitos Previos
Para poder ejecutar este proyecto necesitas tener instalado y configurado lo siguiente:

1.  **Python 3.10 o superior:** Verifica con `python --version`. El proyecto usa `venv` y librerías compatibles con Python 3.10+.
2.  **Git:** Necesario para clonar el repositorio y versionar el código.
3.  **Cuenta en Google AI Studio:** Para obtener tu `GEMINI_API_KEY` gratis desde https://aistudio.google.com/app/apikey
4.  **Visual Studio Code (recomendado):** Con la extensión de Python.
5.  **Acceso a terminal:** PowerShell en Windows o bash/zsh en Linux/Mac para activar el entorno virtual.

No necesitas instalar librerías globalmente, todo se instala dentro del entorno virtual con `requirements.txt`.

## Cómo empezar

Estos pasos se completan de forma progresiva a lo largo de la Unidad U1.2, no todos el mismo día:

1. Clona este repositorio utilizando el comando "git clone https://github.com/DarioWorkSpace/Proyecto"
2. Crea tu entorno virtual de Python usando el comando <python -m venv venv> (por ejemplo, con `venv`) y actívalo en tu terminal usando el comando <venv/bin/activate> o <venv/Scripts/activate> segun tu equipo.
3. Instala las dependencias del proyecto usando el comando <pip install - r requirements.txt> para poder usarlas en la aplicacion.
4. Copia `.env.example` a un archivo nuevo llamado `.env` usando el comando <cp .env.example .env>, y completa ahí usando tu API.
5. Para ejecutar la aplicacion usa el comando <python src/consumir_gemini.py> para hacer la consulta a la api de gemini, <python src/evaluar_modelo.py> para evaluar los datos de latencia y costo en los modelos elejidos o <python src/consistencia.py> para ejecutar el banco de prompts

## Estructura de carpetas

- `src/` : todo el código fuente de tu proyecto va aquí.
- `docs/` : documentación técnica del proyecto (diagramas, decisiones de arquitectura, notas).
- `tests/` : pruebas de tu código (las vas a usar más adelante en el programa, cuando el proyecto lo requiera).
- `requirements.txt` : dependencias de Python de tu proyecto, para que cualquier otra persona pueda reconstruir tu entorno con un solo comando.
- `.env.example` : plantilla de las variables de entorno que tu proyecto necesita, sin valores reales. Tu archivo `.env` real (con tus credenciales) nunca se commitea.
- `.gitignore` : le dice a Git qué archivos y carpetas ignorar (entre ellos, tu entorno virtual y tu archivo `.env`).

## Reglas que se mantienen durante todo el programa

- Ningún secreto (contraseña, llave de API, token) va escrito directamente en el código ni en ningún archivo que se suba al repositorio.
- Cada proyecto nuevo tiene su propio entorno virtual: no se comparten dependencias entre proyectos distintos.
- Todo el trabajo que se entrega en este programa vive en un repositorio de GitHub, sin excepción.

## Registro del ensayo de instalación limpia
 
- Fecha: 25/10/2026
- Encontrado: faltaba 'requests' en requirements.txt (estaba instalado a mano)
- Corregido: agregado con 'pip freeze > requirements.txt' y commiteado
- Resultado tras la corrección: el proyecto corre sin intervención manual