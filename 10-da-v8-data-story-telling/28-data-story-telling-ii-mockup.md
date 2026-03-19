# *Construye historias visuales claras con gráficos II* 🎮📊

## Objetivos academicos

 Agrega aquí 4 objetivos relacionados con el diseño de dashboards a partir de una necesidad de negocio real con una planeación clara y una narrativa SCQA.

## Andes Retail Group 

Aqui crea un contexto de negocio sobre Andes Retail Group con una necesidad de un stakeholder. La actividad deberá ser de convertir la pregunta a un kpi que pueda ser mostrado en un dashboard.  Te comparto un poco de la estructura de los datos para puedas crear el contexto donde incluyas las preguntas, el stakeholder y sus necesidades de segmentacion de información.


### Diccionario de datos 

- `ID_Pedido`: identificador de la transacción (texto)
- `Fecha_pedido`: fecha del pedido (viene como **texto** `dd/mm/yyyy` para practicar *locale*)
- `ID_Cliente`: cliente (texto)
- `Ingresos`: monto vendido (puede venir como número o texto → lo arreglamos)
- `Costo`, `Ganancia`: costos y ganancia (número)
- `Unidades`: unidades (puede venir mezclado texto/número → lo arreglamos)
- `Pais`, `Region`, `Ciudad`: ubicación
- `Segmento_Cliente`: Premium / Estandar / Basico
- `Categoria_Producto`, `Producto`: producto
- `Canal`: Online / Tienda
- `Campaña`: campaña comercial
- `Estación`: Verano / Otoño / Invierno / Primavera

### Muestra de datos

|    | ID_Pedido        | Fecha_pedido   | ID_Cliente   | Segmento_Cliente   | Pais     | Region    | Ciudad      | Categoria_Producto   | Producto   | Canal   | Campaña        | Estación   |   Unidades |   Descuento_pct |   Ingresos |   Costo |   Ganancia |
|---:|:-----------------|:---------------|:-------------|:-------------------|:---------|:----------|:------------|:---------------------|:-----------|:--------|:---------------|:-----------|-----------:|----------------:|-----------:|--------:|-----------:|
|  0 | ORD-202501-00000 | 31/01/2025     | CLI-7800     | Estandar           | Colombia | Andina    | Bogotá      | Electronica          | Tablet     | Tienda  | Temporada baja | Verano     |          1 |               0 |   356.06   |     233 |        123 |
|  1 | ORD-202512-00001 | 30/12/2025     | CLI-8137     | Estandar           | Mexico   | Occidente | Guadalajara | Hogar                | Aspiradora | Online  | Siempre activo | Verano     |          5 |               0 |   994.971  |     706 |        289 |
|  2 | ORD-202405-00002 | 10/05/2024     | CLI-3123     | Estandar           | Mexico   | Centro    | CDMX        | Electronica          | Parlante   | Online  | Temporada baja | Otoño      |          3 |               0 |   400.343  |     289 |        111 |
|  3 | ORD-202507-00003 | 18/07/2025     | CLI-2206     | Premium            | Peru     | Costa     | Lima        | Electronica          | Audifonos  | Online  | Navidad        | Invierno   |          2 |               0 |   203.07   |     142 |         61 |
|  4 | ORD-202502-00004 | 04/02/2025     | CLI-3379     | Estandar           | Colombia | Andina    | Medellín    | Hogar                | Licuadora  | Online  | Temporada baja | Verano     |          1 |               0 |    85.5042 |      56 |         29 |
|  5 | ORD-202412-00005 | 31/12/2024     | CLI-3475     | Estandar           | Peru     | Sierra    | Arequipa    | Deportes             | Guantes    | Online  | Siempre activo | Verano     |          1 |               0 |    34.1862 |      24 |         10 |
|  6 | ORD-202411-00006 | 10/11/2024     | CLI-1923     | Premium            | Chile    | Norte     | Antofagasta | Moda                 | Zapatillas | Tienda  | Siempre activo | Primavera  |          1 |               0 |   125.14   |      78 |         48 |
|  7 | ORD-202205-00007 | 02/05/2022     | CLI-1453     | Basico             | Peru     | Sierra    | Arequipa    | Deportes             | Cuerda     | Online  | Back to School | Otoño      |          2 |               0 |    31.4519 |      21 |         10 |
|  8 | ORD-202304-00008 | 12/04/2023     | CLI-8421     | Premium            | Mexico   | Norte     | Monterrey   | Hogar                | Aspiradora | Online  | Temporada baja | Otoño      |          3 |               0 |   602.362  |     402 |        200 |
|  9 | ORD-202505-00009 | 23/05/2025     | CLI-2956     | Premium            | Colombia | Pacífico  | Cali        | Electronica          | Audifonos  | Online  | Siempre activo | Otoño      |          1 |             nan |   139.725  |      95 |         45 |

### Descripción de la dinámica

Ahora vamos a describir la dinámica, los participantes por grupos deberan:

#### Análisis de la petición de negocio. 

Aqui los participantes deben convertir las preguntas de negocio a KPIS 

Aqui incluye en un bloque de qoute sugerencias de KPIS basados en las preguntas del stakeholder

“Andes Retail Group quiere entender cómo evolucionaron los ingresos 2024–2025 y por qué cambian por meses/estaciones.”

Audiencia: ¿quién lo verá? (ej. Director Comercial)
Pregunta Overview: 1 sola
3–4 KPIs Overview: (ej. Ingresos, Ganancia, Margen, Pedidos)
2 preguntas Detalle: (ej. “¿qué países o categorías explican la caída?”)
Segmentadores mínimos: 2 (ej. Año, País)


#### Analisis de los datos 



Aqui se se hace el reconocimiento de los datos , se evalua la limpieza y se identifican las columnas claves


#### Boceto del dashboard

Se diseña un boceto de la propuesta de dashboard proponiendo graficos,tablas para los KPIS asi como lo segmentadores probables de los datos. Aqui es importante tener datos tipo overview y de nivel detalle
Incluye en un bloque de qoute sugerencias de gráficos, tablas y segmentadores que pudieran agregar. Puede usarse la estructura



#### Conexión y diseño del dashboard y publicacion

Aquí se hace el trabajo ya sea en PowerBi, Tableau o Looker. Organiza el trabajo en etapas donde los estudiantes generen la vista con metricas overview globales, vista de datos detallados, segmentadores. Dale sugerencias sobre llevar la narrativa
del dashboard para que el dashboard sea efectivo. 

SCQA (Situación–Complicación–Pregunta–Respuesta)
S (Situación): qué se observa en general (overview)
C (Complicación): qué problema/cambio llama la atención
Q (Pregunta): qué quieres explicar
A (Respuesta): explicación basada en evidencia + acción recomendada

S: 2024–2025 muestra ingresos sólidos, con Perú liderando en facturación.
C: Se observa una caída a mitad de año.
Q: ¿Por qué disminuyen los ingresos en esos meses?
A: Hay un patrón estacional: Invierno presenta el menor ingreso. Recomendación: campañas específicas en temporada baja y foco en categorías con mayor caída.



Al final en la publicación pide a los estudiantes que si trabajaron en PowerBi o Tableau entreguen el archivo generado y si fue en looker la liga del dashboard


## Cierre 

Agrega aqui algunas preguntas de reflexion sobre la actividad del estilo:

* ¿Qué elementos del dashboard resaltas cómo más relevantes para la toma de decisiones?
* ¿Cómo complementarias la generación de un dashboard con lo visto en los sprint anteriores?