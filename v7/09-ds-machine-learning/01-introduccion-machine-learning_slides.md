@countdown{timer: 600 , title_transition: "¡Comenzamos en breve!", logo_animation: "traffic"}

# Sprint 10 Sesión 1
## Introducción al machine learning

---

@warnup-mood{title_transition: "Midamos los ánimos"}

# ¿Cómo llegas a la sesión de hoy?
## Reacciona con el emoji 😎🤔🤓🙂 que mejor represente tu mood

---
@agenda{title_transition: "Nuestra Agenda de Hoy"}

# Plan de nuestra sesión


* 👋 Bienvenida {5}
* 🐍 Introducción al Machine Learning: Revisión de conceptos 💻📊 {75}
* 🤔 Reflexión y discusión: ¿Qué aprendimos en esta sesión? {5}

---
@objectives{title_transition: "¿Qué aprenderemos hoy?"}

# Metas para esta sesión

* 🧠 Introducción al Machine Learning:
  * Comprender qué es el aprendizaje automático y diferenciar entre regresión y clasificación.
* 🔄 Ciclo de vida de un modelo de ML:
  * Describir las etapas de un proyecto de ML desde la definición del problema hasta su monitoreo.
* 🌿 Clasificación con scikit-learn:
  * Entrenar y comparar modelos como Regresión Logística, Árbol de Decisión y Random Forest.
  * Identificar sobreajuste (overfitting) y subajuste (underfitting) con métricas apropiadas.
* 📈 Regresión con scikit-learn:
  * Entrenar y evaluar modelos de Regresión Lineal, Árboles y Random Forest.
  * Utilizar métricas como el Error Cuadrático Medio (MSE) y la raíz del MSE (RMSE).

---

@gotocode{title_transition: "Momento de trabajar en equipo"}

# ¡A trabajar en equipo!


* [Introducción al Machine Learning](../../img/qrs/01-introduccion-machine-learning.png) 

---
@quizz{time_limit: 80}

# Pongamos a prueba lo aprendido
## Reaccciona en la llamada con el emoji de la respuesta correcta

quizz:
  - question:
      body: |
        ¿Cuál es la definición principal de Machine Learning (Aprendizaje Automático)?
      items:
        - option: "😇 Programar manualmente todas las reglas lógicas que debe seguir una computadora"
        - option: "😎 La capacidad de una computadora para aprender patrones a partir de datos sin ser explícitamente programada"
          correct: true
        - option: "👍 Un tipo de procesador físico más rápido para bases de datos"
        - option: "😄 Un sistema operativo que reemplaza a Windows y macOS"
      feedback: |
        ¡Exacto! El Machine Learning permite que los algoritmos identifiquen patrones en los datos para tomar decisiones por sí mismos, sin necesidad de programar reglas manualmente.

  - question:
      body: |
        Si queremos predecir el precio de una casa (un valor numérico continuo), ¿qué tipo de tarea de Machine Learning estamos realizando?
      items:
        - option: "😇 Clasificación"
        - option: "😎 Regresión"
          correct: true
        - option: "👍 Agrupamiento (Clustering)"
        - option: "😄 Preparación de datos"
      feedback: |
        ¡Correcto! Las tareas de Regresión se encargan de predecir valores numéricos continuos (como precios, temperaturas o salarios).

  - question:
      body: |
        Si queremos clasificar si un correo electrónico es "spam" o "no spam", ¿qué tipo de tarea estamos realizando?
      items:
        - option: "😇 Regresión"
        - option: "😎 Clasificación"
          correct: true
        - option: "👍 División de datos"
        - option: "😄 Entrenamiento lineal"
      feedback: |
        ¡Muy bien! Cuando el objetivo es predecir una categoría o etiqueta (entre un conjunto de opciones discretas), estamos ante un problema de Clasificación.

  - question:
      body: |
        ¿Por qué es fundamental dividir nuestros datos en un conjunto de entrenamiento (train) y otro de prueba (test)?
      items:
        - option: "😇 Para que la computadora procese los datos el doble de rápido"
        - option: "😎 Para evaluar el rendimiento del modelo con datos que nunca ha visto y medir su capacidad de generalización"
          correct: true
        - option: "👍 Porque scikit-learn no funciona si no se dividen los datos"
        - option: "😄 Para borrar los datos duplicados de forma automática"
      feedback: |
        ¡Excelente! Evaluar el modelo con un conjunto de prueba (test) independiente nos permite simular cómo se comportará con datos nuevos del mundo real.

  - question:
      body: |
        ¿Qué ocurre cuando un modelo sufre de sobreajuste (overfitting)?
      items:
        - option: "😇 El modelo memoriza los datos de entrenamiento y falla al intentar generalizar con datos nuevos"
          correct: true
        - option: "😎 El modelo es demasiado simple y no aprende nada de los datos"
        - option: "👍 El modelo predice perfectamente tanto en entrenamiento como en prueba"
        - option: "😄 El modelo se entrena en un tiempo extremadamente corto"
      feedback: |
        ¡Correcto! El sobreajuste (overfitting) sucede cuando el modelo "se aprende de memoria" el conjunto de entrenamiento, perdiendo la capacidad de hacer buenas predicciones en datos nuevos.
        
  - question:
      body: |
        ¿Cuál es el orden lógico de las primeras etapas en el ciclo de vida de un proyecto de Machine Learning?
      items:
        - option: "😇 Despliegue -> Monitoreo -> Entrenamiento"
        - option: "😎 Definición del problema -> Preparación de datos -> Entrenamiento -> Evaluación"
          correct: true
        - option: "👍 Evaluación -> Despliegue -> Recolección de datos"
        - option: "😄 Entrenamiento -> Recolección de datos -> Definición del problema"
      feedback: |
        ¡Excelente! Primero definimos el problema, luego recolectamos y preparamos los datos, entrenamos el modelo y finalmente lo evaluamos antes de su despliegue y monitoreo.
---

@include{path="../../slides/farewell.md"}
