@countdown{timer: 300 , title_transition: "¡Comenzamos en breve!", logo_animation: "traffic"}

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
        - option: "😇 La Paleta de Comandos con Ctrl + Shift + P (o Cmd + Shift + P) y escribir \"Git: Clone\""
          correct: true
        - option: "😎 El explorador de archivos con Ctrl + E (o Cmd + E)"
        - option: "👍 La terminal integrada y ejecutar \"git clone\""
        - option: "😄 La sección de extensiones para instalar el paquete \"Clone Git\""
      feedback: |
        ¡Correcto! Usando la Paleta de Comandos de VS Code e ingresando "Git: Clone", podemos conectar nuestra cuenta de GitHub y clonar el repositorio de forma visual y sencilla.
        
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

  - question:
      body: |
        Para guardar tus cambios locales y subirlos a GitHub, ¿cuál es el orden y propósito correcto del flujo básico de Git?
      items:
        - option: "😇 1. `git add .` (preparar), 2. `git commit -m` (guardar la foto de la versión), 3. `git push` (subir a GitHub)"
          correct: true
        - option: "😎 1. `git push` (enviar), 2. `git commit -m` (describir), 3. `git add .` (guardar archivos)"
        - option: "👍 1. `git clone` (descargar), 2. `git add .` (preparar), 3. `git init` (crear repositorio)"
        - option: "😄 1. `git commit -m` (guardar versión), 2. `git push` (subir), 3. `git status` (confirmar)"
      feedback: |
        ¡Perfecto! Siguiendo la analogía de la clase: primero preparamos la maleta con `git add .`, luego le ponemos la etiqueta descriptiva con `git commit -m`, y finalmente enviamos el equipaje al avión con `git push`.

  - question:
      body: |
        En nuestra aplicación `app.py`, ¿qué rol cumplen conjuntamente Streamlit y Plotly Express?
      items:
        - option: "😇 Plotly Express administra los commits de Git y Streamlit gestiona el servidor en Render"
        - option: "😎 Streamlit genera el conjunto de datos CSV ficticio y Plotly Express diseña la base de datos"
        - option: "👍 Streamlit construye la interfaz web interactiva y Plotly Express genera los gráficos dinámicos"
          correct: true
        - option: "😄 Plotly Express clona el repositorio y Streamlit instala las dependencias de requirements.txt"
      feedback: |
        ¡Excelente! Streamlit proporciona la estructura de la aplicación web (título, checkboxes, interactividad), mientras que Plotly Express crea visualizaciones interactivas (barras, pastel, histogramas) que responden al usuario.

  - question:
      body: |
        Al configurar el servicio web en Render, ¿cuál es la función principal del Comando de Construcción (Build Command: `pip install -r requirements.txt`)?
      items:
        - option: "😇 Mantener la app activa las 24 horas y generar el enlace público .onrender.com"
        - option: "😎 Crear un nuevo commit y enviarlo automáticamente al repositorio remoto"
        - option: "👍 Arrancar la interfaz gráfica para que los usuarios puedan interactuar con los filtros"
        - option: "😄 Descargar e instalar en el servidor de Render todas las librerías necesarias antes de iniciar la app"
          correct: true
      feedback: |
        ¡Exacto! El Build Command se ejecuta primero para preparar el entorno del servidor e instalar las dependencias necesarias de `requirements.txt`. Una vez completado, el Start Command se encarga de encender la app.

  - question:
      body: |
        ¿Por qué es necesario que nuestro repositorio en GitHub esté configurado como Público para el despliegue en esta clase?
      items:
        - option: "😇 Porque permite que el plan gratuito de Render acceda y construya el proyecto sin requerir configuraciones de pago ni llaves privadas"
          correct: true
        - option: "😎 Porque Git no permite hacer commits locales si el repositorio en la nube es privado"
        - option: "👍 Para que cualquier persona en internet pueda editar y borrar el código de tu computadora"
        - option: "😄 Porque los repositorios privados no admiten archivos de código escritos en Python"
      feedback: |
        ¡Así es! Al ser un repositorio público, Render puede conectarse, clonar el código y desplegarlo en su nivel gratuito sin necesidad de membresías de pago ni configuraciones complejas de tokens o SSH.

---

@include{path="../../slides/farewell.md"}


