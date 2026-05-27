@countdown{timer: 600 , title_transition: "¡Comenzamos en breve!", logo_animation: "traffic"}

# Sprint 2 Sesión 2
## Transformar datos para insights de negocio

---

@warnup-mood{title_transition: "Midamos los ánimos"}

# ¿Cómo llegas a la sesión de hoy?
## Reacciona con el emoji 😎🤔🤓🙂 que mejor represente tu mood

---
@agenda{title_transition: "Nuestra Agenda de Hoy"}

# Plan de nuestra sesión


* 👋 Bienvenida {5}
* Avisos parroquiales 📢 {5}
* Analisis exploratorio de datos: Caso Almacen Global   {45}
* 🤔 Reflexión y discusión: ¿Qué aprendimos en esta sesión? {5}

---
@include{path="../slides/out_office.md"}

---
@objectives{title_transition: "¿Qué aprenderemos hoy?"}

# Metas de contenido para esta sesión

* 🎯 Conocer cómo definir el tipo de preguntas que se pueden hacer para analizar datos:
  * Comprender el problema central y los objetivos estratégicos del negocio.
  * Identificar stakeholders y sus necesidades.
* 📏 Conocer las diferentes métricas que se pueden calcular para analizar datos (KPIs, OKRs, Guardrails):
  * Definir indicadores clave de rendimiento (KPIs) para medir el éxito.
  * Conocer OKRs (Objectives and Key Results) y cómo utilizarlos para establecer metas.
* 🛠️ Aplicar herramientas de procesamiento y análisis de datos:
  * Funciones de búsqueda y concatenación de tablas (Vlookup).
  * Aplicar filtros avanzados para obtener información específica.
  * Crear tablas dinámicas para analizar datos.
* 💡 Crear visualizaciones para comunicar insights de negocio:
  * Seleccionar el gráfico más adecuado según la información a transmitir.
  * Aplicar principios de *storytelling* para facilitar la toma de decisiones.

---

@gotocode{title_transition: "Momento de trabajar en equipo"}

# ¡A trabajar en equipo!


* [Transformar datos para insights de negocio](../img/qrs/03-da-v8-insights-negocio.png)

---
@quizz{time_limit: 180}

# Pongamos a prueba lo aprendido: Google Sheets
## Reacciona en la llamada con el emoji de la respuesta correcta

quizz:
  - question:
      body: |
        Tenemos la siguiente tabla de muestra en el rango A1:C4:
        
        ```text
        |   | A (ID) | B (Producto) | C (Precio) |
        |---|--------|--------------|------------|
        | 1 | P101   | Laptop       | 800        |
        | 2 | P102   | Mouse        | 25         |
        | 3 | P103   | Teclado      | 45         |
        | 4 | P104   | Monitor      | 150        |
        ```
        
        Si ejecutamos la siguiente fórmula en otra celda:
        `=BUSCARV("P103", A1:C4, 3, FALSO)`
        
        ¿Cuál será el resultado devuelto por Google Sheets?
      items:
        - option: "😇 'Teclado'"
        - option: "😎 45"
          correct: true
        - option: "👍 'P103'"
        - option: "😄 #N/A"
      feedback: |
        ¡Correcto! `BUSCARV` busca el valor "P103" en la primera columna del rango (`A1:A4`), que está en la fila 3, y devuelve el valor que se encuentra en la tercera columna de esa misma fila (`C3`), que es `45`. El argumento `FALSO` indica que se busca una coincidencia exacta.

  - question:
      body: |
        Tienes una tabla con información de ventas que incluye las columnas: `Región` (Norte, Sur, Este, Oeste), `Categoría` (Tecnología, Muebles), y `Ventas` ($).
        
        Si arrastras `Región` a **Filas**, `Categoría` a **Columnas** y `Ventas` a **Valores** (con la función SUMAR), ¿cómo se estructurará visualmente tu tabla dinámica?
      items:
        - option: "😇 Tendrás 4 columnas (una por región) y 2 filas (una por categoría) con la suma de ventas en las intersecciones."
        - option: "😎 Tendrás una sola columna con las regiones y categorías una debajo de la otra."
        - option: "👍 Tendrás 4 filas (una por región) y 2 columnas (una por categoría) con la suma de ventas en las intersecciones."
          correct: true
        - option: "😄 Tendrás una tabla con las regiones en las filas y las ventas en las columnas, ignorando por completo la categoría."
      feedback: |
        ¡Correcto! Al configurar la tabla dinámica con `Región` en **Filas**, cada región única (Norte, Sur, Este, Oeste) ocupará una fila distinta (4 filas en total). Al poner `Categoría` en **Columnas**, cada categoría única (Tecnología, Muebles) ocupará una columna distinta (2 columnas en total). Las intersecciones mostrarán el cálculo de `Ventas` para esa combinación específica de región y categoría.


  - question:
      body: |
        Un analista financiero crea una tabla dinámica que ocupa el rango A1:C10. Para automatizar un reporte, escribe en la celda E1 la siguiente fórmula:
        `=BUSCARV("Total General", A1:C10, 4, FALSO)`
        
        ¿Por qué esta fórmula arrojará un error #REF!?
      items:
        - option: "😇 Porque el término 'Total General' contiene un espacio y `BUSCARV` no soporta espacios."
        - option: "😎 Porque la tabla dinámica está protegida y no permite búsquedas directas sobre ella."
        - option: "👍 Porque el rango de búsqueda `A1:C10` solo tiene 3 columnas, pero se solicitó devolver la columna número 4."
          correct: true
        - option: "😄 Porque el argumento `FALSO` debería ser `VERDADERO` para buscar totales."
      feedback: |
        ¡Exacto! El error `#REF!` (Referencia no válida) ocurre cuando le pides a `BUSCARV` que devuelva una columna que está fuera de los límites del rango especificado. Dado que el rango `A1:C10` abarca desde la columna A hasta la C (3 columnas en total), indicarle un índice de columna `4` está fuera del rango, resultando en este error.
  - question:
      body: |
        Al agregar un 'Campo Calculado' dentro de una Tabla Dinámica en Google Sheets, debes utilizar siempre los nombres exactos de las columnas de tu base de datos de origen como variables dentro de la fórmula (por ejemplo, `= Ventas / Cantidad`), de lo contrario la tabla dinámica mostrará un error `#ERROR!`.
      items:
        - option: "😇 Verdadero"
          correct: true
        - option: "😎 Falso"
      feedback: |
        ¡Excelente! Los campos calculados requieren que hagas referencia precisa a los nombres de las columnas que contienen los datos numéricos de origen. Si escribes mal un nombre de columna, o usas nombres que no existen, Google Sheets no podrá procesar la fórmula personalizada del campo y mostrará un error en todas las celdas de esa columna.

---

@include{path="../slides/farewell.md"}