# 📊 Análisis del Proyecto: Andes Capital Real Estate (Sprint 11)

Este documento contiene un desglose estructurado de las tareas requeridas y las especificaciones de tipos de datos para el **Proyecto de Análisis Comercial Inmobiliario** de Andes Capital. El objetivo del proyecto es construir un **dashboard ejecutivo** interactivo (en Power BI o Tableau) que responda a preguntas estratégicas de ventas, segmentación de clientes y retención (cohortes).

---

## 📂 1. Orígenes de Datos y Tipos de Datos Necesarios

El proyecto cuenta con tres datasets iniciales en formato CSV y requiere la creación de un cuarto (dim_fecha). A continuación se detallan sus estructuras y los tipos de datos a configurar:

### 🔹 1.1 `hecho_ventas_propiedades.csv` (Tabla de Hechos)
Registra cada transacción inmobiliaria individual.

| Columna | Tipo de Dato (Origen) | Tipo de Dato (BI Target) | Descripción |
| :--- | :--- | :--- | :--- |
| `id_venta` | Texto / String | Texto | Clave Primaria (PK) única de la transacción (Ej: `SALE000001`). |
| `fecha_venta` | Texto / String | Fecha (Date) | Fecha en que se realizó la venta (Ej: `2024-01-05`). *Requiere conversión*. |
| `id_cliente` | Texto / String | Texto | Clave Foránea (FK) que conecta con `dim_clientes` (Ej: `CUST02497`). |
| `id_propiedad` | Texto / String | Texto | Clave Foránea (FK) que conecta con `dim_propiedades` (Ej: `PROP03591`). |
| `ciudad` | Texto / String | Texto / Categoría Geográfica | Ciudad de la transacción (Ej: `Bogotá`, `Ciudad de México`). |
| `precio_venta` | Entero / Numérico | Entero / Moneda | Precio final de la venta (Ej: `1027126`). |
| `tipo_propiedad` | Texto / String | Texto | Tipo de inmueble (Ej: `Casa`, `Departamento`, `Comercial`). |
| `canal_venta` | Texto / String | Texto | Canal a través del cual se vendió (Ej: `Corredor`, `Directo`, `Digital`). |
| `porcentaje_comision` | Flotante / Numérico | Porcentaje (%) | Comisión cobrada en la venta (Ej: `0.0473` -> `4.73%`). *Requiere formato %*. |
| `monto_comision` | Entero / Numérico | Entero / Moneda | Monto calculado de la comisión (Ej: `48605`). |

### 🔹 1.2 `dim_clientes.csv` (Dimensión Clientes)
Contiene la información demográfica e histórica de segmentación de los compradores.

| Columna | Tipo de Dato (Origen) | Tipo de Dato (BI Target) | Descripción |
| :--- | :--- | :--- | :--- |
| `id_cliente` | Texto / String | Texto | Clave Primaria (PK) del cliente (Ej: `CUST00001`). Sin duplicados. |
| `segmento_comprador` | Texto / String | Texto | Segmento del comprador (Ej: `Primera vez`, `Alto patrimonio`, `Inversionista`). |
| `pais` | Texto / String | Texto / Categoría Geográfica | País de residencia del cliente (Ej: `Colombia`, `Mexico`). |
| `ciudad` | Texto / String | Texto / Categoría Geográfica | Ciudad de residencia del cliente (Ej: `Bogotá`, `Ciudad de México`). |

### 🔹 1.3 `dim_propiedades.csv` (Dimensión Propiedades)
Contiene los detalles técnicos y geográficos de los bienes raíces comercializados.

| Columna | Tipo de Dato (Origen) | Tipo de Dato (BI Target) | Descripción |
| :--- | :--- | :--- | :--- |
| `id_propiedad` | Texto / String | Texto | Clave Primaria (PK) del inmueble (Ej: `PROP00001`). Sin duplicados. |
| `tipo_propiedad` | Texto / String | Texto | Tipo de propiedad (Ej: `Apartment`, `House`, `Office`, `Commercial`, `Land`). |
| `ciudad` | Texto / String | Texto / Categoría Geográfica | Ciudad donde se localiza el inmueble (Ej: `Bogotá`, `Ciudad de México`). |
| `barrio` | Texto / String | Texto | Barrio o vecindario (Ej: `Chapinero`, `Polanco`, etc.). |
| `habitaciones` | Entero | Entero (Número entero) | Número de recámaras/habitaciones (Ej: `3`). |
| `tamano_m2` | Entero | Entero (Número entero) | Superficie construida en metros cuadrados (Ej: `150`). |
| `precio_publicado` | Flotante / Numérico | Entero / Moneda | Precio original de publicación del inmueble (Ej: `350000`). |
| `categoria_propiedad` | Texto / String | Texto | Categorización general (Ej: `Residential`, `Commercial`, `Industrial`). |

### 🔹 1.4 `dim_fecha.csv` / `dim_fecha` (Dimensión de Tiempo - Tabla Calendario)
*Nota: Si se usa Power BI, se construye dinámicamente mediante DAX. En Tableau, se puede importar o generar por jerarquías.*

| Columna | Tipo de Dato (Origen / DAX) | Tipo de Dato (BI Target) | Descripción |
| :--- | :--- | :--- | :--- |
| `Date` / `Fecha` | Fecha / Date | Fecha (Clave PK) | Fecha única por día en el rango dinámico. |
| `Año` | Entero | Entero | Año del registro (Ej: `2024`). |
| `Mes` | Texto / String | Texto | Nombre completo del mes en español (Ej: `Enero`). |
| `Mes Numero` | Entero | Entero | Número ordinal del mes (Ej: `1`). Útil para ordenar la columna de texto "Mes". |
| `Año-Mes` | Texto / String | Texto / Código Temporal | Identificador de mes (Ej: `2024-01`). |
| `Trimestre` | Texto / String | Texto | Trimestre (Ej: `Q1`). |
| `Año-Trimestre` | Texto / String | Texto | Año-Trimestre concatenado (Ej: `2024-Q1`). |
| `Dia Semana` | Texto / String | Texto | Día de la semana (Ej: `Lunes`). |
| `Es Fin Semana` | Booleano | Booleano (Verdadero / Falso) | Indica si es fin de semana (Ej: `True`). |

---

## 🛠️ 2. Desglose de Tareas Requeridas

Para completar exitosamente el proyecto, se deben desarrollar las siguientes actividades estructuradas en pasos:

### 🧹 Paso 1: Limpieza e Importación de Datos
- **Carga de Datos**: Importar las tablas dimensionales y de hechos desde los CSV al motor de BI (Power Query o Tableau Data Source).
- **Tipos de Datos**:
  - Asegurar la conversión de `fecha_venta` de Texto a **Fecha**.
  - Formatear los campos numéricos monetarios (`precio_venta`, `monto_comision`, `precio_publicado`) como moneda local/formato numérico adecuado.
  - Asegurar que `porcentaje_comision` se lea correctamente como número decimal y formatearlo como **Porcentaje**.
- **Tratamiento de Nulos**: Examinar si existen valores nulos y justificar la acción tomada (imputación, eliminación o retención).
- **Control de Duplicados**: Validar la integridad referencial y asegurar que las claves primarias (`id_cliente` en `dim_clientes` e `id_propiedad` en `dim_propiedades`) no tengan duplicados.

### 📅 Paso 2: Creación de la Tabla Calendario (`dim_fecha`)
*Solo aplicable si se implementa en Power BI:*
- Crear una nueva tabla DAX llamada `dim_fecha`.
- Utilizar las funciones `CALENDAR` y `ADDCOLUMNS` de forma dinámica:
  - Rango de fechas: desde `MIN(hecho_ventas_propiedades[fecha_venta])` hasta `MAX(hecho_ventas_propiedades[fecha_venta])`.
- Incluir las columnas obligatorias:
  - `Año = YEAR([Date])`
  - `Mes = FORMAT([Date], "MMMM")` (nombre completo del mes)
  - `Mes Número = MONTH([Date])`
  - `Año-Mes = FORMAT([Date], "YYYY-MM")`
- **Configuración**: Marcar la tabla recién creada como **Tabla de fechas** (Mark as date table) utilizando la columna `Date` como clave.

### 🧩 Paso 3: Modelado de Datos (Esquema Estrella)
- **Estructuración**: Colocar la tabla `hecho_ventas_propiedades` en el centro del lienzo del modelo.
- **Relaciones**:
  - Conectar `dim_clientes` a `hecho_ventas_propiedades` a través de `id_cliente` (Relación `1:*`, dirección de filtro: Única/Simple).
  - Conectar `dim_propiedades` a `hecho_ventas_propiedades` a través de `id_propiedad` (Relación `1:*`, dirección de filtro: Única/Simple).
  - Conectar `dim_fecha` a `hecho_ventas_propiedades` a través de `Date` -> `fecha_venta` (Relación `1:*`, dirección de filtro: Única/Simple).
- **Validación**: Comprobar que todas las relaciones estén activadas y que sigan la dirección de filtro estándar del esquema estrella (de las dimensiones a la tabla de hechos).

### 📊 Paso 4: Implementación de Medidas y Cálculos
- **4.1 Medidas Base**:
  - `Ingreso Total` = Suma de `precio_venta`.
  - `Cantidad de Ventas` = Conteo de filas de transacciones o conteo de `id_venta`.
  - `Ticket Promedio` = `Ingreso Total / Cantidad de Ventas` o promedio de `precio_venta`.
  - `Comisión Total` = Suma de `monto_comision`.
- **4.2 Medidas con Contexto de Filtro Modificado (%)**:
  - Construir al menos 2 medidas que utilicen la modificación de contexto para calcular participación. Ejemplos:
    - `% Participación Ingresos por Tipo de Propiedad` = Dividir el ingreso filtrado entre el ingreso total acumulado sin filtros de propiedad (usando `CALCULATE` y `ALL`/`ALLSELECTED` en DAX, o expresiones `FIXED` LOD en Tableau).
    - `% Participación Ingresos por Canal de Venta`.
    - `% Participación Ingresos por Segmento de Cliente`.
- **4.3 Inteligencia de Tiempo**:
  - Implementar al menos 2 cálculos de tiempo. Opciones:
    - `Ventas YTD (Year-to-Date)`: Ventas acumuladas del año actual.
    - `Ventas del Año Anterior (Prior Year - PY)`.
    - `Crecimiento YoY % (Year-over-Year)`: `(Ventas Actuales - Ventas Año Anterior) / Ventas Año Anterior`.
- **4.4 Columnas Calculadas para Cohortes (Recompra)**:
  - Crear en la tabla `hecho_ventas_propiedades` los siguientes campos para la matriz de cohortes:
    - `Primera compra por cliente`: Registra la fecha mínima de venta para cada cliente.
    - `Mes Cohorte`: Mes y año de esa primera compra (mes de adquisición).
    - `Mes Venta`: Mes y año de la venta del registro actual (para calcular la distancia en meses y mapear la recompra).

### 🎨 Paso 5: Diseño del Reporte Visual (Dashboard de 3 Páginas)
- **Página 1: Overview Ejecutivo**:
  - Panel superior con 4 tarjetas de KPIs: *Ingreso Total*, *Cantidad de Ventas*, *Ticket Promedio* y *Comisión Total*.
  - Gráfico de líneas o columnas para mostrar la evolución y tendencia de las ventas en el tiempo.
  - Gráfico de barras horizontales mostrando el volumen de ingresos por ciudad.
  - Indicador visual o tarjeta del crecimiento YoY %.
- **Página 2: Análisis Comercial**:
  - Gráficos de distribución de ingresos (Ej: donas, barras o treemap) por:
    - *Tipo de propiedad*.
    - *Canal de venta*.
    - *Segmento de cliente*.
  - Tabla detallada con formato condicional (estilo semáforo) que agrupe por *Tipo de propiedad*, mostrando su *Ingreso Total*, *Cantidad de Ventas* y *Ticket Promedio*.
  - Agregar tooltips dinámicos que incluyan las medidas de `% Participación` creadas en el Paso 4.2.
- **Página 3: Análisis de Cohortes**:
  - Matriz de cohortes (tabla de doble entrada o mapa de calor):
    - Filas: `Mes Cohorte` (mes de primera compra).
    - Columnas: `Mes Venta` o `Meses Transcurridos`.
    - Valores: Conteo de ventas, ingresos generados o número de clientes activos que recompran.
  - El diseño debe permitir visualizar de forma clara la tasa de retención y la frecuencia con la que los clientes vuelven a comprar en Andes Capital.

### 📝 Paso 6: Resumen Ejecutivo e Insights
- Completar la sección final del Jupyter Notebook detallando:
  - **Hallazgos clave**: Desempeño comercial y qué variables (tipos, canales, ciudades) son las más representativas en facturación.
  - **Métricas principales**: Valores consolidados y validados de los KPIs.
  - **Insights accionables**: Análisis de comportamiento de clientes, cohortes y crecimiento porcentual YoY.
  - **Recomendaciones estratégicas**: Propuestas de negocio justificadas por los datos (por ejemplo, potenciar ciertos canales o fidelizar segmentos clave).

### 🚀 Paso 7: Publicación y Entrega
- Publicar el dashboard en Power BI Service (crear link público) o subirlo a Tableau Public / Tableau Cloud.
- Alternativamente, subir el archivo `.pbix` a una carpeta de Google Drive/OneDrive y compartir el enlace con permisos de lectura.
- Registrar el enlace final en la celda designada al final del notebook de entregas.
