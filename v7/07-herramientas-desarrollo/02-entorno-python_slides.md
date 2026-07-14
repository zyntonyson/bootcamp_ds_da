@countdown{timer: 600 , title_transition: "¡Comenzamos en breve!", logo_animation: "traffic"}

# Sprint 7 Sesión 2
## Herramientas de desarrollo de software: Creando un dashboard con Streamlit 

---

@warnup-mood{title_transition: "Midamos los ánimos"}

# ¿Cómo llegas a la sesión de hoy?
## Reacciona con el emoji 😎🤔🤓🙂 que mejor represente tu mood

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
        Después de instalar nuevas librerías en tu entorno virtual con `pip install`, ¿cuál es la buena práctica recomendada para registrar de forma automática estas dependencias en tu archivo de requerimientos?
      items:
        - option: "😇 Ejecutar `pip install -r requirements.txt` en la consola"
        - option: "😎 Ejecutar `pip freeze > requirements.txt` en la consola"
          correct: true
        - option: "👍 Crear manualmente un archivo llamado `libraries.json`"
        - option: "😄 Ejecutar `python -m venv requirements.txt` en la consola"
      feedback: |
        ¡Excelente! `pip freeze > requirements.txt` exporta el listado exacto de las librerías instaladas en tu entorno virtual activo y lo guarda en `requirements.txt`, asegurando que cualquier otra persona pueda replicar exactamente tu entorno.

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


