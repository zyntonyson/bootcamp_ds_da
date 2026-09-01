@countdown{timer: 300 , title_transition: "¡Comenzamos en breve!", logo_animation: "traffic"}

# Sprint 7 Sesión 2
## Herramientas de desarrollo de software: Creando un dashboard con Streamlit 

---

@warnup-mood{title_transition: "Midamos los ánimos"}

# ¿Cómo llegas a la sesión de hoy?
## Reacciona con el emoji 😎🤔🤓🙂 que mejor represente tu mood

---

@include{path="./content_sprint.md"}


---
@agenda{title_transition: "Nuestra Agenda de Hoy"}

# Plan de nuestra sesión


* 👋 Bienvenida {5}
* 🐍 Herramientas de desarrollo de software: ¡Creando un dashboard con Streamlit! 💻📊 {75}
* 🤔 Reflexión y discusión: ¿Qué aprendimos en esta sesión? {5}

---
@objectives{title_transition: "¿Qué aprenderemos hoy?"}

# Metas para esta sesión

* 🤖 IA y visualización de datos:
  * Diseñar prompts con IA para generar un conjunto de datos personalizado y una app interactiva.
  * Construir gráficos dinámicos usando la librería Plotly Express integrada con Streamlit.


---

@gotocode{title_transition: "Momento de trabajar en equipo"}

# ¡A trabajar en equipo!


* [Aplicación de Streamlit ](../../img/qrs/02-entorno-python.png) 

---
@quizz{time_limit: 80}

# Pongamos a prueba lo aprendido
## Reaccciona en la llamada con el emoji de la respuesta correcta

quizz:
  - question:
      body: |
        Si estás estructurando un proyecto profesional de Python para análisis de datos, ¿en qué carpeta es más recomendable guardar los scripts de automatización (archivos `.py`) y en cuál los cuadernos interactivos (archivos `.ipynb`)?
      items:
        - option: "😇 En `data/` para los scripts y en `prompts/` para los cuadernos"
        - option: "😎 En `scripts/` para los scripts y en `notebooks/` para los cuadernos"
          correct: true
        - option: "👍 En la raíz del proyecto para ambos para encontrarlos más rápido"
        - option: "😄 En `.venv/` para los scripts y en `data/` para los cuadernos"
      feedback: |
        ¡Correcto! La estructura recomendada organiza los scripts ejecutables en `scripts/` y los cuadernos de análisis interactivo (Jupyter Notebooks) en `notebooks/`, manteniendo el proyecto limpio y profesional.

  - question:
      body: |
        ¿Para qué sirve crear un entorno virtual en nuestro proyecto de Python y cuál es el comando correcto para activarlo en Windows usando la terminal GitBash?
      items:
        - option: "😇 Sirve para acelerar la velocidad de ejecución de Python y se activa con `python -m virtualenv .venv`"
        - option: "😎 Sirve para aislar las dependencias del proyecto evitando conflictos y se activa con `source .venv/Scripts/activate`"
          correct: true
        - option: "👍 Sirve para sincronizar nuestro código con GitHub y se activa con `pip freeze > requirements.txt`"
        - option: "😄 Sirve para diseñar la interfaz visual y se activa con `streamlit run app.py`"
      feedback: |
        ¡Así es! El entorno virtual aísla las librerías instaladas para evitar conflictos de versiones entre distintos proyectos. En Windows usando GitBash, se activa con el comando `source .venv/Scripts/activate`.

  - question:
      body: |
        Necesitas instalar la librería `pandas` en tu entorno virtual activo. ¿Cuál es el comando correcto para hacerlo con `pip`?
      items:
        - option: "😇 `pip install pandas --global`"
        - option: "😎 `pip install pandas`"
          correct: true
        - option: "👍 `python add pandas`"
        - option: "😄 `pip download pandas`"
      feedback: |
        ¡Correcto! El comando `pip install pandas` descarga e instala la librería directamente en el entorno virtual activo. Si el entorno virtual está activado, la instalación queda aislada sólo para ese proyecto.

  - question:
      body: |
        ¿Cuál es el comando que debes ejecutar en la terminal para verificar qué versión del intérprete de Python está activa en tu entorno?
      items:
        - option: "😇 `python --help`"
        - option: "😎 `python --version`"
          correct: true
        - option: "👍 `python -info`"
        - option: "😄 `pip show python`"
      feedback: |
        ¡Exacto! `python --version` muestra en la terminal la versión del intérprete de Python que está siendo utilizada, por ejemplo `Python 3.11.9`. Es el primer comando que debes ejecutar para confirmar que el entorno está bien configurado.

  - question:
      body: |
        En VS Code, ¿cómo seleccionas el intérprete de Python correcto para que el editor use el de tu entorno virtual y no el del sistema?
      items:
        - option: "😇 Editando directamente el archivo `settings.json` y escribiendo la ruta manualmente"
        - option: "😎 Abriendo la paleta de comandos con `Ctrl+Shift+P`, buscando `Python: Select Interpreter` y eligiendo el de `.venv`"
          correct: true
        - option: "👍 Reinstalando la extensión de Python en VS Code"
        - option: "😄 Ejecutando `code --interpreter .venv` desde la terminal"
      feedback: |
        ¡Muy bien! En VS Code, usas `Ctrl+Shift+P` para abrir la paleta de comandos, escribes `Python: Select Interpreter` y seleccionas el intérprete dentro de la carpeta `.venv` de tu proyecto. Así el editor usa las librerías instaladas en tu entorno virtual.

  - question:
      body: |
        Si ya creaste tu archivo `app.py` con el código de tu panel interactivo, ¿cuál es el comando correcto para ejecutar e iniciar tu aplicación de Streamlit localmente?
      items:
        - option: "😇 `python app.py`"
        - option: "😎 `streamlit run app.py`"
          correct: true
        - option: "👍 `run app.py --streamlit`"
        - option: "😄 `python -m streamlit app.py`"
      feedback: |
        ¡Exacto! El comando `streamlit run app.py` levanta un servidor web local y abre automáticamente la pestaña de tu aplicación interactiva en el navegador predeterminado (por defecto en `http://localhost:8501`).

---

@include{path="../../slides/farewell.md"}


