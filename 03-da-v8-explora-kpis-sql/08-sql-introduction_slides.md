@countdown{timer: 300 , title_transition: "¡Comenzamos en breve!", logo_animation: "traffic"}

# Sprint 3 Sesión 2
## Explorar KPIs con SQL


---

@warnup-mood{title_transition: "Midamos los ánimos"}

# ¿Cómo llegas a la sesión de hoy?
## Reacciona con el emoji 😎🤔🤓🙂 que mejor represente tu mood

---
@agenda{title_transition: "Nuestra Agenda de Hoy"}

# Plan de nuestra sesión


* 👋 Bienvenida {5}
* 🚀 Introducción a bases de datos relacionales y consultas SQL (Continuación) {100}
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
@quizz{time_limit: 80}

# Recordemos algunos conceptos anteriores
## Reaccciona en la llamada con el emoji de la respuesta correcta

quizz:
  - question:
      body: |
        En una base de datos relacional, la información se organiza en tablas compuestas por filas y columnas, y estas tablas se pueden conectar entre sí mediante relaciones de claves (keys).
      items:
        - option: "😇 Verdadero"
          correct: true
        - option: "😎 Falso"
      feedback: |
        ¡Correcto! Las bases de datos relacionales organizan la información en tablas que se vinculan mediante claves primarias y foráneas.

  - question:
      body: |
        Al escribir una consulta en SQL, la cláusula `ORDER BY` se debe colocar antes de la cláusula `WHERE`.
      items:
        - option: "😇 Verdadero"
        - option: "😎 Falso"
          correct: true
      feedback: |
        ¡Correcto! En la sintaxis de SQL, la cláusula `WHERE` (para filtrar) siempre va antes de la cláusula `ORDER BY` (para ordenar).

  - question:
      body: |
        Si ejecutamos la siguiente consulta:
        
        ```sql
        SELECT title
        FROM film
        WHERE release_year = 2020;
        ```
        
        El resultado incluirá todos los campos (columnas) de las películas estrenadas en el año 2020.
      items:
        - option: "😇 Verdadero"
        - option: "😎 Falso"
          correct: true
      feedback: |
        ¡Correcto! Es falso porque el `SELECT` solo especifica la columna `title`. Si quisiéramos todas las columnas, deberíamos usar `SELECT *`.

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
        ¿Cuál de las siguientes consultas calcula el total de clientes (filas) y el límite de crédito más alto de la tabla `customers`?
      items:
        - option: "😇 SELECT SUM(customer_id), MAX(credit_limit) FROM customers;"
        - option: "😎 SELECT COUNT(*), MAX(credit_limit) FROM customers;"
          correct: true
        - option: "👍 SELECT COUNT(*), HIGH(credit_limit) FROM customers;"
        - option: "😄 SELECT COUNT(credit_limit), SUM(credit_limit) FROM customers;"
      feedback: |
        ¡Correcto! Usamos `COUNT(*)` para contar todas las filas de la tabla y `MAX(credit_limit)` para obtener el valor máximo del límite de crédito. Como no se usa `GROUP BY`, el resultado es una sola fila con ambos totales.

  - question:
      body: |
        Queremos calcular el monto total vendido por cada empleado (`employee_id`) usando la función `SUM(amount)`.
        
        ¿Qué cláusula debemos agregar al final de la consulta para agrupar los resultados correctamente?
      items:
        - option: "😇 ORDER BY employee_id"
        - option: "😎 WHERE employee_id"
        - option: "👍 GROUP BY employee_id"
          correct: true
        - option: "😄 HAVING employee_id"
      feedback: |
        ¡Exacto! La cláusula `GROUP BY employee_id` le indica a la base de datos que agrupe las filas que tienen el mismo ID de empleado para que la función agregada `SUM()` calcule la suma para cada uno de ellos.

  - question:
      body: |
        Tienes una tabla `orders` (con la columna `customer_id`) y una tabla `customers` (con la columna `customer_id`).
        
        ¿Cuál es la forma correcta de unir ambas tablas para obtener los datos de los pedidos junto con los nombres de los clientes?
      items:
        - option: "😇 SELECT * FROM orders JOIN customers ON orders.customer_id = customers.customer_id;"
          correct: true
        - option: "😎 SELECT * FROM orders MERGE customers WHERE orders.customer_id = customers.customer_id;"
        - option: "👍 SELECT * FROM orders ON customers WHERE orders.customer_id = customers.customer_id;"
        - option: "😄 SELECT * FROM orders, customers WHERE JOIN;"
      feedback: |
        ¡Correcto! La sintaxis estándar de SQL usa la cláusula `JOIN` (o `INNER JOIN`) para especificar la tabla a unir y la cláusula `ON` para establecer la condición de igualdad entre las claves correspondientes.

  - question:
      body: |
        Queremos crear una nueva columna temporal en el resultado para clasificar los productos según su precio. Si el precio es mayor a 100, debe decir 'Caro'; de lo contrario, 'Barato'.
        
        ¿Cuál es la sintaxis correcta utilizando `CASE`?
      items:
        - option: "😇 CASE WHEN price > 100 THEN 'Caro' ELSE 'Barato' END"
          correct: true
        - option: "😎 IF price > 100 THEN 'Caro' ELSE 'Barato'"
        - option: "👍 SELECT CASE price > 100 = 'Caro' ELSE 'Barato'"
        - option: "😄 CASE WHEN price > 100 DO 'Caro' DEFAULT 'Barato' STOP"
      feedback: |
        ¡Correcto! La expresión condicional en SQL utiliza la estructura `CASE WHEN [condición] THEN [resultado] ELSE [resultado_alternativo] END`.

---

@include{path="../slides/farewell.md"}
