# Sprint 11 ·Crea dashboards interactivos para stakeholders 

---

**Tema:** Análisis de la Coexistencia y Desplazamiento Comercial: Tiendas Pequeñas vs. Grandes Supermercados como Indicadores de Gentrificación en el Modelado Dimensional.


## 🏪 El Reto: Gentrificación y el Comercio Local

**IPDUS**, es un organismo gubernamental encargado de monitorear la salud comercial y la inclusión social en las zonas urbanas de rápido crecimiento.

El Director de Desarrollo Urbano e Inclusión Comercial necesita presentar un diagnóstico integral al cabildo de la ciudad. Quieren evaluar cómo la proliferación de grandes cadenas de supermercados y el encarecimiento de los alquileres están afectando a los comercios locales y de barrio (las tradicionales "tienditas", fruterías, carnicerías y panaderías). Sin embargo, se enfrentan a desafíos clave:
- Tienen los registros de facturación y visitas comerciales desconectados del censo geográfico de barrios y del catálogo detallado de comercios.
- No saben con precisión si el aumento en la renta promedio por metro cuadrado (`alquiler_promedio_m2`) expulsa directamente a los comercios pequeños o si estos logran coexistir con las grandes superficies.
- Desconocen qué barrios muestran signos de gentrificación comercial acelerada (pérdida acelerada de pequeños comercios y dominio absoluto de franquicias o supermercados multinacionales).
- Necesitan evaluar la tasa de supervivencia de los comercios tradicionales (cohortes): una vez que un gran supermercado se instala en un barrio, ¿cuántos meses logran sobrevivir las tiendas de barrio circundantes?

Tu misión es estructurar sus datos en un **Modelo Estrella** ⭐, implementar cálculos dinámicos en DAX y diseñar un **Dashboard Ejecutivo** de alto impacto para responder a estas preguntas con claridad y precisión técnica en Power BI.

---

## 🎯 Objetivos de la Sesión

1. **Importar y limpiar archivos CSV** con información comercial y urbana estructurada en Power BI.
2. **Establecer relaciones consistentes** entre una tabla de hechos y dos tablas de dimensiones en un **Modelo Estrella**.
3. **Generar una dimensión de tiempo dinámica (`dim_fecha`)** usando fórmulas DAX para el análisis temporal.
4. **Calcular métricas avanzadas en DAX** incluyendo sumas, promedios, participación porcentual (%) y fórmulas de inteligencia de tiempo (YoY).
5. **Implementar un análisis de cohortes** para medir la supervivencia o retención de las tiendas pequeñas en los barrios analizados.
6. **Crear visualizaciones profesionales** en Power BI para el análisis de tendencias geográficas y comerciales.

---

## 📚 Diccionario de Datos 

Para este webinar utilizaremos un set de datos   el monitoreo mensual de la actividad comercial en los barrios de la ciudad en el periodo 2023-2025.

### 1️⃣ [32-hechos-comercios.csv](file:///c:/Users/roman/Documents/proyectos/tripleten/bootcamp_ds_da/11-da-v8-dashboards/32-hechos-comercios.csv) (Tabla de Hechos)
Registra mensualmente el desempeño financiero, la afluencia y el costo de alquiler por cada establecimiento comercial monitoreado.

| Columna | Tipo de Dato (Origen) | Tipo de Dato (BI Target) | Descripción |
| :--- | :--- | :--- | :--- |
| `id_registro` | Texto / String | Texto | Clave Primaria (PK) única del registro mensual (Ej: `REG000001`). |
| `fecha_registro` | Texto / String | Fecha (Date) | Fecha del cierre de mes reportado (Ej: `2023-01-31`). *Requiere conversión*. |
| `id_barrio` | Texto / String | Texto | Clave Foránea (FK) que conecta con `dim_barrios` (Ej: `BAR004`). |
| `id_comercio` | Texto / String | Texto | Clave Foránea (FK) que conecta con `dim_comercios` (Ej: `COM025`). |
| `ventas_mensuales_usd`| Entero / Numérico | Entero / Moneda (USD) | Ventas estimadas del comercio en el mes reportado (Ej: `12500`). |
| `alquiler_promedio_m2`| Flotante / Numérico | Flotante / Moneda (USD) | Costo promedio mensual de alquiler por metro cuadrado en la zona comercial (Ej: `24.50`). |
| `afluencia_peatonal` | Entero / Numérico | Entero | Número estimado de clientes/transeúntes que visitaron el comercio en el mes (Ej: `4500`). |
| `costo_operativo_usd` | Entero / Numérico | Entero / Moneda (USD) | Costos fijos y variables declarados de operación del comercio (Ej: `3800`). |
| `porcentaje_descuento_renta`| Flotante / Numérico| Porcentaje (%) | Porcentaje de subsidio o descuento en el alquiler otorgado por programas locales (Ej: `0.10` -> `10%`). |

### 2️⃣ [32-dim-barrios.csv](file:///c:/Users/roman/Documents/proyectos/tripleten/bootcamp_ds_da/11-da-v8-dashboards/32-dim-barrios.csv) (Dimensión Barrios)
Contiene información socioeconómica y geográfica de las zonas o distritos analizados.

| Columna | Tipo de Dato (Origen) | Tipo de Dato (BI Target) | Descripción |
| :--- | :--- | :--- | :--- |
| `id_barrio` | Texto / String | Texto | Clave Primaria (PK) del barrio (Ej: `BAR001`). Sin duplicados. |
| `nombre_barrio` | Texto / String | Texto / Categoría Geográfica | Nombre del barrio (Ej: `San Rafael`, `La Condesa`, `Polanco`). |
| `nivel_socioeconomico`| Texto / String | Texto | Nivel de ingresos predominante en el barrio (Ej: `Bajo`, `Medio`, `Alto`). |
| `estatus_gentrificacion`| Texto / String | Texto | Clasificación urbana actual (Ej: `Tradicional`, `En Transición`, `Gentrificado`). |
| `poblacion_estimada` | Entero | Entero | Cantidad de habitantes censados en el barrio (Ej: `15000`). |
| `distancia_centro_km` | Flotante | Decimal / Número | Distancia en kilómetros al centro histórico o financiero de la ciudad (Ej: `3.2`). |

### 3️⃣ [32-dim-comercios.csv](file:///c:/Users/roman/Documents/proyectos/tripleten/bootcamp_ds_da/11-da-v8-dashboards/32-dim-comercios.csv) (Dimensión Comercios)
Contiene las características intrínsecas de los establecimientos comerciales registrados.

| Columna | Tipo de Dato (Origen) | Tipo de Dato (BI Target) | Descripción |
| :--- | :--- | :--- | :--- |
| `id_comercio` | Texto / String | Texto | Clave Primaria (PK) del comercio (Ej: `COM001`). Sin duplicados. |
| `nombre_comercio` | Texto / String | Texto | Nombre de fantasía o razón social (Ej: `Abarrotes La Unión`, `Supermercado Express`). |
| `tipo_escala` | Texto / String | Texto | Escala del negocio (Ej: `Pequeño Comercio`, `Gran Supermercado`). |
| `categoria_negocio` | Texto / String | Texto | Rubro comercial (Ej: `Abarrotes`, `Verdulería`, `Carnicería`, `Supermercado General`). |
| `origen_capital` | Texto / String | Texto | Procedencia del capital (Ej: `Local/Familiar`, `Franquicia Nacional`, `Multinacional`). |
| `superficie_m2` | Entero | Entero | Área física total del local en metros cuadrados (Ej: `45`). |

---

## 🛠️ Desglose de Tareas del Analista

Para construir este sistema analítico, realizaremos las siguientes tareas estructuradas paso a paso en Power BI:

### 🧹 Paso 1: Limpieza e Importación de Datos
- **Carga de Archivos**: Cargar las tres tablas dimensionales y de hechos desde sus orígenes CSV en Power Query.
- **Configuración de Tipos**:
  - Asegurar que `fecha_registro` se convierta de Texto a **Fecha (Date)**.
  - Asegurar que los IDs (`id_registro`, `id_barrio`, `id_comercio`) estén configurados como **Texto** (no como números) para prevenir agregaciones accidentales.
  - Asignar formato de moneda (USD) a `ventas_mensuales_usd`, `alquiler_promedio_m2` y `costo_operativo_usd`.
  - Asegurar que `porcentaje_descuento_renta` se lea como decimal y formatearlo como **Porcentaje (%)**.
- **Integridad y Duplicados**: Asegurarse de que no existan duplicados en las claves primarias de `dim_barrios` y `dim_comercios`. Justificar la eliminación de nulos si existieran.

### 📅 Paso 2: Creación de la Tabla Calendario (`dim_fecha`)
Utilizando DAX en Power BI, crearemos una tabla calendario de rango dinámico basada en la tabla de hechos para controlar la temporalidad del análisis.

```dax
dim_fecha = 
VAR FechaMin = MIN('32-hechos-comercios'[fecha_registro])
VAR FechaMax = MAX('32-hechos-comercios'[fecha_registro])
RETURN
ADDCOLUMNS(
    CALENDAR(FechaMin, FechaMax),
    "Año", YEAR([Date]),
    "Mes", FORMAT([Date], "MMMM"),
    "Mes Número", MONTH([Date]),
    "Año-Mes", FORMAT([Date], "YYYY-MM"),
    "Trimestre", "Q" & FORMAT([Date], "Q"),
    "Año-Trimestre", FORMAT([Date], "YYYY") & "-Q" & FORMAT([Date], "Q"),
    "Dia Semana", FORMAT([Date], "dddd"),
    "Es Fin Semana", IF(WEEKDAY([Date], 2) > 5, TRUE, FALSE)
)
```
> ⚠️ **Configuración Crítica:** Recuerda marcar esta tabla como **Tabla de fechas (Mark as date table)** seleccionando la columna `Date` como su clave primaria. ¡Esto garantizará que las funciones de Inteligencia de Tiempo de DAX funcionen a la perfección!

### 🧩 Paso 3: Modelado de Datos (Esquema Estrella)
- Coloca la tabla de hechos `32-hechos-comercios` en el centro del lienzo del modelo.
- Organiza a su alrededor las tres tablas dimensionales (`dim_barrios`, `dim_comercios`, `dim_fecha`).
- Establece las siguientes relaciones de **1 a Muchos (1:*)** con dirección de filtro **Única (Single)**:
  - Conectar `dim_barrios[id_barrio]` ➔ `32-hechos-comercios[id_barrio]`.
  - Conectar `dim_comercios[id_comercio]` ➔ `32-hechos-comercios[id_comercio]`.
  - Conectar `dim_fecha[Date]` ➔ `32-hechos-comercios[fecha_registro]`.

---

## 📈 Paso 4: Fórmulas y Medidas DAX

Crearemos medidas explícitas para estructurar los indicadores clave en nuestro dashboard interactivo.

### 4.1 Medidas Base 📊
- **Ventas Totales (USD):** Suma total de las ventas registradas.
  ```dax
  Ventas Totales = SUM('32-hechos-comercios'[ventas_mensuales_usd])
  ```
- **Cantidad de Comercios Activos:** Número único de comercios que registran operaciones en el período.
  ```dax
  Comercios Activos = DISTINCTCOUNT('32-hechos-comercios'[id_comercio])
  ```
- **Alquiler Promedio por m² (USD):** Costo de alquiler promedio simple por metro cuadrado.
  ```dax
  Alquiler Promedio m2 = AVERAGE('32-hechos-comercios'[alquiler_promedio_m2])
  ```
- **Afluencia Peatonal Total:** Suma total de visitas estimadas.
  ```dax
  Afluencia Total = SUM('32-hechos-comercios'[afluencia_peatonal])
  ```

### 4.2 Medidas con Contexto de Filtro Modificado (CALCULATE) 🔬
Estas medidas nos permiten conocer la participación de un segmento específico respecto al total global de ventas o segmentar según la escala de los comercios.
- **Ventas de Grandes Supermercados:**
  ```dax
  Ventas Grandes Supermercados = 
  CALCULATE(
      [Ventas Totales], 
      'dim_comercios'[tipo_escala] = "Gran Supermercado"
  )
  ```
- **Ventas de Pequeños Comercios:**
  ```dax
  Ventas Pequeños Comercios = 
  CALCULATE(
      [Ventas Totales], 
      'dim_comercios'[tipo_escala] = "Pequeño Comercio"
  )
  ```
- **% Participación Ventas de Pequeños Comercios:**
  ```dax
  % Participacion Ventas Pequenos Comercios = 
  DIVIDE(
      [Ventas Pequeños Comercios], 
      CALCULATE([Ventas Totales], ALL('dim_comercios'[tipo_escala])), 
      0
  )
  ```
- **Alquiler Promedio en Barrios Gentrificados:**
  ```dax
  Alquiler Promedio Gentrificado = 
  CALCULATE(
      [Alquiler Promedio m2], 
      'dim_barrios'[estatus_gentrificacion] = "Gentrificado"
  )
  ```

### 4.3 Inteligencia de Tiempo (YoY & CALCULATE) ⏳
Para evaluar si el volumen de ventas y el costo de alquiler residencial/comercial está creciendo interanualmente en comparación con períodos anteriores:
- **Ventas YTD (Year-to-Date):**
  ```dax
  Ventas YTD = TOTALYTD([Ventas Totales], 'dim_fecha'[Date])
  ```
- **Ventas del Año Anterior (Prior Year - PY):**
  ```dax
  Ventas PY = CALCULATE([Ventas Totales], SAMEPERIODLASTYEAR('dim_fecha'[Date]))
  ```
- **Crecimiento de Ventas YoY (%):**
  ```dax
  Crecimiento Ventas YoY % = 
  DIVIDE(
      [Ventas YTD] - [Ventas PY], 
      [Ventas PY], 
      0
  )
  ```
- **Alquiler Promedio del Año Anterior (PY):**
  ```dax
  Alquiler PY = CALCULATE([Alquiler Promedio m2], SAMEPERIODLASTYEAR('dim_fecha'[Date]))
  ```
- **Crecimiento de Renta YoY (%):**
  ```dax
  Crecimiento Renta YoY % = 
  DIVIDE(
      [Alquiler Promedio m2] - [Alquiler PY], 
      [Alquiler PY], 
      0
  )
  ```

### 4.4 Columnas Calculadas para Cohortes (Análisis de Supervivencia de Tiendas) 🧩
Queremos ver cuántos meses siguen registrando actividad comercial las tiendas locales desde su primer registro en la base de datos (lo que permite medir el abandono y desplazamiento provocado por la gentrificación).
1. **Fecha de Primer Registro del Comercio:**
   ```dax
   Fecha Primer Registro = 
   CALCULATE(
       MIN('32-hechos-comercios'[fecha_registro]),
       ALLEXCEPT('32-hechos-comercios', '32-hechos-comercios'[id_comercio])
   )
   ```
2. **Mes de Ingreso (Mes Cohorte):**
   ```dax
   Mes Cohorte = FORMAT('32-hechos-comercios'[Fecha Primer Registro], "YYYY-MM")
   ```
3. **Mes Registro Actual:**
   ```dax
   Mes Registro Actual = FORMAT('32-hechos-comercios'[fecha_registro], "YYYY-MM")
   ```
4. **Meses de Permanencia Activa (Distancia de Cohorte):**
   Mide cuántos meses ha sobrevivido el comercio tradicional desde su aparición.
   ```dax
   Meses Activo = 
   DATEDIFF(
       '32-hechos-comercios'[Fecha Primer Registro],
       '32-hechos-comercios'[fecha_registro],
       MONTH
   )
   ```

---

## 🎨 Diseño Visual del Dashboard (3 Páginas)

Diseñaremos un informe ejecutivo interactivo con una paleta de colores urbana y sobria (tonos azul acero para grandes superficies, tonos terracota/naranja para el comercio local y tradicional, y acentos de escala de grises para el alquiler y densidad urbana).

### 📊 Página 1: Panorama Comercial y Gentrificación (Overview)
- **Tarjetas KPI en la cabecera:** `Ventas Totales` (moneda), `Comercios Activos` (entero), `Alquiler Promedio m2` (moneda) y `Crecimiento Renta YoY %` (porcentaje con color condicional: rojo si sube deprisa, verde si se mantiene estable).
- **Tendencia de Renta vs. Desplazamiento (Gráfico de Líneas y Columnas agrupadas):** Eje X en `Año-Mes` de `dim_fecha`, Columnas para `Comercios Activos` (filtrando por Pequeño Comercio) y una Línea para `Alquiler Promedio m2`. *Permite observar si las rentas altas coinciden con la caída de comercios locales.*
- **Distribución de Ventas por Escala (Gráfico de Anillo):** Muestra el volumen total de ventas comparando `Pequeño Comercio` vs. `Gran Supermercado`.
- **Filtros Laterales (Segmentadores):** `nivel_socioeconomico` y `estatus_gentrificacion`.

### 🏢 Página 2: Diagnóstico por Barrio y Desplazamiento
- **Gráfico de Dispersión (Scatter Plot) de Desplazamiento:**
  - Eje X: `Alquiler Promedio m2`
  - Eje Y: `Ventas Totales`
  - Tamaño de la burbuja: `Afluencia Total`
  - Leyenda / Color: `tipo_escala` (Gran Supermercado vs. Pequeño Comercio)
  - Reproductor/Play Axis: `Año-Mes` (para ver la animación de cómo los comercios pequeños se reducen o cambian de cuadrante conforme pasan los meses).
- **Treemap de Categoría Comercial:** Mapea las `Ventas Totales` por `categoria_negocio` y `origen_capital`.
- **Matriz Detallada con Formato Condicional (Semáforo Urbano):**
  - Filas: `estatus_gentrificacion` ➔ `nombre_barrio`.
  - Columnas/Métricas: `Ventas Totales`, `Alquiler Promedio m2` y `% Participacion Ventas Pequenos Comercios`.
  - Formato condicional: Escala de colores degradada de amarillo a rojo en la columna de alquileres para alertar sobre zonas críticas de encarecimiento.

### 👥 Página 3: Matriz de Retención y Supervivencia Local (Cohortes)
- **Matriz de Supervivencia de Comercios Pequeños (Heatmap):**
  - Filas: `Mes Cohorte` (mes de inserción inicial del pequeño comercio).
  - Columnas: `Meses Activo` (0, 1, 2, 3... meses transcurridos).
  - Valores: `Comercios Activos` (filtrando visualmente `tipo_escala = "Pequeño Comercio"`).
  - Formato condicional: Escala de color terracota/naranja (donde el tono más oscuro es 100% de retención y se va aclarando conforme desaparecen los comercios).
- **Panel de Filtro de Barrio:** Permite al usuario filtrar la matriz de cohortes para comparar barrios "Tradicionales" contra barrios "Gentrificados" y evidenciar la diferencia en la tasa de mortalidad comercial.

---

## 🕵️‍♂️ Preguntas de Negocio para el Análisis de Gentrificación

Utiliza tu modelo y el dashboard interactivo para dar respuestas fundamentadas a la Secretaría de Desarrollo Social:

1. **Relación Renta-Desplazamiento:** *¿Existe una correlación directa entre el incremento del `Alquiler Promedio m2` y la disminución de la cantidad de `Comercios Activos` de escala pequeña? ¿Cuál es el umbral de alquiler por m2 en el que el comercio tradicional empieza a desaparecer masivamente?*
2. **Brecha de Cuota de Mercado:** *En los barrios clasificados como "En Transición", ¿cómo se comporta el indicador `% Participacion Ventas Pequenos Comercios` en comparación con los barrios "Gentrificados"? ¿Las grandes cadenas absorben por completo el consumo local o se estabiliza la coexistencia?*
3. **Análisis de Cohortes y Esperanza de Vida Comercial:** *Al comparar el heatmap de cohortes entre un barrio "Tradicional" y uno "Gentrificado", ¿cuál es la diferencia en la supervivencia promedio (en meses) del pequeño comercio? ¿Cuántas tienditas sobreviven más de 12 meses después de la entrada del primer "Gran Supermercado" en su zona?*
4. **Impacto Geográfico:** *¿Cuáles son los 3 barrios con mayor tasa de crecimiento interanual de renta comercial (`Crecimiento Renta YoY %`) y qué porcentaje de su afluencia peatonal se ha trasladado de pequeños comercios locales a franquicias multinacionales?*
5. **Estrategia de Mitigación:** *Basado en el indicador `% porcentaje_descuento_renta`, ¿los programas locales de subsidio de alquiler están funcionando para prolongar la supervivencia de los comercios pequeños en zonas de alta gentrificación? ¿Qué barrios requieren intervención prioritaria?*

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
