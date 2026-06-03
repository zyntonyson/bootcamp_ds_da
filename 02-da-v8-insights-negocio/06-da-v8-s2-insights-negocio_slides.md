@countdown{timer: 600 , title_transition: "¡Comenzamos en breve!", logo_animation: "traffic"}

# Sprint 2 Sesión 4
## Transformar datos para insights de negocio

---

@warnup-mood{title_transition: "Midamos los ánimos"}

# ¿Cómo llegas a la sesión de hoy?
## Reacciona con el emoji 😎🤔🤓🙂 que mejor represente tu mood

---
@agenda{title_transition: "Nuestra Agenda de Hoy"}

# Plan de nuestra sesión


* 👋 Bienvenida {5}
* 🏗️ Revisión del proyecto del sprint {5}
* 〽️ Actividad colaborativa: Reporte para marcas (*Continuación*)   {40}
* 🤔 ¿Qué hemos aprendido en este sprint? (Repaso con Quiz) {10}
* 🤔 Reflexión y discusión: ¿Qué aprendimos en esta sesión? {5}

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


* [Transformar datos para insights de negocio](../img/qrs/05-da-v8-insigths-negocio.png)
---

@quizz{time_limit: 90, title_transition: "¡Repasemos algunos conceptos!"}

# Quizz de repaso
## Transformar datos para insights de negocio

> Reacciona en el chat con el emoji de la respuesta correcta

quizz:
  - question:
      body: |
        Estás preparando un reporte de ventas en Google Sheets y notas que una columna de números no se suma correctamente y todos los valores están alineados a la izquierda de la celda.
        
        ¿Qué indica principalmente esta alineación a la izquierda y cómo deberías solucionarlo?
      items:
        - option: "😄 Que los números están almacenados como texto. Se soluciona seleccionando la columna y aplicando el formato de número desde el menú de formato."
          correct: true
        - option: "👍 Que las celdas contienen un error de fórmula oculto. Se soluciona eliminando la columna y volviéndola a escribir."
        - option: "😇 Que la columna tiene activado un filtro de visualización. Se soluciona haciendo doble clic en la cabecera de la columna."
        - option: "❤️ Que los números son excesivamente grandes para el ancho actual de la columna. Se soluciona ensanchando la columna."
      feedback: |
        ¡Correcto! En Google Sheets (y la mayoría de las hojas de cálculo), el texto se alinea automáticamente a la izquierda y los números a la derecha de forma predeterminada. Cuando los números se alinean a la izquierda, la hoja de cálculo los interpreta como texto y las funciones matemáticas como `SUMA` los ignoran. Convertirlos al formato numérico adecuado resuelve el problema.

  - question:
      body: |
        Tienes una hoja de cálculo con información de clientes y notas que en la columna "Teléfono" hay varios registros vacíos (valores nulos). Para evitar celdas en blanco en tu reporte final, deseas rellenar estas celdas vacías con el texto "No provisto" de forma dinámica mediante una fórmula.
        
        ¿Qué función de Google Sheets te permite evaluar si una celda está vacía para poder imputar este valor?
      items:
        - option: "😄 `=SI(ESBLANCO(B2); \"No provisto\"; B2)`"
          correct: true
        - option: "👍 `=SI.ERROR(B2; \"No provisto\")`"
        - option: "😇 `=CONTAR.BLANCO(B2; \"No provisto\")`"
        - option: "❤️ `=QUITAR.ESPACIOS(B2; \"No provisto\")`"
      feedback: |
        ¡Excelente! La función `ESBLANCO` evalúa si una celda está vacía. Al anidarla dentro de una condicional `SI`, puedes especificar que si la celda está vacía se devuelva el texto "No provisto", y si tiene un valor, conserve el valor original (`B2`).

  - question:
      body: |
        Tenemos la siguiente tabla de clientes en el rango A1:C4 de Google Sheets:
        
        ```text
        |   | A (ID_Cliente) | B (Nombre)  | C (País)    |
        |---|----------------|-------------|-------------|
        | 1 | ID_Cliente     | Nombre      | País        |
        | 2 | C001           | Mateo       | Chile       |
        | 3 | C002           | Sofía       | México      |
        | 4 | C003           | Valentina   | Colombia    |
        ```
        
        Si escribimos la siguiente fórmula en otra celda:
        `=BUSCARV("C002"; A2:C4; 3; FALSO)`
        
        ¿Qué resultado nos devolverá Google Sheets?
      items:
        - option: "😄 'Sofía'"
        - option: "👍 'México'"
          correct: true
        - option: "😇 'Colombia'"
        - option: "❤️ #N/A"
      feedback: |
        ¡Muy bien! La fórmula `BUSCARV` busca el identificador "C002" en la primera columna del rango especificado (`A2:A4`), lo encuentra en la segunda fila del rango (fila 3 de la hoja), y devuelve el valor que se encuentra en la tercera columna del rango (`C3`), que corresponde a "México". El argumento `FALSO` garantiza una búsqueda exacta.

  - question:
      body: |
        Un colega está intentando obtener la ciudad de un cliente usando la fórmula:
        `=BUSCARV("C003"; B2:D10; 3; FALSO)`
        
        La base de datos original tiene los siguientes campos: la columna A contiene el "ID_Cliente", la columna B el "Nombre", la columna C la "Ciudad" y la columna D el "Teléfono". La fórmula le devuelve un error `#N/A`.
        
        ¿Cuál es la razón principal por la que esta fórmula está fallando?
      items:
        - option: "😄 Porque el rango de búsqueda inicia en la columna B, por lo que `BUSCARV` intenta encontrar el ID \"C003\" en la columna de nombres en lugar de la columna A."
          correct: true
        - option: "👍 Porque el índice 3 excede las columnas disponibles en el rango `B2:D10`."
        - option: "😇 Porque se especificó el parámetro `FALSO` en lugar de `VERDADERO` para una búsqueda de coincidencia exacta."
        - option: "❤️ Porque la columna de destino (\"Ciudad\") está a la izquierda de la columna de búsqueda."
      feedback: |
        ¡Exacto! `BUSCARV` siempre busca el valor de coincidencia en la *primera* columna del rango proporcionado. Dado que el rango se definió como `B2:D10`, la función busca el ID "C003" en la columna B (que contiene los nombres de los clientes). Al no encontrarlo allí, devuelve el error `#N/A` (no disponible). Para solucionarlo, el rango debería ser `A2:D10`.

  - question:
      body: |
        Trabajas con un conjunto de datos que incluye: `Categoría` (Electrónica, Ropa, Hogar), `Mes` (Enero, Febrero), `Canal` (Online, Tienda Física) y `Ventas` ($). Tu gerente te pide un reporte dinámico para identificar los ingresos totales de cada categoría en cada mes, considerando únicamente las ventas realizadas por el canal "Online".
        
        ¿Cómo deberías configurar las áreas de tu tabla dinámica en Google Sheets para responder a esta petición?
      items:
        - option: "😄 Filas: 'Categoría'; Columnas: 'Mes'; Valores: 'Ventas' (SUMAR); Filtros: 'Canal' (filtrado para mostrar solo 'Online')."
          correct: true
        - option: "👍 Filas: 'Canal'; Columnas: 'Categoría'; Valores: 'Ventas' (CONTAR); Filtros: 'Mes' (filtrado para mostrar solo 'Enero')."
        - option: "😇 Filas: 'Ventas'; Columnas: 'Canal'; Valores: 'Categoría' (SUMAR); Filtros: ninguno."
        - option: "❤️ Filas: 'Categoría' y 'Mes'; Columnas: ninguna; Valores: 'Canal' (PROMEDIO); Filtros: 'Ventas'."
      feedback: |
        ¡Correcto! Al configurar 'Categoría' en las filas y 'Mes' en las columnas, creas una estructura cruzada muy fácil de leer. Agregar las 'Ventas' a los valores mediante la función `SUMAR` te dará los ingresos de cada cruce. Finalmente, al colocar 'Canal' en los filtros y seleccionar únicamente 'Online', aíslas los datos necesarios para cubrir el requerimiento del negocio.

  - question:
      body: |
        Al estructurar una pregunta analítica de negocio efectiva para guiar un proyecto de datos, es fundamental evitar preguntas ambiguas.
        
        ¿Cuál de los siguientes grupos de elementos representa los aspectos clave indispensables que debe incorporar la redacción de la pregunta para ser accionable?
      items:
        - option: "😄 El objetivo del negocio, la métrica/KPI de éxito, el segmento de interés (ej. tipo de usuario/producto) y el marco temporal del análisis."
          correct: true
        - option: "👍 El motor de base de datos preferido, la velocidad de procesamiento, el presupuesto del hardware y la cantidad de columnas de la tabla."
        - option: "😇 La tipografía del dashboard final, la paleta de colores de la presentación, el número de diapositivas y el nombre del diseñador."
        - option: "❤️ El tipo de gráfico que se usará para el reporte, la hora de la junta de presentación y los datos de contacto de los stakeholders."
      feedback: |
        ¡Muy bien! Una pregunta analítica de negocio sólida debe ser clara y estar delimitada por el contexto del negocio: el propósito u objetivo, la métrica que utilizaremos para evaluar el comportamiento, los segmentos específicos a los que se reduce el estudio y la ventana de tiempo aplicable. Los aspectos de diseño, infraestructura o herramientas técnicas se definen de manera independiente.

  - question:
      body: |
        Una gráfica de líneas es la mejor opción de visualización cuando necesitamos mostrar la participación de mercado de 5 marcas competidoras en un año específico y estático (composición en un único punto en el tiempo).
      items:
        - option: "😇 Verdadero"
        - option: "😎 Falso"
          correct: true
      feedback: |
        ¡Correcto! Las gráficas de líneas se diseñan específicamente para mostrar tendencias y cambios en los datos a lo largo del tiempo (secuencias continuas). Para mostrar la distribución o participación de mercado estática de un grupo reducido de categorías, una gráfica de barras (horizontal o vertical) o una gráfica circular/anillo resulta mucho más intuitiva y efectiva para comparar proporciones en un solo momento.

  - question:
      body: |
        Considera la siguiente formulación realizada por un equipo de marketing: *"¿Cómo podemos hacer para que nuestros clientes compren mucho más en el sitio web durante el próximo año?"*
        
        Esta pregunta está correctamente estructurada como una **pregunta analítica de negocio** accionable.
      items:
        - option: "😇 Verdadero"
        - option: "😎 Falso"
          correct: true
      feedback: |
        ¡Exacto! Esta formulación es demasiado subjetiva y vaga. Términos como "compren mucho más" no especifican una métrica cuantitativa (¿hablamos de frecuencia de compra, ticket promedio o tasa de conversión?). Tampoco acota los segmentos (¿todos los clientes o clientes nuevos vs recurrentes?). Una formulación analítica accionable sería: *"¿Qué categorías de productos y qué segmentos de usuarios recurrentes impulsaron el aumento de la tasa de conversión el año pasado, y cómo podemos optimizar su experiencia para incrementar el valor de compra promedio en un 10% el próximo trimestre?"*

---
@include{path="../slides/farewell.md"}