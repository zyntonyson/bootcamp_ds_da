@countdown{timer: 60 , title_transition: "¡Comenzamos en breve!", logo_animation: "traffic"}

# Sprint 7 Sesión 3
## Herramientas de desarrollo de software: Compartiendo tu Proyecto en GitHub y Despliegue en Render

---

@warnup-mood{title_transition: "Midamos los ánimos"}

# ¿Cómo llegas a la sesión de hoy?
## Reacciona con el emoji 😎🤔🤓🙂 que mejor represente tu mood

---
@include{path="content_sprint.md"}

---
@agenda{title_transition: "Nuestra Agenda de Hoy"}

# Plan de nuestra sesión


* 👋 Bienvenida {5}
* 🐍 Herramientas de desarrollo de software: ¡Compartiendo tu Proyecto en GitHub y Despliegue en Render! 💻📊 {75}
* 🤔 Reflexión y discusión: ¿Qué aprendimos en esta sesión? {5}

---
@objectives{title_transition: "¿Qué aprenderemos hoy?"}

# Metas para esta sesión

* 🌿 Git y GitHub en VS Code:
  * Comprender la diferencia e importancia de Git y GitHub en el desarrollo de software.
  * Crear y clonar repositorios remotos directamente desde la interfaz visual de VS Code.
  * Dominar el flujo básico de Git (`add`, `commit`, `push`) para subir tu código a la nube.
* 🤖 IA y visualización de datos:
  * Diseñar prompts con IA para generar un conjunto de datos personalizado y una app interactiva.
  * Construir gráficos dinámicos usando la librería Plotly Express integrada con Streamlit.
* 🚀 Despliegue en la nube:
  * Desplegar tu aplicación en la nube de forma gratuita en Render para que esté visible en línea.

---

@gotocode{title_transition: "Momento de trabajar en equipo"}

# ¡A trabajar en equipo!


* [Despliegue de tu proyecto ](../../img/qrs/03-entorno-python.png) 

---
@quizz{time_limit: 80}

# Pongamos a prueba lo aprendido
## Reaccciona en la llamada con el emoji de la respuesta correcta

quizz:
  - question:
      body: |
        ¿Cuál es la diferencia principal entre Git y GitHub?
      items:
        - option: "😇 Git es la plataforma en la nube y GitHub es el motor local"
        - option: "😎 Git es el sistema de control de versiones local y GitHub es la plataforma en la nube para alojar repositorios"
          correct: true
        - option: "👍 Git sirve para diseñar dashboards y GitHub sirve para escribir código Python"
        - option: "😄 Git es una base de datos y GitHub es un editor de texto"
      feedback: |
        ¡Excelente! Git es el motor local que controla las versiones de tu código en tu computadora, mientras que GitHub es el servicio web en la nube que hospeda esos repositorios.

  - question:
      body: |
        Para clonar un repositorio remoto directamente desde VS Code sin usar comandos de consola, ¿qué herramienta debemos abrir primero?
      items:
        - option: "😇 El explorador de archivos con Ctrl + E (o Cmd + E)"
        - option: "😎 La Paleta de Comandos con Ctrl + Shift + P (o Cmd + Shift + P) y escribir \"Git: Clone\""
          correct: true
        - option: "👍 La terminal integrada y ejecutar \"git clone\""
        - option: "😄 La sección de extensiones para instalar el paquete \"Clone Git\""
      feedback: |
        ¡Correcto! Usando la Paleta de Comandos de VS Code e ingresando "Git: Clone", podemos conectar nuestra cuenta de GitHub y clonar el repositorio de forma visual y sencilla.

  - question:
      body: |
        Al preparar el archivo `requirements.txt` para desplegar en Render, ¿cuál es una buena práctica recomendada para las versiones de las librerías?
      items:
        - option: "😇 Especificar siempre el número de versión exacto de cada librería"
        - option: "😎 No colocar números de versión para permitir que Render instale las versiones más recientes y estables"
          correct: true
        - option: "👍 Escribir los nombres de las librerías en mayúsculas"
        - option: "😄 Incluir el comando pip install antes de cada librería"
      feedback: |
        ¡Así es! Al no definir versiones específicas (ej. escribir `streamlit` en lugar de `streamlit==1.25.0`), Render descarga automáticamente las versiones estables compatibles con su sistema operativo Linux, evitando conflictos de dependencias.
        
  - question:
      body: |
        Al configurar el despliegue de una app de Streamlit en Render, ¿cuál debe ser el Comando de Inicio (Start Command)?
      items:
        - option: "😇 `pip install -r requirements.txt`"
        - option: "😎 `python app.py`"
        - option: "👍 `streamlit run app.py`"
          correct: true
        - option: "😄 `git push origin main`"
      feedback: |
        ¡Correcto! `pip install -r requirements.txt` es el Comando de Construcción (Build Command), mientras que `streamlit run app.py` es el Comando de Inicio (Start Command) que efectivamente arranca el servidor para que los usuarios accedan a la web.

---

@include{path="../../slides/farewell.md"}


