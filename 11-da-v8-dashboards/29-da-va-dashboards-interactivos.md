# Sprint 11 · Webinar · BI (Power BI + Tableau) · Dashboards Interactivos y Customer Journey ☕📊

**Tema:** Análisis del efecto de Campañas de Marketing y el Viaje del Usuario (Customer Journey). 

> En esta sesión nos pondremos en los zapatos de un Analista de Datos y jugaremos con un dataset real provisto originalmente por Starbucks. 
> Crearemos nuestro modelo relacional, entenderemos a nuestros usuarios, y armaremos tres páginas de dashboard interactivas centrándonos en el **rendimiento comercial, engagement y cohortes**.

**Programa:** Data Analytics · **Sprint:** 11 · **Duración:** 100 min · **Modalidad:** Práctico

---

## ☕ El Reto: Entendiendo a nuestros "Coffee Lovers"

Imagina que acabas de ser contratado como el nuevo flamante Junior Data Analyst en una reconocida cadena mundial de cafeterías. 🏪 

El equipo de Marketing acaba de terminar una agresiva prueba de 30 días en la aplicación móvil, enviando diferentes tipos de ofertas a los clientes: promociones BOGO (*Buy One Get One* o 2x1), descuentos y simples anuncios informativos. 

El problema es que el equipo directivo está a ciegas 🫣:
- No saben qué ofertas son las más efectivas.
- No saben qué segmento demográfico (edad, ingresos) responde mejor.
- Y lo más importante: **¿Los usuarios compran porque vieron la oferta o iban a comprar de todos modos?**

Tu misión es transformar tres archivos JSON alojados en la nube en un **Modelo Estrella** brillante ⭐ y construir un **Dashboard Ejecutivo** interactivo que responda a estas inquietudes.

---

## 🎯 Objetivos de la Sesión

Al finalizar esta clase práctica, serás capaz de:

1. **Importar datos estructurados en JSON** directamente desde la web (GitHub) a Power BI.
2. **Transformar atributos complejos** (listas y registros anidados) utilizando Power Query.
3. **Entender el modelado de datos** conectando una tabla de hechos y dos dimensiones para formar un **Modelo Estrella**.
4. Crear **Métricas y KPIs clave** con expresiones DAX (Tasa de Conversión, Ingresos Totales).
5. Diseñar **dashboards interactivos** para analizar embudos de conversión (Enviado ➡️ Visto ➡️ Completado).

---

## 📚 Diccionario de Datos y Origen

Para este proyecto, conectaremos Power BI directamente al repositorio en GitHub. 

> ⚠️ **¡Atención!** Siempre usa el enlace **Raw** de GitHub para importar a Power BI. Si usas el enlace normal web (el que dice `/blob/`), Power BI intentará descargar el código HTML de la página web de GitHub en lugar del texto JSON.

🌐 **Enlaces Raw para importar datos:**
- `portfolio`: `https://raw.githubusercontent.com/salgha/starbucks-customers-segmentation/master/data/portfolio.json`
- `profile`: `https://raw.githubusercontent.com/salgha/starbucks-customers-segmentation/master/data/profile.json`
- `transcript`: `https://raw.githubusercontent.com/salgha/starbucks-customers-segmentation/master/data/transcript.json`

### 1️⃣ `portfolio` (Dimensión: Campañas de Marketing)
| Columna | Descripción |
| :--- | :--- |
| **`id`** | El identificador único de la oferta (String). |
| **`offer_type`** | Tipo de oferta: `bogo` (2x1), `discount` (descuento) o `informational` (solo anuncio). |
| **`difficulty`** | Gasto mínimo requerido para completar la oferta (dólares). |
| **`reward`** | Recompensa otorgada al completar la oferta (dólares). |
| **`duration`** | Tiempo en días que la oferta es válida antes de caducar. |
| **`channels`** | Por dónde se envió. Viene como una *Lista* (`web`, `email`, `mobile`, `social`). |

### 2️⃣ `profile` (Dimensión: Clientes)
| Columna | Descripción |
| :--- | :--- |
| **`id`** | El identificador único del cliente (String). |
| **`age`** | Edad del cliente. (⚠️ *Tip: ¡El valor 118 indica N/A!*). |
| **`gender`** | Género del cliente (`M`, `F`, `O` o nulo si no se especificó). |
| **`income`** | Ingreso anual del cliente en dólares. |
| **`became_member_on`** | Fecha de inicio de cuenta (Formato: YYYYMMDD). |

### 3️⃣ `transcript` (Tabla de Hechos: Eventos de la App)
| Columna | Descripción |
| :--- | :--- |
| **`person`** | ID del cliente. |
| **`event`** | Qué ocurrió: `offer received`, `offer viewed`, `transaction`, `offer completed`. |
| **`value`** | Viene como un *Registro (Record)* anidado. Contiene IDs de la oferta y montos de compra. |
| **`time`** | Tiempo en horas desde el inicio de la prueba de 30 días. |

---

### Fase 1: Extracción y Transformación con Power Query 🕸️
Nuestro principal objetivo aquí es conectar los datos e interpretar los JSON anidados:

1.  **Obtener los datos web:** 
    *   Ir a *Obtener Datos > Web* y pegar el enlace Raw. Power BI abrirá Power Query en formato "Lista".
    *   Hacer clic en el botón **"A la tabla"** (To Table) en el menú Convertir (dejando los valores predeterminados sin delimitador).


2.  **Limpiar la tabla `portfolio`:**
    *  *PowerBi* debe reconocer la estructura de los datos y expandir las columnas. Aquí podras ver que:
        * Channels fue expandido a varios renglones repitiendo el resto de los datos. 
        
3.  **Limpiar la tabla `profile`:**
    *   Llevar la lista JSON a tabla .
    *   **Fechas ocultas:** La columna `became_member_on` viene como un número abstracto (`20171111`). Para que Power BI lo entienda, selecciona la columna, ve a la pestaña superior **"Agregar columna" (Add Column)** *(¡Asegúrate de estar en la ventana separada del Editor de Power Query, no en la principal!)*, y haz clic en el botón **"Columna a partir de ejemplos" (Column From Examples) > "A partir de la selección"**. En la primera celda vacía escribe a mano el formato correcto (ej. `2017-11-11`), presiona Enter, y Power Query creará inteligentemente el patrón para el resto de la tabla. ¡Recuerda borrar la columna original numérica!
    *   **Edades imposibles:** Observarás que en la columna `age` aparecen clientes con ¡118 años! En este dataset, 118 es un marcador de falta de datos (N/A). Usa "Reemplazar Valores" en la columna `age` para cambiar el 118 por *null* (nulo) y evitar que tu promedio de edad en el dashboard se arruine.

4.  **Limpiar la tabla `transcript`:**
    *   Este archivo tiene una trampa clásica en la vida real. La columna `value` es un diccionario JSON que en algunos eventos trae `{"amount": 18.52}`, en otros `{"offer id": "fafd..."}` y en otros `{"offer_id": "fafd...", "reward": 2}`.
    *   Power Query extraerá automáticamente cuatro nuevas columnas: `amount` (monto), `reward` (recompensa), `offer id` y `offer_id`.
    *   **Fusionar columnas:** Como tenemos dos columnas para el nombre de la oferta (`offer_id` y `offer id`) que nunca se llenan al mismo tiempo, el método más seguro a prueba de errores es crear una condición lógica. Ve a **Agregar Columna > Columna Condicional** (Conditional Column). Nómbrala `ID_Campaña_Final`. Configura la regla así: *Si `[offer_id]` no es igual a `null`*, entonces > seleccionar "Seleccionar Columna" > devolver `[offer_id]`. *De lo contrario* > "Seleccionar Columna" > devolver `[offer id]`.


### Fase 2: Construcción del Modelo Estrella ⭐
Al presionar "Cerrar y aplicar", conectaremos el modelo de la vista de diagrama:
1.  **`Transcript` al Centro (Tabla de Hechos):** Aquí ocurren los eventos y donde reside el campo de ventas que acabamos de transformar (`amount`).
2.  **`Profile` conectado a `transcript` (Dimensión de Cliente):** Relación de "1 a Muchos" arrastrando el campo `id` de profile hacia `person` de transcript.
3.  **`Portfolio` conectado a `transcript` (Dimensión de Campaña):** Relación de "1 a Muchos" arrastrando el campo `id` de portfolio hacia la columna fusionada *ID_de_Campana* en transcript. (*Ambas relaciones deben estar activas y con dirección de cruce sencilla*).
4.  **Ajuste temporal (Nueva Columna calculada):** Aunque la tabla Hechos tiene la columna `time`, está medida en horas continuas (0 a 714). Para saber el número de día, crearemos y estructuraremos una nueva columna calculada paso a paso. En la vista de Datos, selecciona la tabla `transcript`, ve a **Herramientas de tablas > Nueva columna** y usa la siguiente lógica:
    *   **Fórmula DAX final a pegar:** `Dia_Del_Experimento = RIGHT("0" & ROUNDDOWN(transcript[time] / 24, 0), 2)`


### Fase 3: Medidas DAX Recomendadas (Métricas) 📈
Calcularemos los números vitales para colocar en nuestras tarjetas ejecutivas:

*   **`Total Ingresos`**: `SUM(transcript[amount])`
*   **`Cargas Promocionales` (Ofertas enviadas)**: `CALCULATE(COUNTROWS(transcript), transcript[event] = "offer received")`
*   **`Interacciones Confirmadas` (Vistas)**: `CALCULATE(COUNTROWS(transcript), transcript[event] = "offer viewed")`
*   **`Embudo Completo`**: `CALCULATE(COUNTROWS(transcript), transcript[event] = "offer completed")`
*   **`Total Transacciones (Órdenes netas)`**: `CALCULATE(COUNTROWS(transcript), transcript[event] = "transaction")`
*   **`ARPU` (Ingreso por Usuario)**: Dividiremos la medida `Total Ingresos` entre `DISTINCTCOUNT(transcript[person])`.

### Fase 4: Propuesta Estructural del Dashboard 🎨
Sugerimos desarrollar tres vistas claras que simulen una entrega profesional:

1.  **Vista 1: Visión General (Executive Overview)**
    *   *Fila superior:* Medidas DAX en "Tarjetas" (Total Ingresos, ARPU, Total Vistas).
    *   *Panel Izquierdo:* Dona gráfica distribuyendo a los usuarios (`gender`) para entender el piso de la campaña. Dispersión cruzando `age` contra `income` (filtro interactivo).
    *   *Panel Principal:* Gráfico de áreas apiladas monitoreando los ingresos a lo largo de los casi 30 días usando nuestra nueva columna calculada `Dia_Del_Experimento`.
2.  **Vista 2: Rendimiento Marketing**
    *   Filtros nativos (Segmentadores) por el campo `offer_type` (BOGO vs Discount).
    *   Matriz visual de Tabla: Por fila agregaremos el `id` (o un nombre inventado al campo portfolio) y agregaremos la medida Total Ingresos y la medida Embudo Completo para ranquear cuál generó más ganancia real.
3.  **Vista 3: El Viaje del Usuario (Funnel)**
    *   Un simple pero poderoso gráfico en forma de Embudo (Funnel chart original de Power BI). Usaremos el campo texto `event` a nivel de Categoría y un simple recuento de ID como valor. Así veremos si el 90% recibe publicidad pero solo el 20% la lee y el 5% la cobra.

### Fase 5: Preguntas de Negocio que daremos respuesta 🕵️‍♂️
De nada sirve armar el embudo visual si no podemos guiar las decisiones gerenciales:
1.  **Duelo de Ofertas:** *Al usar el dashboard, ¿fue más rentable regalarles café extra (BOGO 2x1) o simplemente quitar precio (Discount)?*
2.  **Segmentación Oculta:** *¿Ves una correlación entre clientes femeninos y masculinos con el nivel de completitud de los retos basados en dólares?*
3.  **Fidelización:** *¿El ARPU asciende dependiendo si el cliente inició su cuenta en años más antiguos en relación a quién descargó la app hace un mes?*
4.  **Journey Analytics:** *¿Hay clientes fantasmas? Es decir, aquellos que en la matriz de facturación hicieron un "offer completed" pero no existe data de un "offer viewed" intermedio.*

---

> 🚀 **¿Toda esta data cruda asusta? ¡Para nada!** Transforma esos JSON abriendo Power BI. ¡Vamos a desatar el poder del Customer Journey!
