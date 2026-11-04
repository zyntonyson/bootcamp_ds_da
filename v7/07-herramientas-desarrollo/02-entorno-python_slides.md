@countdown{timer: 600 , title_transition: "¡Comenzamos en breve!", logo_animation: "traffic"}

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
        - option: "😎 En la raíz del proyecto para ambos para encontrarlos más rápido"
        - option: "👍 En `scripts/` para los scripts y en `notebooks/` para los cuadernos"
          correct: true
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
        - option: "😇 `pip install pandas`"
          correct: true
        - option: "😎 `pip install pandas --global`"
        - option: "👍 `python add pandas`"
        - option: "😄 `pip download pandas`"
      feedback: |
        ¡Correcto! El comando `pip install pandas` descarga e instala la librería directamente en el entorno virtual activo. Si el entorno virtual está activado, la instalación queda aislada sólo para ese proyecto.

  - question:
      body: |
        ¿Cuál es el comando que debes ejecutar en la terminal para verificar qué versión del intérprete de Python está activa en tu entorno?
      items:
        - option: "😇 `python --help`"
        - option: "😎 `python -info`"
        - option: "👍 `pip show python`"
        - option: "😄 `python --version`"
          correct: true
      feedback: |
        ¡Exacto! `python --version` muestra en la terminal la versión del intérprete de Python que está siendo utilizada, por ejemplo `Python 3.11.9`. Es el primer comando que debes ejecutar para confirmar que el entorno está bien configurado.

  - question:
      body: |
        En VS Code, ¿cómo seleccionas el intérprete de Python correcto para que el editor use el de tu entorno virtual y no el del sistema?
      items:
        - option: "😇 Editando directamente el archivo `settings.json` y escribiendo la ruta manualmente"
        - option: "😎 Reinstalando la extensión de Python en VS Code"
        - option: "👍 Abriendo la paleta de comandos con `Ctrl+Shift+P`, buscando `Python: Select Interpreter` y eligiendo el de `.venv`"
          correct: true
        - option: "😄 Ejecutando `code --interpreter .venv` desde la terminal"
      feedback: |
        ¡Muy bien! En VS Code, usas `Ctrl+Shift+P` para abrir la paleta de comandos, escribes `Python: Select Interpreter` y seleccionas el intérprete dentro de la carpeta `.venv` de tu proyecto. Así el editor usa las librerías instaladas en tu entorno virtual.

  - question:
      body: |
        Si ya creaste tu archivo `app.py` con el código de tu panel interactivo, ¿cuál es el comando correcto para ejecutar e iniciar tu aplicación de Streamlit localmente?
      items:
        - option: "😇 `streamlit run app.py`"
          correct: true
        - option: "😎 `python app.py`"
        - option: "👍 `run app.py --streamlit`"
        - option: "😄 `python -m streamlit app.py`"
      feedback: |
        ¡Exacto! El comando `streamlit run app.py` levanta un servidor web local y abre automáticamente la pestaña de tu aplicación interactiva en el navegador predeterminado (por defecto en `http://localhost:8501`).

  - question:
      body: |
        Tienes un archivo `requirements.txt` con todas las dependencias necesarias del proyecto. ¿Qué comando debes ejecutar en la terminal para instalarlas todas juntas en tu entorno virtual activo?
      items:
        - option: "😇 `python install requirements.txt`"
        - option: "😎 `pip install -r requirements.txt`"
          correct: true
        - option: "👍 `pip load --file requirements.txt`"
        - option: "😄 `streamlit install requirements.txt`"
      feedback: |
        ¡Correcto! La opción `-r` le indica a `pip` que lea el archivo de requerimientos e instale sucesivamente cada una de las librerías listadas con sus dependencias.

  - question:
      body: |
        Tu cuaderno interactivo está ubicado en `notebooks/EDA.ipynb` y necesitas cargar el archivo `datos.csv` guardado en la carpeta `data/`. ¿Qué ruta relativa debes pasarle a `pd.read_csv()`?
      items:
        - option: "😇 `"../data/datos.csv"`"
          correct: true
        - option: "😎 `"data/datos.csv"`"
        - option: "👍 `"./data/datos.csv"`"
        - option: "😄 `"../../datos.csv"`"
      feedback: |
        ¡Excelente! Como el cuaderno de Jupyter se encuentra dentro de la carpeta `notebooks/`, se utilizan dos puntos `..` para salir al directorio raíz del proyecto y luego entrar a `data/datos.csv`.

  - question:
      body: |
        En una aplicación de Streamlit que procesa datos, ¿por qué es una buena práctica utilizar el decorador `@st.cache_data` antes de la función que carga un archivo CSV?
      items:
        - option: "😇 Porque encripta la información del archivo CSV para que sea privada"
        - option: "😎 Porque convierte automáticamente los datos tabulares en gráficos de Seaborn"
        - option: "👍 Porque sube una copia de respaldo del archivo a un servidor externo"
        - option: "😄 Porque almacena los datos en memoria para no volver a leer el archivo del disco en cada interacción o filtro, mejorando el rendimiento"
          correct: true
      feedback: |
        ¡Así es! `@st.cache_data` guarda en memoria caché los resultados de la carga. Esto previene que Streamlit reejecute lecturas pesadas desde el disco cada vez que el usuario manipula un filtro o control interactivo.

  - question:
      body: |
        En Streamlit, ¿cómo puedes ubicar controles interactivos (como selectores de categorías o casillas de verificación) dentro de la barra lateral izquierda?
      items:
        - option: "😇 Pasando el argumento `position="sidebar"` dentro de cada widget (ej. `st.selectbox(..., position="sidebar")`)"
        - option: "😎 Creando un archivo secundario llamado `sidebar.py`"
        - option: "👍 Anteponiendo `st.sidebar` al widget (ej. `st.sidebar.selectbox(...)` o `st.sidebar.checkbox(...)`)"
          correct: true
        - option: "😄 Insertando una etiqueta HTML `<sidebar>` mediante `st.markdown()`"
      feedback: |
        ¡Exacto! El prefijo `st.sidebar` dirige cualquier componente directamente al panel lateral plegable de la aplicación, dejando el área principal libre para mostrar los gráficos y tablas.

  - question:
      body: |
        Has terminado tu sesión de trabajo y deseas salir del entorno virtual activo para regresar al entorno global de tu sistema. ¿Qué comando debes ejecutar en la terminal?
      items:
        - option: "😇 `exit .venv`"
        - option: "😎 `deactivate`"
          correct: true
        - option: "👍 `python stop`"
        - option: "😄 `venv --close`"
      feedback: |
        ¡Muy bien! El comando `deactivate` cierra la sesión del entorno virtual activo y restaura las variables de entorno de tu sistema operativo (desapareciendo el prefijo `(.venv)` de la terminal). Si usas Conda, el comando correspondiente es `conda deactivate`.

  - question:
      body: |
        Al diseñar un prompt para pedirle a una Inteligencia Artificial que genere un dataset sintético útil para visualización y dashboards, ¿cuál de las siguientes es la mejor práctica?
      items:
        - option: "😇 Pedir texto libre sin especificar columnas ni número de filas para darle creatividad a la IA"
        - option: "😎 No indicar la temática ni el delimitador de datos"
        - option: "👍 Solicitar únicamente un resumen estadístico sin filas de datos reales o simuladas"
        - option: "😄 Definir la temática, especificar la cantidad exacta de filas, los tipos de columnas (numéricas, categóricas, fechas) y solicitar formato CSV separado por comas"
          correct: true
      feedback: |
        ¡Correcto! Un prompt estructurado que define temática, cantidad de filas, tipos de variables (para poder crear barras, histogramas o scatterplots) y formato de salida CSV facilita que la IA genere datos consistentes y directamente utilizables.

---

@include{path="../../slides/farewell.md"}


