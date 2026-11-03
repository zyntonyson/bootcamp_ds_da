@countdown{timer: 300 , title_transition: "¡Comenzamos en breve!", logo_animation: "traffic"}

# Sprint 7 Sesión 1
## Herramientas de desarrollo de software: Entorno local para análisis de datos con Python

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
* 🐍 Herramientas de desarrollo de software: ¡Tu Primer Entorno de Análisis de Datos! 💻📊 {75}
* 🤔 Reflexión y discusión: ¿Qué aprendimos en esta sesión? {5}

---
@objectives{title_transition: "¿Qué aprenderemos hoy?"}

# Metas para esta sesión

* 🖥️ Uso de la terminal:
  * Comprender qué es una terminal y su utilidad para automatizar flujos de datos.
  * Utilizar comandos esenciales de navegación (`pwd`, `ls`, `cd`) .
* 🐍 Configurar el entorno de Python y un IDE local:
  * Seleccionar e instalar una versión estable de Python y verificar su instalación con `python --version`.
  * Comprender qué es un IDE e instalar VSCode junto con sus extensiones esenciales (*Python* y *Jupyter*).
* 📦 Crear y administrar entornos virtuales:
  * Comprender la importancia del aislamiento de dependencias para evitar conflictos entre proyectos.
  * Aprender a crear un entorno virtual con `python -m virtualenv .venv` y activarlo según tu sistema operativo.
* 📊 Instalar librerías de datos y ejecutar código interactivo:
  * Utilizar `pip` para instalar librerías clave (`pandas`, `numpy`, `matplotlib`, `seaborn`, `jupyter`) de manera individual o usando un archivo *requirements.txt*.
  * Crear un cuaderno interactivo (.ipynb) en VSCode, seleccionar el entorno virtual como kernel y ejecutar scripts para analizar y visualizar información.

---

@gotocode{title_transition: "Momento de trabajar en equipo"}

# ¡A trabajar en equipo!


* [Entorno Local de Análisis de Datos](../../img/qrs/01-entorno-python.png) 

---
@quizz{time_limit: 80}

# Pongamos a prueba lo aprendido
## Reaccciona en la llamada con el emoji de la respuesta correcta

quizz:
  - question:
      body: |
        ¿Cuál es el beneficio principal de crear un entorno virtual (`.venv`) para un proyecto de análisis de datos?
      items:
        - option: "😇 Aumentar la velocidad de procesamiento de Python"
        - option: "😎 Guardar una copia de seguridad automática de tu código en GitHub"
        - option: "👍 Aislar las librerías del proyecto para evitar conflictos de versiones"
          correct: true
        - option: "😄 Permitir que Windows corra comandos de Mac nativamente"
      feedback: |
        ¡Exacto! Los entornos virtuales sirven para aislar las dependencias (librerías) de cada proyecto de forma independiente, evitando conflictos de compatibilidad en tu computadora.
  - question:
      body: |
        ¿Cuál es la función del comando `pwd` en la terminal?
      items:
        - option: "😇 Listar los archivos dentro del directorio actual"
        - option: "😎 Mostrar la ruta completa del directorio donde te encuentras"
          correct: true
        - option: "👍 Cambiar a una carpeta diferente"
        - option: "😄 Crear un archivo de texto vacío"
      feedback: |
        ¡Correcto! `pwd` significa *Print Working Directory* e imprime en pantalla la ruta absoluta de la carpeta en la que estás trabajando.

  - question:
      body: |
        ¿Qué comando de la terminal debes utilizar para instalar en bloque las librerías listadas en un archivo *requirements.txt*?
      items:
        - option: "😇 `pip install -r requirements.txt`"
          correct: true
        - option: "😎 `python install requirements.txt`"
        - option: "👍 `pip get requirements.txt`"
        - option: "😄 `python -m requirements.txt`"
      feedback: |
        ¡Excelente! La opción `-r` le indica a `pip` que lea el archivo de requerimientos e instale de forma masiva todos los paquetes y versiones especificados en él.

  - question:
      body: |
        Tienes un archivo llamado `analisis.py` en tu carpeta de proyecto. ¿Cuál es el comando correcto para ejecutarlo desde la terminal?
      items:
        - option: "😇 `run script analisis.py`"
        - option: "😎 `python analisis.py`"
          correct: true
        - option: "👍 `pip start analisis.py`"
        - option: "😄 `execute analisis.py`"
      feedback: |
        ¡Correcto! Para ejecutar un script de Python desde la terminal usamos `python nombre_del_archivo.py` (o `python3` según tu sistema operativo).

  - question:
      body: |
        Al ejecutar tu código, la terminal muestra el error `ModuleNotFoundError: No module named 'pandas'`. ¿Qué significa y cómo lo resuelves?
      items:
        - option: "😇 El archivo de código está corrupto y debes crearlo de nuevo"
        - option: "😎 El sistema operativo bloqueó Python y debes reiniciar la computadora"
        - option: "👍 La librería `pandas` no está instalada en el entorno actual; debes ejecutar `pip install pandas`"
          correct: true
        - option: "😄 La sintaxis del archivo está mal y debes renombrar el archivo a `pandas.py`"
      feedback: |
        ¡Muy bien! Este error indica que el intérprete no encuentra la librería en tu entorno activo (o no activaste el entorno virtual). La solución es instalarla usando `pip install pandas`.

  - question:
      body: |
        ¿Cómo puedes activar tu entorno virtual `.venv` en Windows (GitBash) y cómo confirmas visualmente que está activo?
      items:
        - option: "😇 Ejecutas `pip on .venv` y la terminal se cierra automáticamente"
        - option: "😎 Ejecutas `source .venv/Scripts/activate` y verás el prefijo `(.venv)` al inicio de la terminal"
          correct: true
        - option: "👍 Ejecutas `python activate` y se abre una pestaña en el navegador web"
        - option: "😄 Ejecutas `start virtualenv` y el texto de la terminal cambia de color a verde"
      feedback: |
        ¡Así es! En Windows con GitBash activamos el entorno con `source .venv/Scripts/activate` (o `source .venv/bin/activate` en macOS/Linux). Sabrás que está activo porque aparecerá `(.venv)` al inicio de la línea de comandos.

---

@include{path="../../slides/farewell.md"}
