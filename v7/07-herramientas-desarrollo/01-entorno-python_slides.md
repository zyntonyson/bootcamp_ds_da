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
        ¿Verdadero o Falso? Un IDE (como VSCode) es simplemente un editor de texto básico para tomar notas, sin herramientas adicionales para programar.
      items:
        - option: "👍 Verdadero"
        - option: "👎 Falso"
          correct: true
      feedback: |
        ¡Correcto! Es **Falso**. Un IDE (*Integrated Development Environment*) es un entorno de desarrollo completo que integra terminal, resaltado de código, extensiones, depuración y utilidades avanzadas para escribir código de manera profesional.

  - question:
      body: |
        ¿Verdadero o Falso? En Windows, recomendamos usar GitBash porque permite ejecutar comandos de terminal basados en UNIX/Linux (como `ls` y `pwd`).
      items:
        - option: "👍 Verdadero"
          correct: true
        - option: "👎 Falso"
      feedback: |
        ¡Correcto! Es **Verdadero**. GitBash emula una consola tipo Bash (Linux/macOS) en Windows, lo que nos permite usar la misma sintaxis de comandos de navegación en cualquier sistema operativo.

---

@include{path="../../slides/farewell.md"}
