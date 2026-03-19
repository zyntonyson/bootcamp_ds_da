# *Construye historias visuales claras con gráficos II* 🎮📊

¡Hola, equipo! En esta sesión vamos a dar un paso más allá en la visualización de datos. No solo se trata de hacer gráficos bonitos, sino de construir herramientas que respondan preguntas de negocio y cuenten una historia clara y convincente. ¡Manos a la obra!

## Objetivos académicos 🎯

Al final de esta sesión, serás capaz de:

1.  **Traducir** una pregunta de negocio ambigua en **KPIs (Key Performance Indicators)** claros y medibles.
2.  **Planificar** la estructura de un dashboard utilizando una narrativa de datos como **SCQA (Situación, Complicación, Pregunta, Respuesta)**.
3.  **Diseñar** un boceto de dashboard que organice la información de manera jerárquica (de lo general a lo específico).
4.  **Argumentar** cómo el diseño y la narrativa de un dashboard facilitan la toma de decisiones.

## Andes Retail Group 🏢

Trabajas para **Andes Retail Group**, una empresa que vende una gran variedad de productos en varios países de Latinoamérica. La Directora Comercial, Ana, ha notado que los ingresos fluctúan mucho, pero no sabe exactamente por qué.

Ana te dice: 
> "Necesito entender qué pasó con los ingresos en 2024 y 2025. Veo picos y valles, pero no tengo claro si es por la temporada, por alguna categoría de producto o por el país. ¿Podemos crear un dashboard para explorar esto?"

Nuestra misión es convertir esta necesidad en una herramienta visual que le permita a Ana tomar decisiones informadas.



### Descripción de la dinámica ⚙️

Dividiremos la tarea en 4 pasos clave:

#### 1. Análisis de la petición de negocio 🧐

El primer paso es traducir la pregunta de Ana en KPIs concretos.

> **Pregunta de negocio:** "Andes Retail Group quiere entender cómo evolucionaron los ingresos 2024–2025 y por qué cambian por meses/estaciones.”

> **Audiencia:** ¿Quién lo verá? → Directora Comercial.
> **Pregunta Overview (General):** ¿Cuál es el rendimiento general de los ingresos y ganancias?
> **KPIs Overview Sugeridos:** Ingresos Totales, Ganancia Total, Margen de Ganancia (%), Pedidos Totales.
> **Preguntas de Detalle:** ¿Qué países o categorías explican las caídas/picos? ¿Hay algún patrón estacional?
> **Segmentadores Mínimos:** Año, País, Categoría de Producto, Estación.

#### 2. Análisis de los datos 🧹

Antes de construir, debemos asegurarnos de que nuestros datos son confiables. En esta fase, exploramos el dataset para:
-   Verificar tipos de datos (¡`Fecha_pedido` y `Unidades` necesitan atención!).
-   Buscar valores nulos o inconsistentes.
-   Identificar las columnas clave para nuestros KPIs y filtros.

### Diccionario de datos 📚

Puedes descargar los datos de la liga [Andes Retail Group](https://raw.githubusercontent.com/zyntonyson/data_repo/refs/heads/main/andes_retail_group/S10_AndesRetail_Desempeno_Comercial_2022_2025.csv) y para ayudarte, aquí tienes la estructura de los datos de ventas:

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

```python
andes_retail_group = pd.read_csv('https://raw.githubusercontent.com/zyntonyson/data_repo/refs/heads/main/andes_retail_group/S10_AndesRetail_Desempeno_Comercial_2022_2025.csv')
```



#### 3. Boceto del dashboard 📝

Con los KPIs y filtros claros, es hora de dibujar nuestra propuesta. 
Un buen dashboard tiene una jerarquía: empieza con una vista general y permite explorar detalles.Puedes usar excalidraw para hacer tus bocetos rápidos [excalidraw.com](https://excalidraw.com/).

> **Sugerencias para el boceto:**
>
> **Nivel 1: Overview (Vista General)**
> -   **Tarjetas de KPIs:** Mostrar Ingresos Totales, Ganancia Total, Margen Promedio, y Total de Pedidos del período seleccionado.
> -   **Gráfico Principal:** Un gráfico de líneas mostrando la evolución mensual de Ingresos y Ganancia.
> -   **Gráficos Secundarios:** Un mapa para ver los ingresos por `País` y un gráfico de barras para el top 5 de `Categoría_Producto`.
>
> **Nivel 2: Detalle (Drill-Down)**
> -   **Tabla Detallada:** Una tabla con los pedidos individuales que se actualice según los filtros aplicados.
> -   **Filtros Interactivos:** Segmentadores para `Año`, `Estación`, `País`, `Canal` y `Categoría_Producto`.

#### 4. Conexión, diseño y publicación del dashboard 🚀

¡Es el momento de la verdad! Conectamos nuestros datos a una herramienta de BI (Power BI, Tableau, Looker Studio) y construimos el dashboard siguiendo nuestro boceto.

Para que el dashboard cuente una historia efectiva, usaremos la narrativa **SCQA**:

-   **S (Situación):** Describe el panorama general.
    > *Los ingresos totales de 2024-2025 son sólidos, con Perú y Colombia como los principales mercados.*
-   **C (Complicación):** Señala un problema o cambio interesante.
    > *Sin embargo, se observa una caída significativa de los ingresos durante los meses de invierno en ambos años.*
-   **Q (Pregunta):** La pregunta que surge de la complicación.
    > *¿Qué categorías de producto o países están impulsando esta caída estacional?*
-   **A (Respuesta):** La explicación basada en datos, con una recomendación.
    > *La categoría "Moda" y "Deportes" muestran la mayor caída en invierno. **Recomendación:** Lanzar campañas específicas para estas categorías en temporada baja para estabilizar los ingresos.*

**Entrega final:**
-   Si usas Power BI o Tableau, entrega el archivo (`.pbix` o `.twbx`).
-   Si usas Looker Studio, comparte el enlace público de tu dashboard.

---

## Cierre y reflexión 🤔

Para finalizar, reflexionemos sobre lo que hemos construido:

*   ¿Qué elementos de tu dashboard consideras más relevantes para que Ana tome decisiones?
*   ¿Cómo se relaciona esta actividad con lo que hemos visto en sprints anteriores (calidad de datos, SQL, análisis exploratorio)?
*   Si tuvieras solo 2 minutos para presentarle tu dashboard a la Directora Comercial, ¿qué historia le contarías?

¡Excelente trabajo, equipo! Han transformado datos crudos en una historia visual con un propósito claro. 👏
