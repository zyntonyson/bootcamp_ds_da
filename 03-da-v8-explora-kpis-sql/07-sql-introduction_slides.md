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
        Quieres filtrar la tabla `film` para encontrar todas las películas cuyo título comienza exactamente con la letra 'A'.
        
        ¿Qué condición en la cláusula `WHERE` debes utilizar para lograrlo?
      items:
        - option: "😇 WHERE title = 'A%'"
        - option: "😎 WHERE title LIKE 'A%'"
          correct: true
        - option: "👍 WHERE title IN ('A')"
        - option: "😄 WHERE title CONTAINS 'A'"
      feedback: |
        ¡Correcto! El operador LIKE junto con el comodín '%' permite realizar búsquedas de patrones de texto. 'A%' buscará cualquier texto que empiece con 'A' seguido de cualquier carácter.

  - question:
      body: |
        Al escribir una consulta en SQL, debes usar las cláusulas `WHERE`, `ORDER BY` y `LIMIT` al mismo tiempo.
        
        ¿Cuál es el orden correcto en el que deben estructurarse estas palabras clave en tu consulta?
      items:
        - option: "😇 SELECT ... FROM ... ORDER BY ... LIMIT ... WHERE ..."
        - option: "😎 SELECT ... FROM ... LIMIT ... WHERE ... ORDER BY ..."
        - option: "👍 SELECT ... FROM ... WHERE ... ORDER BY ... LIMIT ..."
          correct: true
        - option: "😄 SELECT ... FROM ... WHERE ... LIMIT ... ORDER BY ..."
      feedback: |
        ¡Excelente! En la sintaxis de SQL, el filtro de filas (WHERE) siempre debe declararse antes de la ordenación (ORDER BY), y el límite de filas (LIMIT) se coloca al final de la consulta.
---

@include{path="../slides/farewell.md"}
