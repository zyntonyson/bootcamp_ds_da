# Análisis de Métricas de Negocio con SQL: Catálogo e Interacción en "Readify" 📚✨

¡Hola, futura/o analista de datos! 👋 Bienvenido a este reto práctico. En esta sesión de 45 minutos nos pondremos en el rol de **Data Analysts** para **Readify**, una startup en crecimiento de distribución y recomendación de libros en línea. 

El equipo de Marketing y Adquisiciones necesita tomar decisiones estratégicas basadas en datos para lanzar su próximo boletín de recomendaciones y optimizar su catálogo. ¡Tu misión es ayudarles a responder sus preguntas de negocio utilizando **SQL** (en un motor SQLite)! 🚀

---

## 🧩 1. Contexto del negocio 🏢

**Readify** no solo vende libros en línea, sino que fomenta una comunidad activa de lectores donde los usuarios califican y escriben reseñas detalladas sobre sus lecturas. 

En los últimos meses, el equipo ha notado un incremento en las visitas pero quiere mejorar la **conversión y la retención de usuarios** mediante campañas hiper-personalizadas. Para ello, el Chief Content Officer (CCO) y el Director de Marketing necesitan entender en profundidad qué libros tienen mayor engagement, qué autores son los favoritos y qué editoriales nos ofrecen el contenido de mejor calidad percibida.

---

## 💡 2. Problemática general ⚠️

> **El reto del trimestre:** El presupuesto para campañas de email-marketing es limitado. Necesitamos identificar con precisión quirúrgica cuáles son los libros "estrella" (altamente valorados), los libros que más conversación generan (más reseñados) y entender si las editoriales con mayor volumen de publicaciones son también las que tienen las mejores calificaciones. 

---

## 🗄️ 3. Sobre los datos: Estructura y Diccionario 📊

Nuestra base de datos de **Readify** está estructurada en 5 tablas principales. Aquí tienes el mapa de cómo se relacionan entre sí:

```
  [authors]                  [publishers]
     │ (author_id)              │ (publisher_id)
     └───► [books] ◄────────────┘
             │ (book_id)
             ├───► [ratings]
             │ 
             └───► [reviews]
```

### 📖 Diccionario de Datos

#### Tabla 1: `books` (Catálogo de libros)
| Campo | Tipo de Dato | Descripción |
| :--- | :--- | :--- |
| **`book_id`** (PK) | `INTEGER` | Identificador único del libro. |
| `author_id` (FK) | `INTEGER` | Identificador del autor (relacionado con la tabla `authors`). |
| `title` | `VARCHAR` | Título del libro. |
| `num_pages` | `INTEGER` | Número de páginas del libro. |
| `publication_date` | `DATE` | Fecha de publicación del libro. |
| `publisher_id` (FK) | `INTEGER` | Identificador de la editorial (relacionado con la tabla `publishers`). |

#### Tabla 2: `authors` (Autores y autoras)
| Campo | Tipo de Dato | Descripción |
| :--- | :--- | :--- |
| **`author_id`** (PK) | `INTEGER` | Identificador único del autor o autora. |
| `author` | `VARCHAR` | Nombre completo del autor o autora. |

#### Tabla 3: `publishers` (Editoriales)
| Campo | Tipo de Dato | Descripción |
| :--- | :--- | :--- |
| **`publisher_id`** (PK) | `INTEGER` | Identificador único de la editorial. |
| `publisher` | `VARCHAR` | Nombre de la editorial. |

#### Tabla 4: `ratings` (Calificaciones de usuarios)
| Campo | Tipo de Dato | Descripción |
| :--- | :--- | :--- |
| **`rating_id`** (PK) | `INTEGER` | Identificador único de la calificación. |
| `book_id` (FK) | `INTEGER` | Identificador del libro calificado. |
| `username` | `VARCHAR` | Nombre de usuario que califica el libro. |
| `rating` | `INTEGER` | Calificación del 1 al 5. |

#### Tabla 5: `reviews` (Reseñas escritas)
| Campo | Tipo de Dato | Descripción |
| :--- | :--- | :--- |
| **`review_id`** (PK) | `INTEGER` | Identificador único de la reseña. |
| `book_id` (FK) | `INTEGER` | Identificador del libro reseñado. |
| `username` | `VARCHAR` | Nombre del usuario que escribe la reseña. |
| `text` | `TEXT` | Contenido de la reseña escrita. |

---

## 🗣️ 4. Preguntas clave de los Stakeholders 💬

Para enfocar tu análisis, el equipo de marketing te ha planteado las siguientes preguntas clave:
1. ¿Cuáles son los libros más largos del catálogo y quiénes los escribieron?
2. ¿Qué libros publicados recientemente (de 2018 en adelante) tienen baja cantidad de páginas para una campaña de "Lecturas Rápidas"?
3. ¿Cuáles son las editoriales que reciben el mayor número de calificaciones y qué calificación promedio tienen?
4. ¿Qué autores generan mayor debate en la plataforma (mayor cantidad de reseñas escritas)?
5. ¿Qué libros tienen una extensión superior al promedio general de nuestra base de datos?
6. ¿Cuáles son los libros cuya calificación promedio es estrictamente mayor que el promedio de calificaciones de toda la plataforma?

---

## 📏 5. KPIs de Referencia para el Negocio 📈

Antes de escribir código, es útil tener en el radar las métricas que definen el desempeño:

| KPI | Descripción | Métrica SQL sugerida |
| :--- | :--- | :--- |
| **Extensión Promedio** | Promedio de páginas de los libros | `AVG(num_pages)` |
| **Calificación Promedio (Global)**| Promedio general de satisfacción | `AVG(rating)` |
| **Volumen de Engagement** | Cantidad total de calificaciones y reseñas escritas | `COUNT(rating_id)` y `COUNT(review_id)` |
| **Popularidad del Autor** | Cantidad de valoraciones acumuladas por autor | `COUNT(rating_id) GROUP BY author_id` |

---

## 🔍 6. Guía de Trabajo y Queries SQL Propuestos (45 min) ⏱️

¡Es hora de la acción! A continuación, se presentan las consultas organizadas de menor a mayor complejidad para resolver las inquietudes del negocio.

### 🥉 Nivel 1: Consultas básicas con `LIMIT` y `ORDER BY`

#### 🎯 Reto 1: Identificar los 5 libros más largos del catálogo
* **Objetivo de negocio:** El equipo de logística quiere estimar el espacio físico e impresión de los libros más extensos, y marketing quiere saber si debe promocionarlos para lectores de "largo aliento".

```sql
-- Tu Query aquí
SELECT 
    title, 
    num_pages 
FROM books 
ORDER BY num_pages DESC 
LIMIT 5;
```

---

### 🥈 Nivel 2: Filtrado selectivo con `WHERE`

#### 🎯 Reto 2: Filtrar libros recientes (desde 2018) con menos de 250 páginas
* **Objetivo de negocio:** Campaña de *micro-learning* y lecturas rápidas para captar la atención de usuarios ocupados durante el fin de semana.

```sql
-- Tu Query aquí
SELECT 
    title, 
    num_pages, 
    publication_date 
FROM books 
WHERE publication_date >= '2018-01-01' 
  AND num_pages < 250
ORDER BY num_pages ASC;
```

---

### 🥇 Nivel 3: Cruzando datos con `JOINs` y agrupamientos (`GROUP BY`)

#### 🎯 Reto 3: Desempeño de calidad y volumen por Editorial
* **Objetivo de negocio:** Identificar qué editoriales nos proveen los libros más exitosos (mayor calificación promedio) y con mayor interacción (volumen de calificaciones).

```sql
-- Tu Query aquí
SELECT 
    p.publisher,
    COUNT(r.rating_id) AS total_ratings,
    ROUND(AVG(r.rating), 2) AS avg_rating
FROM books b
JOIN publishers p ON b.publisher_id = p.publisher_id
JOIN ratings r ON b.book_id = r.book_id
GROUP BY p.publisher
ORDER BY avg_rating DESC, total_ratings DESC;
```

#### 🎯 Reto 4: Los autores que generan más conversación (Reseñas escritas)
* **Objetivo de negocio:** Identificar autores que generan debate y comunidad para invitarlos a eventos en vivo o webinars virtuales de Readify.

```sql
-- Tu Query aquí
SELECT 
    a.author,
    COUNT(rev.review_id) AS total_reviews
FROM books b
JOIN authors a ON b.author_id = a.author_id
JOIN reviews rev ON b.book_id = rev.book_id
GROUP BY a.author
ORDER BY total_reviews DESC
LIMIT 5;
```

---

### 🏆 Nivel 4: Decisiones avanzadas usando Subconsultas (`Subqueries`)

#### 🎯 Reto 5: Libros que superan el tamaño promedio del catálogo
* **Objetivo de negocio:** Comparar libros individuales contra la métrica global del negocio sin necesidad de calcular el promedio a mano y reintroducirlo en el query.

```sql
-- Tu Query aquí
SELECT 
    title, 
    num_pages
FROM books
WHERE num_pages > (SELECT AVG(num_pages) FROM books)
ORDER BY num_pages DESC;
```

#### 🎯 Reto 6: Los "hits" de la plataforma (Calificación promedio > Calificación promedio global)
* **Objetivo de negocio:** Encontrar los libros que son evaluados por encima de la media de toda la plataforma para destacarlos de forma prioritaria en el carrusel principal de la app.

```sql
-- Tu Query aquí
SELECT 
    b.title,
    ROUND(AVG(r.rating), 2) AS avg_book_rating
FROM books b
JOIN ratings r ON b.book_id = r.book_id
GROUP BY b.book_id, b.title
HAVING AVG(r.rating) > (SELECT AVG(rating) FROM ratings)
ORDER BY avg_book_rating DESC;
```

---

## 💡 7. Insights esperados del Estudiante 🧠

Después de ejecutar estas consultas, un analista de datos junior debería ser capaz de estructurar observaciones como las siguientes:

* *"Aunque la editorial X tiene el mayor volumen de libros, su calificación promedio apenas roza las 3.2 estrellas, mientras que la editorial Y, con solo 3 títulos en la plataforma, ostenta un promedio de 4.8 estrellas con alta participación de usuarios."*
* *"Los libros publicados después de 2018 tienden a ser en promedio un 15% más cortos en número de páginas que los clásicos anteriores al 2010, lo que valida la hipótesis de que el contenido moderno se adapta a lecturas más breves."*

---

## 🚀 8. Recomendaciones accionables para el Stakeholder 🎯

Basados en el análisis anterior, aquí hay algunas propuestas prácticas para el negocio:

1. **Ajuste de Adquisición:** Priorizar el catálogo de las editoriales que tienen un rating promedio superior a 4.2 y suspender promociones con aquellas por debajo de 3.0.
2. **Campañas Temáticas:** Crear una sección destacada en la app llamada *"Lecturas Rápidas del Momento"*, alimentada automáticamente por la consulta del Reto 2.
3. **Engagement de Comunidad:** Enviar cupones de descuento personalizados para los libros de los autores identificados en el Reto 4, ya que son los que provocan que los usuarios interactúen escribiendo opiniones completas.

---

### 📝 Reporte de Resultados
¡Felicidades por completar el taller de SQL! Guarda tus consultas en un script `.sql` o Jupyter Notebook, y anota tus 3 insights principales para presentárselos a los stakeholders en el canal de discusión de la comunidad. 📊🤓
