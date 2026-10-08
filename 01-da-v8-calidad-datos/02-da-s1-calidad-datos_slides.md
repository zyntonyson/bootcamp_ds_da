@countdown{timer: 300 , title_transition: "¡Comenzamos en breve!", logo_animation: "traffic"}

# Sprint 1 Sesión 2
## Asegura la calidad de los datos y genera reportes básicos

---

@warnup-mood{title_transition: "Midamos los ánimos"}

# ¿Cómo llegas a la sesión de hoy?
## Reacciona con el emoji 😎🤔🤓🙂 que mejor represente tu mood

---

@include{path="content-sprint.md"}

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
@basic_slide{title_transition: "Limpieza de datos"}

# ¿Qué es la limpieza de datos? 🧹📊
## La base fundamental antes de calcular cualquier métrica

La **limpieza de datos** (*Data Cleaning*) es el proceso de identificar, corregir o remover datos incorrectos, incompletos, duplicados o mal estructurados dentro de un dataset.

* 🎯 **Los datos limpios son para el analista, no para la presentación:**  
  No limpiamos los datos solo para que una tabla se vea estética. Los limpiamos para que **nuestras fórmulas, filtros, cruces de tablas y cálculos funcionen correctamente** y no entreguen resultados falsos.
* 🗑️ **Principio GIGO (*Garbage In, Garbage Out*):**  
  Si alimentamos nuestro análisis con datos sucios o erróneos, cualquier gráfica, promedio o conclusión obtenida será incorrecta, sin importar qué tan avanzada sea la herramienta.
* ⏱️ **La regla del 80/20 en el trabajo diario:**  
  Un analista de datos dedica habitualmente entre el **60% y el 80% de su tiempo** a explorar y limpiar los datos antes de poder iniciar un análisis confiable.

---
@objectives{title_transition: "¿Por qué limpiar?"}

# ¿Qué pasa si analizamos datos sin limpiar? ⚠️🚨
## Riesgos y problemas comunes al saltarse la limpieza

* 🧮 **Cálculos y métricas distorsionadas**
    * *Valores nulos o texto en columnas numéricas rompen sumas y promedios*
    * *Filas duplicadas inflan artificialmente conteos, ingresos y totales*
    * *Valores atípicos o errores de captura distorsionan la realidad*

* 🧩 **Filtros y agrupaciones rotas**
    * *`"México"`, `"Mexico "` y `"méxico"` se contarán como 3 países diferentes*
    * *Fechas leídas como texto impiden ordenar cronológicamente o calcular plazos*
    * *Espacios invisibles provocan que funciones de búsqueda y cruces fallen*

* 💼 **Decisiones de negocio erróneas**
    * *Reportar conclusiones equivocadas a clientes y líderes de área*
    * *Pérdida de credibilidad y confianza en el equipo de analítica*
    * *Pérdida de dinero o tiempo por actuar sobre datos errados*

---
@objectives{title_transition: "Tips: Texto y Categorías"}

# Tips de Limpieza: Texto y Categorías 🔤🏷️
## Cómo estandarizar variables cualitativas

* 🔤 **Texto y Cadenas de Caracteres**
    * 🧹 **Espacios extra:** Elimina espacios al inicio, final o dobles con funciones como `ESPACIOS` / `TRIM`
    * 🔠 **Normalizar formato:** Estandariza todo a minúsculas, MAYÚSCULAS o Tipo Título
    * ✍️ **Errores tipográficos (typos):** Mapea variaciones (ej. `"Taylor Swfit"` ➔ `"Taylor Swift"`)
    * 🚫 **Caracteres especiales:** Remueve símbolos extraños y saltos de línea indeseados

* 🏷️ **Variables Categóricas**
    * 🎯 **Estandarizar etiquetas:** Homogeneiza sinónimos y siglas (ej. `"CDMX"`, `"DF"` ➔ `"Ciudad de México"`)
    * 📦 **Agrupar categorías poco frecuentes:** Junta valores con poquísimos registros bajo la etiqueta `"Otros"`
    * 🔍 **Validar dominio:** Verifica que no existan valores fuera de las opciones permitidas del negocio

---
@objectives{title_transition: "Tips: Números, Fechas y Booleanos"}

# Tips de Limpieza: Números, Fechas y Booleanos 🔢📅
## Cómo asegurar consistencia en variables cuantitativas y lógicas

* 🔢 **Valores Numéricos**
    * 💲 **Remover símbolos:** Quita signos de moneda (`$`), porcentajes (`%`) o unidades de texto (`kg`, `km`)
    * 🌐 **Separadores decimales:** Unifica el uso de punto (`.`) o coma (`,`) según la configuración regional
    * 🎯 **Redondeo y precisión:** Define una cantidad coherente de decimales para no falsear cálculos

* 📅 **Fechas y Tiempos**
    * 🗓️ **Convertir a tipo Fecha real:** Convierte texto a formato nativo `Date` para poder operar con ellas
    * 🌍 **Estandarizar formato:** Asegura el orden consistente entre día y mes (`DD/MM/YYYY` vs `MM/DD/YYYY`)
    * ⏱️ **Extraer componentes:** Desglosa año, mes o día de la semana para analizar tendencias

* 🔘 **Valores Booleanos y Lógicos**
    * ⚖️ **Criterio binario único:** Homogeneiza a un estándar único (`VERDADERO`/`FALSO`, `1`/`0`, `"Sí"`/`"No"`)
    * ❓ **Tratamiento de vacíos:** Define claramente si un valor vacío significa `FALSO` o si representa información desconocida

---
@objectives{title_transition: "Duplicados y Nulos"}

# Tips de Limpieza: Duplicados y Datos Nulos 👥🕳️
## Cómo identificar y resolver registros repetidos y valores faltantes

* 👥 **Registros Duplicados**
    * 🔍 **Identificar tipo de duplicado:** Distingue entre filas 100% idénticas y duplicados por clave (ej. mismo ID o cliente)
    * 🧹 **Eliminación inteligente:** Emplea herramientas como `Quitar duplicados` o la función `UNIQUE()` conservando el registro válido
    * ⚠️ **Investigar el origen:** Evalúa si se trata de un error de captura o transacciones legítimas antes de borrar

* 🕳️ **Valores Nulos y Faltantes**
    * ❓ **Comprender el motivo:** Identifica si el dato no aplica (ej. segundo nombre), no fue capturado o hubo un fallo de carga
    * 🗑️ **Eliminación justificada:** Si faltan campos críticos o una fila tiene demasiados vacíos, evalúa descartarla
    * 🩹 **Imputación adecuada:** Sustituye con medidas como mediana/promedio (numéricos) o etiquetas como `"Sin registrar"` (texto)
    * 🚫 **Peligro con el cero:** Nunca reemplaces vacíos con `0` a ciegas en métricas como salarios o edades, pues altera promedios

---
@overlay{title_transition: ""}

# 💡 Regla de Oro del Analista

"Los datos limpios no son para que las tablas se vean bonitas; son la garantía de que tus cálculos, gráficos y decisiones reflejen la realidad."




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
        ¿Cuál de las siguientes es una forma adecuada de eliminar filas duplicadas en una hoja de cálculo?
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


