@countdown{timer: 600 , title_transition: "¡Comenzamos en breve!", logo_animation: "traffic"}

# Sprint 3 Sesión 4
## Explorar KPIs con SQL


---

@warnup-mood{title_transition: "Midamos los ánimos"}

# ¿Cómo llegas a la sesión de hoy?
## Reacciona con el emoji 😎🤔🤓🙂 que mejor represente tu mood

---
@agenda{title_transition: "Nuestra Agenda de Hoy"}

# Plan de nuestra sesión


* 👋 Bienvenida {5}
* 🔎 Revisión del proyecto del sprint {5}
* 💡 Consultas SQL para análisis de negocio: Caso Readify {60} 
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


* [Análisis de negocio: Caso Readify](../img/qrs/10-insights-sql-books.png)
* [SQL runner](../img/qrs/sql-interface.png)

---
@quizz{time_limit: 80}

# Pongamos a prueba lo aprendido
## Reaccciona en la llamada con el emoji de la respuesta correcta

quizz:
  - question:
      body: |
        Si ejecutas la siguiente consulta para analizar la valoración del catálogo en Readify:
        
        ```sql
        SELECT AVG(rating) AS promedio_valoracion
        FROM ratings;
        ```
        
        ¿Qué métrica de negocio estás calculando?
      items:
        - option: "😇 La calificación más alta registrada por un usuario."
        - option: "😎 La cantidad total de calificaciones recibidas en la plataforma."
        - option: "👍 La satisfacción promedio o calidad percibida del catálogo por parte de los lectores."
          correct: true
        - option: "😄 El número de usuarios activos que han calificado algún libro."
      feedback: |
        ¡Correcto! La función `AVG(rating)` calcula el promedio de todas las calificaciones de la tabla `ratings`, representando la calidad general o satisfacción percibida de los lectores.

  - question:
      body: |
        Para identificar libros extensos (de largo aliento) en Readify, ejecutamos la siguiente consulta:
        
        ```sql
        SELECT book_id, title
        FROM books
        WHERE num_pages > 500;
        ```
        
        ¿Qué registros devolverá esta consulta?
      items:
        - option: "😇 Todos los libros que tienen exactamente 500 páginas."
        - option: "😎 Únicamente los libros con una extensión de páginas estrictamente mayor a 500."
          correct: true
        - option: "👍 Los primeros 500 libros registrados en la base de datos."
        - option: "😄 Todos los libros ordenados de mayor a menor número de páginas."
      feedback: |
        ¡Exacto! La condición `WHERE num_pages > 500` filtra las filas para mostrar solo aquellos libros cuya extensión de páginas supera el valor de 500.

  - question:
      body: |
        Para analizar el catálogo de libros según la editorial que los publica, ejecutamos:
        
        ```sql
        SELECT publisher_id, COUNT(*) AS total_libros
        FROM books
        GROUP BY publisher_id;
        ```
        
        ¿Qué resultado produce esta consulta?
      items:
        - option: "😇 Muestra la editorial con los libros más largos del catálogo."
        - option: "😎 Cuenta cuántos libros han sido publicados por cada editorial (publisher_id)."
          correct: true
        - option: "👍 Filtra los libros para mostrar solo los que pertenecen a una editorial específica."
        - option: "😄 Muestra el promedio de páginas de todos los libros de la base de datos."
      feedback: |
        ¡Correcto! `GROUP BY publisher_id` agrupa los libros por su editorial asociada, y `COUNT(*)` cuenta el número de títulos pertenecientes a cada grupo de editorial.

  - question:
      body: |
        Para identificar el nombre del autor o autora de cada libro de nuestro catálogo, usamos la siguiente consulta:
        
        ```sql
        SELECT books.title, authors.author
        FROM books
        INNER JOIN authors ON books.author_id = authors.author_id;
        ```
        
        ¿Por qué es necesario usar `INNER JOIN` en esta consulta?
      items:
        - option: "😇 Porque los títulos de los libros están en la tabla `books` y los nombres de los autores en `authors`."
          correct: true
        - option: "😎 Porque queremos ordenar los libros alfabéticamente por el nombre del autor."
        - option: "👍 Porque `INNER JOIN` elimina automáticamente los libros con títulos duplicados."
        - option: "😄 Porque de lo contrario la base de datos no sabría cómo calcular el total de páginas de cada autor."
      feedback: |
        ¡Así es! Los datos de negocio están distribuidos en dos tablas: `books` (información del libro) y `authors` (nombre del autor). El `JOIN` las une usando la clave común `author_id`.

  - question:
      body: |
        Analiza la siguiente consulta que busca identificar libros con alta interacción y debate:
        
        ```sql
        WITH debate_libros AS (
            SELECT book_id, COUNT(review_id) AS total_reseñas
            FROM reviews
            GROUP BY book_id
        )
        SELECT book_id
        FROM debate_libros
        WHERE total_reseñas > 10;
        ```
        
        ¿Qué información devuelve esta consulta?
      items:
        - option: "😇 Los IDs de los libros que recibieron más de 10 reseñas escritas en un solo día."
        - option: "😎 Los IDs de los libros que han acumulado más de 10 reseñas escritas en total en la plataforma."
          correct: true
        - option: "👍 El total de reseñas escritas en toda la plataforma cuando el total supera las 10."
        - option: "😄 Una lista de todos los libros ordenados de mayor a menor cantidad de reseñas."
      feedback: |
        ¡Excelente! La CTE `debate_libros` calcula primero la cantidad total de reseñas escritas para cada libro. Luego, la consulta principal filtra y muestra solo los IDs de aquellos libros que superan las 10 reseñas acumuladas.

---

@include{path="../slides/farewell.md"}
