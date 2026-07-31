# Sprint 11 · Webinar · BI (Power BI) · Dashboards de Exportación Agrícola y Modelo Estrella 🍍📊

**Tema:** Análisis de Exportaciones Globales de Fruta y Modelado de Datos.

> En esta sesión nos pondremos en los zapatos de un Analista de Datos dentro de la corporación exportadora **"Frutícola del Sur"** 🌍.
> Conectaremos nuestros datos a Power BI, diseñaremos un modelo relacional tipo estrella ⭐ y crearemos un dashboard interactivo para presentar al comité directivo los resultados comerciales del periodo 2024-2025.

**Programa:** Data Analytics · **Sprint:** 11 · **Duración:** 100 min · **Modalidad:** Práctico

---

## 🍊 El Reto: Monitoreando el Sabor de Nuestras Exportaciones

¡Felicidades! Has sido contratado/a como Junior Data Analyst en **Frutícola del Sur**, una de las distribuidoras de fruta más importantes del continente. 🏪

El Director Comercial necesita preparar la presentación para la junta anual de accionistas. Quieren ver con total claridad cómo se están comportando las ventas globales, pero se enfrentan a un problema:
- Tienen los datos de ventas separados del catálogo de productos y de la lista de países destino.
- No saben con precisión qué categoría de fruta genera más valor monetario en relación al volumen enviado.
- Desconocen qué mercados (continentes/países) están pagando el mejor precio promedio por tonelada.

Tu misión es conectar tres archivos CSV alojados en la nube, diseñar un **Modelo Estrella** ⭐ y construir un **Dashboard Ejecutivo** de alto impacto para responder a estas preguntas estratégicas con la menor complejidad técnica posible.

---

## 🎯 Objetivos de la Sesión

Al finalizar esta clase práctica, serás capaz de:

1. **Importar múltiples archivos CSV** directamente desde la web (GitHub Raw) a Power BI.
2. **Revisar y ajustar tipos de datos** usando Power Query para asegurar que las claves relacionales funcionen.
3. **Entender el modelado de datos** conectando una tabla de hechos y dos dimensiones para formar un **Modelo Estrella**.
4. Crear **Métricas y KPIs clave** mediante fórmulas DAX básicas (Ingresos FOB, Volumen Total, Precio Promedio).
5. Diseñar **dashboards interactivos** centrados en la rentabilidad y estacionalidad del negocio agrícola.

---

## 📚 Diccionario de Datos y Origen

Para asegurar que todo el equipo trabaje con la misma fuente oficial, importaremos los archivos directamente desde el repositorio del bootcamp:

🌐 **Enlaces Raw para importar datos en Power BI:**
- **Dimensión Frutas:** `https://raw.githubusercontent.com/zyntonyson/data_repo/refs/heads/main/fruit_exportation/30-dim-frutas.csv`
- **Dimensión Países:** `https://raw.githubusercontent.com/zyntonyson/data_repo/refs/heads/main/fruit_exportation/30-dim-paises.csv`
- **Hechos Exportaciones:** `https://raw.githubusercontent.com/zyntonyson/data_repo/refs/heads/main/fruit_exportation/30-hechos-exportaciones.csv`

### 1️⃣ `30-dim-frutas` (Dimensión: Catálogo de Frutas)
| Columna | Tipo | Descripción |
| :--- | :--- | :--- |
| **`id_fruta`** | Texto | Identificador único de la fruta (Clave Primaria). Ej. `FRU-001`. |
| **`nombre_fruta`** | Texto | Nombre común de la fruta (Aguacate, Mango, Arándano, etc.). |
| **`categoria`** | Texto | Agrupación comercial (Tropicales, Berries, Cítricos). |
| **`variedad`** | Texto | Variedad botánica específica (Hass, Kent, Biloxi, etc.). |

### 2️⃣ `30-dim-paises` (Dimensión: Destinos Globales)
| Columna | Tipo | Descripción |
| :--- | :--- | :--- |
| **`id_pais`** | Texto | Identificador único del país (Clave Primaria). Ej. `PAI-001`. |
| **`pais_destino`** | Texto | Nombre del país comprador (Estados Unidos, España, Japón, etc.). |
| **`continente_destino`** | Texto | Continente de destino (América del Norte, Europa, Asia). |

### 3️⃣ `30-hechos-exportaciones` (Tabla de Hechos: Transacciones de Envío)
| Columna | Tipo | Descripción |
| :--- | :--- | :--- |
| **`id_transaccion`** | Texto | Identificador único de la operación de exportación. Ej. `EXP-2024-0001`. |
| **`fecha`** | Fecha | Fecha en que se realizó el embarque (Formato: `YYYY-MM-DD`). |
| **`id_fruta`** | Texto | Código de la fruta exportada (Clave Foránea). |
| **`id_pais`** | Texto | Código del país de destino (Clave Foránea). |
| **`toneladas`** | Decimal | Peso neto del cargamento medido en toneladas métricas (t). |
| **`precio_usd_tonelada`**| Decimal | Precio de venta pactado por cada tonelada de fruta (USD). |
| **`valor_fob_usd`** | Decimal | Valor neto de la exportación libre a bordo (FOB). Se calcula como: $Valor FOB = Toneladas \times Precio por Tonelada$. |

---

## 🛠️ Fase 1: Extracción y Preparación de Datos con Power Query

> 💡 **La analogía del lavadero de autos:** Imagina que Power Query es como un sistema automático de lavado de autos. Tus datos crudos entran sucios (con tipos de datos incorrectos o formatos inconsistentes) y salen limpios y pulidos listos para el show. En este caso, la limpieza es mínima porque la data viene estructurada, pero siempre debemos verificar los detalles.

1. **Obtener los datos desde la Web:**
   - En Power BI, haz clic en **Obtener datos (Get Data) > Web**.
   - Pega el enlace **Raw** de la tabla de hechos. Repite el proceso para las dimensiones.
   - Power BI detectará automáticamente el delimitador de coma (`,`) de los archivos CSV. Haz clic en **Transformar datos** para ingresar a la ventana de Power Query.

2. **Revisión de Tipos de Datos (Muy Importante):**
   - Asegúrate de que las columnas de ID (`id_fruta`, `id_pais`, `id_transaccion`) tengan asignado el tipo **Texto** (y no número entero), para evitar que Power BI intente sumarlas de forma automática.
   - En la tabla de hechos, valida que `fecha` sea de tipo **Fecha**, y que `toneladas`, `precio_usd_tonelada` y `valor_fob_usd` sean reconocidos como **Número decimal**.
   - Haz clic en **Cerrar y aplicar** en el menú de Inicio de Power Query para cargar los datos en el modelo de Power BI.

---

## ⭐ Fase 2: Construcción del Modelo Estrella

> 🌌 **La analogía del Sistema Solar:** En el modelado dimensional, la **Tabla de Hechos** es como nuestro Sol: masivo, en el centro del sistema, acumulando la gravedad de todas las métricas operativas (`toneladas`, `valor_fob_usd`). Las **Dimensiones** son como los planetas que orbitan a su alrededor. Las relaciones actúan como la gravedad que nos permite viajar desde una característica del planeta (como el continente del país o la categoría de la fruta) hasta los números del Sol de forma segura.

Dirígete a la vista de **Modelo** (diagrama de relaciones) y organiza tu estructura:
1. Ubica la tabla `30-hechos-exportaciones` al centro del lienzo.
2. Coloca las tablas `30-dim-frutas` y `30-dim-paises` a los costados o en la parte superior.
3. Conecta las tablas arrastrando los campos correspondientes:
   - Une `id_fruta` de `30-dim-frutas` con `id_fruta` de `30-hechos-exportaciones`.
   - Une `id_pais` de `30-dim-paises` con `id_pais` de `30-hechos-exportaciones`.
4. Verifica que ambas relaciones sean de **1 a Muchos (1:*)**, donde el extremo `1` esté en las dimensiones y el extremo `*` (Muchos) esté en la tabla de hechos. La dirección del filtro cruzado debe ser **Única**.

---

## 📈 Fase 3: Métricas Clave con Fórmulas DAX

Para evitar calcular métricas implícitas arrastrando columnas, crearemos medidas explícitas usando expresiones DAX. Es una buena práctica profesional que le dará orden a tu reporte.

1. **Ingresos FOB Totales (USD):**
   Suma de todos los montos de facturación FOB.
   $$\text{Total Ingresos FOB} = \sum (\text{valor\_fob\_usd})$$
   ```dax
   Total Ingresos FOB = SUM('30-hechos-exportaciones'[valor_fob_usd])
   ```

2. **Volumen Total Exportado (Toneladas):**
   Suma del peso neto de los embarques.
   ```dax
   Total Volumen (Tons) = SUM('30-hechos-exportaciones'[toneladas])
   ```

3. **Precio Promedio Real por Tonelada (USD/t):**
   Calcula la tarifa promedio ponderada dividiendo los ingresos totales entre el volumen total. Usamos `DIVIDE` para protegernos matemáticamente contra divisiones por cero ($0$).
   $$\text{Precio Promedio} = \frac{\text{Total Ingresos FOB}}{\text{Total Volumen (Tons)}}$$
   ```dax
   Precio Promedio Tonelada = DIVIDE([Total Ingresos FOB], [Total Volumen (Tons)], 0)
   ```

4. **Total de Embarques (Transacciones):**
   Cantidad total de registros de exportación completados.
   ```dax
   Total Embarques = COUNTROWS('30-hechos-exportaciones')
   ```

---

## 🎨 Fase 4: Propuesta Estructural del Dashboard

Te sugerimos diseñar un informe de dos páginas con una paleta de colores natural y armónica (tonos verdes forestales, naranjas y grises suaves):

### 📋 Página 1: Resumen Ejecutivo (Sales Performance)
*   **Fila de KPIs (Tarjetas):** Coloca el `Total Ingresos FOB` (formateado como moneda en USD), `Total Volumen (Tons)` y `Precio Promedio Tonelada` de forma destacada en la parte superior.
*   **Tendencia Temporal (Gráfico de Líneas):** Utiliza el campo `fecha` en el eje X (agrupado por Año y Mes) y `Total Ingresos FOB` en el eje Y. Esto permitirá observar visualmente la estacionalidad de las cosechas a lo largo del año.
*   **Rentabilidad por Producto (Gráfico de Barras Horizontales):** Muestra el `Total Ingresos FOB` cruzado por `nombre_fruta` de la tabla de dimensiones.
*   **Filtros Interactivos (Segmentadores):** Añade un segmentador por `categoria` de fruta (Cítricos, Berries, Tropicales) y otro por `Año`.

### 🗺️ Página 2: Distribución de Mercados (Market Share & Pricing)
*   **Participación de Mercado (Gráfico de Treemap o Anillos):** Muestra los `Total Ingresos FOB` distribuidos por `continente_destino`.
*   **Comparativa de Destinos (Matriz/Tabla):** Filas con `pais_destino`, columnas con `nombre_fruta`, y en los valores incluye el `Total Volumen (Tons)` y el `Precio Promedio Tonelada`. ¡Esto ayudará a detectar de inmediato qué países pagan mejor por cada tipo de fruta!
*   **Análisis de Precios (Gráfico de Dispersión):** Coloca el `Total Volumen (Tons)` en el eje X, el `Precio Promedio Tonelada` en el eje Y, y añade `nombre_fruta` en la Leyenda. Las frutas ubicadas en la esquina superior derecha serán aquellas de alto volumen y alto precio (nuestras joyas de la corona 💎).

---

## 🕵️‍♂️ Fase 5: Preguntas de Negocio para el Análisis de Datos

Un analista de datos no solo construye gráficos, sino que extrae conclusiones valiosas de ellos. Utiliza el dashboard interactivo que creaste para responder a las siguientes inquietudes del CEO:

1. **Duelo de Rentabilidad:** *¿Cuál es la fruta que tiene el precio promedio por tonelada más alto y a qué continente se exporta principalmente?*
2. **Estacionalidad Agrícola:** *¿En qué meses se concentra el mayor volumen de toneladas exportadas y a qué se debe ese comportamiento en la categoría de "Berries"?*
3. **Optimización de Canales:** *¿Hay países compradores de "Cítricos" que pagan un precio por tonelada notablemente mayor que otros? ¿Valdría la pena redireccionar carga hacia esos destinos?*
4. **Consistencia de Datos:** *¿Ves una relación directa entre el tamaño del cargamento (toneladas) y el precio unitario pactado por tonelada, o se mantiene estable por fruta?*

---

## 💪 Para seguir aprendiendo

En la medida que sigas practicando, elaborarás dashboards más complejos, con más tablas, gráficos y medidas. Te comparto un prompt con el que podrás generar un dashboard interactivo completo, además podrás personalizarlo según tus intereses y la temática que prefieras.

Copia y pega el siguiente prompt en tu IA favorita para crear un nuevo caso de análisis:

```text
Quiero que me ayudes a diseñar y estructurar un nuevo proyecto de dashboard interactivo. 

Por favor, genera un caso de negocio detallado basado en la siguiente temática: [ESCRIBE AQUÍ TU TEMA DE INTERÉS, por ejemplo: E-commerce de moda, Logística de última milla, Suscripciones de streaming, Ventas de una cadena de restaurantes].

Para este tema, proporciona la siguiente información estructurada de manera clara:

1. **Contexto de Negocio:**
   - Nombre de la empresa/institución ficticia y a qué se dedica.
   - Modelo de ingresos/operación y el desafío principal que enfrentan actualmente (ej. caída en retención, costos elevados, ineficiencia operativa).

2. **Necesidades del Stakeholder:**
   - Define el rol del stakeholder clave interesado en este dashboard (ej. Director de Operaciones, CMO, CFO).
   - Detalla qué decisiones estratégicas necesita tomar y qué preguntas cotidianas quiere resolver al interactuar con el reporte.

3. **Conjunto de Datos (Dataset Simulado):**
   - Propón un esquema de estrella (star schema) o copo de nieve (snowflake schema).
   - Define al menos una tabla de hechos (fact table) y de 2 a 3 tablas de dimensiones (dimension tables).
   - Para cada tabla, lista los campos clave con su tipo de dato (ej. Entero, Texto, Fecha, Decimal) y una breve descripción de lo que representa cada columna.
   - Los datos deben tener algun patrón interesante, evita generar unicamente aleatoriedad

4. **Recomendaciones de Diseño del Dashboard:**
  - Distribución o Layout sugerido para la interfaz (ej. dónde ubicar los filtros, los KPIs clave y los gráficos detallados).
  - 3 a 4 Indicadores Clave de Rendimiento (KPIs) numéricos principales que deben resaltar a primera vista.
  - Selección de gráficos recomendados (ej. gráfico de líneas para tendencias, barras para comparaciones, matriz para cohortes) justificando la elección de cada uno.
  - Filtros y segmentadores dinámicos indispensables para el usuario final.
  - El usuario usara Power Bi/ Tableau
  - Entre los analisis incluye:
    - Analisis temporal (yoy%)
    - Tendencias temporales (diarias, semanales, mensuales, anuales)
    - Comparaciones entre categorias (calculate/fixed)
    - Segmentación por grupos 
    - Analisis de cohortes

5. **Preguntas para el Análisis:**
   - Genera de 4 a 5 preguntas analíticas de negocio desafiantes que el estudiante deba responder explorando y cruzando los datos en su dashboard interactivo.
```
Finalmente pide que te genere el conjunto de datos descrito cada uno en formato csv
