@countdown{timer: 300 , title_transition: "¡Comenzamos en breve!", logo_animation: "traffic"}

# Sprint 3 Sesión 3
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
* 🚀 Introducción a bases de datos relacionales y consultas SQL (Continuación) {20}
* 💡 Consultas SQL para análisis de negocio: Caso Sakila {60} 
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
* [Análisis de negocio: Caso Sakila](../img/qrs/09-insights-sakila.png)
* [SQL runner](../img/qrs/sql-interface.png)

---
@quizz{time_limit: 80}

# Pongamos a prueba lo aprendido
## Reaccciona en la llamada con el emoji de la respuesta correcta

quizz:
  - question:
      body: |
        Si ejecutas la siguiente consulta para analizar los ingresos del negocio:
        
        ```sql
        SELECT SUM(amount) AS total_ingresos
        FROM payment;
        ```
        
        ¿Qué métrica de negocio estás calculando?
      items:
        - option: "😇 El monto promedio cobrado por cada alquiler."
        - option: "😎 La cantidad total de transacciones realizadas."
        - option: "👍 El total de ingresos históricos acumulados por la tienda."
          correct: true
        - option: "😄 El ingreso máximo registrado en una sola transacción."
      feedback: |
        ¡Correcto! La función `SUM(amount)` suma todos los pagos registrados en la tabla `payment`, lo que representa el total de ingresos históricos del negocio.

  - question:
      body: |
        Para identificar transacciones de alto valor, ejecutamos la siguiente consulta:
        
        ```sql
        SELECT payment_id, amount
        FROM payment
        WHERE amount > 10.00;
        ```
        
        ¿Qué registros devolverá esta consulta?
      items:
        - option: "😇 Todos los pagos donde el monto cobrado es exactamente 10.00."
        - option: "😎 Únicamente los pagos con un monto estrictamente mayor a 10.00."
          correct: true
        - option: "👍 Los primeros 10 pagos registrados en la base de datos."
        - option: "😄 Todos los pagos ordenados de mayor a menor monto."
      feedback: |
        ¡Exacto! La condición `WHERE amount > 10.00` filtra las filas para mostrar solo aquellas transacciones cuyo monto de pago supera el valor de 10.00.

  - question:
      body: |
        Para analizar el catálogo de películas según su clasificación por edades, ejecutamos:
        
        ```sql
        SELECT rating, COUNT(*) AS total_peliculas
        FROM film
        GROUP BY rating;
        ```
        
        ¿Qué resultado produce esta consulta?
      items:
        - option: "😇 Muestra la película con mayor duración para cada clasificación."
        - option: "😎 Cuenta cuántas películas existen en total para cada clasificación de edad (rating)."
          correct: true
        - option: "👍 Filtra las películas para mostrar solo las que tienen una clasificación específica."
        - option: "😄 Muestra el promedio de precio de alquiler de todas las películas."
      feedback: |
        ¡Correcto! `GROUP BY rating` agrupa las películas por su clasificación, y `COUNT(*)` cuenta el número de películas pertenecientes a cada grupo.

  - question:
      body: |
        Para identificar el nombre de los clientes que realizaron cada pago, usamos la siguiente consulta:
        
        ```sql
        SELECT customer.first_name, payment.amount
        FROM payment
        INNER JOIN customer ON payment.customer_id = customer.customer_id;
        ```
        
        ¿Por qué es necesario usar `INNER JOIN` en esta consulta?
      items:
        - option: "😇 Porque los nombres de los clientes están en la tabla `customer` y el monto del pago en `payment`."
          correct: true
        - option: "😎 Porque queremos ordenar los resultados por el nombre del cliente."
        - option: "👍 Porque `INNER JOIN` elimina de forma automática los pagos duplicados."
        - option: "😄 Porque de lo contrario la base de datos no sabría cómo sumar los montos."
      feedback: |
        ¡Así es! Los datos de negocio están distribuidos en dos tablas: `customer` (información del cliente) y `payment` (transacciones). El `JOIN` las une usando la clave común `customer_id`.

  - question:
      body: |
        Analiza la siguiente consulta que busca identificar clientes de alto valor:
        
        ```sql
        WITH ingresos_clientes AS (
            SELECT customer_id, SUM(amount) AS total_gastado
            FROM payment
            GROUP BY customer_id
        )
        SELECT customer_id
        FROM ingresos_clientes
        WHERE total_gastado > 150;
        ```
        
        ¿Qué información devuelve esta consulta?
      items:
        - option: "😇 Los IDs de los clientes que gastaron más de 150 en una sola transacción."
        - option: "😎 Los IDs de los clientes cuyo gasto acumulado total en la tienda supera los 150."
          correct: true
        - option: "👍 El total acumulado de las ventas de la tienda cuando supera los 150."
        - option: "😄 Una lista de todos los clientes ordenados de mayor a menor gasto."
      feedback: |
        ¡Excelente! La CTE `ingresos_clientes` calcula primero el gasto total acumulado de cada cliente. Luego, la consulta principal filtra y muestra solo los IDs de aquellos clientes que han gastado más de 150 en total.

---

@include{path="../slides/farewell.md"}
