@countdown{timer: 600 , title_transition: "¡Comenzamos en breve!", logo_animation: "traffic"}

# Sprint 3 Sesión 1
## Explorar KPIs con SQL


---

@warnup-mood{title_transition: "Midamos los ánimos"}

# ¿Cómo llegas a la sesión de hoy?
## Reacciona con el emoji 😎🤔🤓🙂 que mejor represente tu mood

---
@agenda{title_transition: "Nuestra Agenda de Hoy"}

# Plan de nuestra sesión


* 👋 Bienvenida {5}
* 🚀 Introducción a bases de datos relacionales y consultas SQL {100}
* 🤔 Reflexión y discusión: ¿Qué aprendimos en esta sesión? {5}

---
@objectives{title_transition: "¿Qué aprenderemos hoy?"}

# Metas de contenido para esta sesión

* 🗄️ **Comprender los fundamentos de bases de datos y consultas SQL**:
  * Conocer el concepto de bases de datos relacionales y cómo se estructuran las tablas.
  * Entender la sintaxis y el orden de ejecución lógico de una consulta SQL.
* 🔍 **Realizar consultas de selección y filtrado**:
  * Dominar la selección básica de columnas usando `SELECT` y `FROM`.
  * Ordenar y limitar los resultados obtenidos con `ORDER BY` y `LIMIT`.
  * Aplicar filtros avanzados a los registros mediante la cláusula `WHERE`.
* 📊 **Categorizar y segmentar información**:
  * Utilizar expresiones condicionales con `CASE` para clasificar y etiquetar datos dinámicamente.
* 🤝 **Relacionar y unir información de múltiples tablas**:
  * Combinar datos relacionados de distintas tablas utilizando la cláusula `JOIN`.
* 🧬 **Estructurar consultas avanzadas con subconsultas y CTEs**:
  * Implementar subconsultas dentro de las cláusulas `FROM` y `WHERE`.
  * Organizar y simplificar consultas complejas utilizando expresiones de tabla comunes con `WITH`.

---

@gotocode{title_transition: "Momento de trabajar en equipo"}

# ¡A trabajar en equipo!


* [Explorar KPIs con SQL](../img/qrs/07-sql-introduction.png)
* [SQL runner](../img/qrs/sql-interface.png)

---
@quizz{time_limit: 80}

# Pongamos a prueba lo aprendido
## Reaccciona en la llamada con el emoji de la respuesta correcta

quizz:
  - question:
      body: |
        ¿Cuál es la función principal de un Sistema de Gestión de Bases de Datos Relacionales (RDBMS) y del lenguaje SQL?
      items:
        - option: "😇 Almacenar la información de manera estructurada en tablas relacionadas y permitir consultarla mediante un lenguaje estándar."
          correct: true
        - option: "😎 Diseñar únicamente la interfaz gráfica de usuario y las páginas web de una aplicación."
        - option: "👍 Almacenar archivos de texto plano sin ningún tipo de estructura ni relación entre ellos."
        - option: "😄 Ejecutar de forma automática códigos de programación en Python y JavaScript en el navegador."
      feedback: |
        ¡Correcto! Una base de datos relacional organiza la información en tablas (filas y columnas) conectadas por claves, y SQL es el lenguaje estándar para consultar y manipular esta estructura.

  - question:
      body: |
        Estás buscando las 5 películas más largas de una tabla llamada `film`.
        
        ¿Cuál es la combinación correcta de cláusulas que debes usar para ordenar los resultados de mayor a menor duración (`length`) y mostrar solo 5 registros?
      items:
        - option: "😇 ORDER BY length ASC LIMIT 5"
        - option: "😎 WHERE length > 5 ORDER BY length DESC"
        - option: "👍 ORDER BY length DESC LIMIT 5"
          correct: true
        - option: "😄 SELECT length FROM film WHERE LIMIT = 5"
      feedback: |
        ¡Exacto! Usamos 'ORDER BY length DESC' para ordenar de mayor a menor (descendente) y 'LIMIT 5' para restringir el número de resultados a las primeras 5 filas.

  - question:
      body: |
        Deseas clasificar las películas en dos categorías: 'Larga' (si dura más de 120 minutos) y 'Corta' (en cualquier otro caso).
        
        ¿Cuál es la sintaxis básica correcta usando `CASE` en tu consulta?
      items:
        - option: "😇 CASE WHEN length > 120 THEN 'Larga' WHEN length <= 120 THEN 'Corta'"
        - option: "😎 IF length > 120 THEN 'Larga' ELSE 'Corta' END"
        - option: "👍 CASE length > 120 THEN 'Larga' ELSE 'Corta'"
        - option: "😄 CASE WHEN length > 120 THEN 'Larga' ELSE 'Corta' END"
          correct: true
      feedback: |
        ¡Excelente! La expresión CASE comienza con 'CASE WHEN [condición] THEN [valor]' y siempre debe terminar con la palabra clave 'END', pudiendo opcionalmente usar 'ELSE' para el caso por defecto.

  - question:
      body: |
        Quieres consultar la tabla `film` (películas) y la tabla `language` (idiomas) para ver el nombre de la película y su idioma.
        
        ¿Qué tipo de cláusula y condición debes emplear para unir ambas tablas usando el campo común `language_id`?
      items:
        - option: "😇 JOIN language WHERE film.language_id in language.language_id"
        - option: "😎 JOIN language ON film.language_id = language.language_id"
          correct: true
        - option: "👍 JOIN language USING language_id WHERE ON"
        - option: "😄 MERGE language WHERE language_id = language_id"
      feedback: |
        ¡Correcto! La cláusula 'JOIN' (o 'INNER JOIN') se acompaña de la condición 'ON' para especificar qué columnas de ambas tablas se corresponden para realizar la unión.

  - question:
      body: |
        Quieres definir una consulta temporal llamada `data` que puedas reutilizar dentro de tu consulta principal para hacer tu código más limpio y modular.
        
        ¿Cuál es la forma correcta de iniciar una Expresión de Tabla Común (CTE) en SQL?
      items:
        - option: "😇 DEFINE data AS (SELECT * FROM film)"
        - option: "😎 SELECT * FROM (SELECT * FROM film) AS data"
        - option: "👍 WITH data AS (SELECT * FROM film)"
          correct: true
        - option: "😄 CREATE TEMP TABLE data AS (SELECT * FROM film)"
      feedback: |
        ¡Perfecto! La cláusula 'WITH' permite definir una CTE (Common Table Expression), actuando como una subconsulta temporal nombrada que simplifica y organiza el código SQL complejo.

---

@include{path="../slides/farewell.md"}
