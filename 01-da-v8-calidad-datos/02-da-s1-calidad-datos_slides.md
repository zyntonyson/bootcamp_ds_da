@countdown{timer: 300 , title_transition: "¡Comenzamos en breve!", logo_animation: "traffic"}

# Sprint 1 Sesión 2
## Asegura la calidad de los datos y genera reportes básicos

---

@warnup-mood{title_transition: "Midamos los ánimos"}

# ¿Cómo llegas a la sesión de hoy?
## Reacciona con el emoji 😎🤔🤓🙂 que mejor represente tu mood

---

@agenda{title_transition: "Nuestra Agenda de Hoy"}

# Plan de nuestra sesión



* 👋 Bienvenida {10}
*  📊🧹 Proyecto colaborativo: Taylor Swift dataset 👱‍♀️💃  {60}
* 🤔 Reflexión y discusión: ¿Qué aprendimos en esta sesión? {10}

---
@objectives{title_transition: "¿Qué aprenderemos hoy?"}

# Metas de contenido para esta sesión

* 🧹 **Aplicar técnicas de limpieza de datos**
    * *Corregir formatos inconsistentes*
    * *Tratar valores nulos o duplicados*
* 🧮 **Calcular métricas descriptivas**
    * *Obtener promedios, medianas y frecuencias*
    * *Resumir información clave del dataset*
* 📊 **Generar visualizaciones de datos**
    * *Crear gráficos básicos para analizar tendencias*
    * *Facilitar la interpretación de la información*
* 💡 **Descubrir insights en los datos**
    * *Identificar patrones y relaciones ocultas*
    * *Generar conclusiones útiles a partir de los datos*

---
@gotocode{title_transition: "Manos a la Obra"}

# Escanea el código para los materiales de la clase



* [Limpieza de datos: Taylor Swift Dataset](../img/qrs/01-da-s1-calidad-datos.png)


---

@quizz{time_limit: 60}

# Pongamos a prueba lo aprendido
## Reaccciona en la llamada con el emoji de la respuesta correcta

quizz:
  - question:
      body: |
        ¿Qué actividad no es típica de un analista de datos?
      items:
        - option: "😇 Entrevistar a los clientes"
          correct: true
        - option: "😎 Revisar la calidad de los datos"
        - option: "👍 Comunicar insights de los datos"
        - option: "😄 Calcular métricas de los datos"
      feedback: |
        ¡Correcto! Entrevistar a los clientes es una tarea más típica de investigación de usuarios o equipos de producto. Nuestro trabajo principal es analizar la información que ya ha sido recolectada y extraer valor de ella.

  - question:
      body: |
        ¿Cuál de las siguientes etapas debería ser la primera al realizar un análisis de datos?
      items:
        - option: "😇 Calcular métricas como sumas y porcentajes"
        - option: "😎 Hacer tablas y gráficas"
        - option: "👍 Conocer el origen de los datos"
          correct: true
        - option: "😄 Realizar limpieza de los datos"
      feedback: |
        ¡Excelente! Antes de hacer cualquier limpieza o cálculo, debemos entender de dónde vienen los datos, qué significan y bajo qué contexto fueron generados.

  - question:
      body: |
        Al limpiar datos, no necesariamente...
      items:
        - option: "😇 Revisamos existencia de datos repetidos"
        - option: "😎 Identificamos/Tratamos los datos faltantes"
        - option: "👍 Estandarizamos el formato de los datos"
        - option: "😄 Ordenamos los valores de menor a mayor"
          correct: true
      feedback: |
        ¡Exacto! El orden de los valores no afecta la calidad de los datos per se. Limpiar datos se enfoca en que la información sea correcta, completa y consistente, independientemente de cómo esté ordenada.

  - question:
      body: |
        Si tienes una columna de texto con valores inconsistentes como `"  mAnZaNa "`, `"Manzana "`, y `"MANZANA"`, ¿Qué acciones son necesarias para limpiar estos datos en una hoja de cálculo?
      items:
        - option: "😇 Usar la función BUSCARV para encontrar la palabra correcta"
        - option: "😎 Aplicar funciones para eliminar espacios (ESPACIOS/TRIM) y estandarizar mayúsculas/minúsculas (MINUSC/MAYUSC)"
          correct: true
        - option: "👍 Filtrar la columna y borrar manualmente los que se ven raros"
        - option: "😄 Ordenar alfabéticamente y sumar los valores"
      feedback: |
        ¡Exacto! Para limpiar cadenas de texto inconsistentes, lo ideal es quitar los espacios extra al inicio/final y estandarizar todo a un solo formato usando las funciones de texto integradas.

  - question:
      body: |
        ¿Cuál de las siguientes es una forma adecuada de eliminar filas duplicadas en Google Sheets o Excel?
      items:
        - option: "😇 Usar la función SUMAR.SI para agrupar los datos"
        - option: "😎 Ordenar los datos y borrar a mano las filas que parezcan iguales"
        - option: "👍 Ocultar las filas que se ven repetidas para que no estorben"
        - option: "😄 Utilizar la herramienta integrada de 'Quitar duplicados' o la función UNIQUE()"
          correct: true
      feedback: |
        ¡Correcto! Las hojas de cálculo cuentan con herramientas nativas para identificar y eliminar filas duplicadas de manera automática y sin errores humanos.


---


@include{path="../slides/farewell.md"}


