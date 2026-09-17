# PROMPT MAESTRO — PROYECTOS DE LIMPIEZA DE DATOS Y REPORTEO SIMPLE EN EXCEL

Actúa como **diseñador instruccional y analista de datos senior**.

Tu tarea es crear **un solo proyecto práctico de análisis de datos** dirigido a estudiantes que ya conocen fórmulas básicas de Excel o Google Sheets.

El objetivo principal del proyecto debe ser practicar:

- exploración de datos;
- identificación de problemas de calidad;
- limpieza y estandarización;
- recuperación de valores faltantes;
- eliminación de duplicados;
- cálculo de métricas sencillas;
- creación de gráficas básicas;
- redacción de un resumen ejecutivo.

El proyecto debe simular una tarea que podría recibir un **analista de datos junior en una empresa real**.

No incluyas programación, SQL, Power BI, estadística avanzada, machine learning ni análisis predictivo.

---

# 1. PARÁMETROS DE ENTRADA

Genera el proyecto utilizando estos parámetros:

**Sector / industria:** [SECTOR]

**Número de registros:** [NÚMERO_DE_REGISTROS]

Si no se especifica, utiliza **100 registros**.

**Duración objetivo:** [TIEMPO]

Si no se especifica, utiliza **90 minutos**.

**País o región:** [PAÍS_O_REGIÓN]

Si no se especifica, selecciona uno coherente con el sector.

**Periodo de análisis:** [PERIODO]

Si no se especifica, selecciona un periodo razonable de entre 1 y 6 meses.

**Nivel:** Básico-intermedio.

**Herramienta:** [HERRAMIENTA]

Valores permitidos: **Excel** o **Google Sheets**.

Si no se especifica, utiliza **Excel**.

**Regla de entrega:** independientemente de la herramienta elegida, los archivos de trabajo del estudiante y del instructor deben generarse físicamente en formato `.xlsx`.

Si la herramienta es **Google Sheets**, el `.xlsx` debe estar diseñado para importarse y trabajar correctamente en Google Sheets, evitando características exclusivas de Excel y utilizando fórmulas, formatos y gráficos compatibles con Google Sheets.

**Idioma de instrucciones:** Español.

**Idioma de las fórmulas:** Incluye el nombre de la función en inglés y, cuando sea útil, su equivalente en Excel en español.

Todos los nombres, empresas, personas, transacciones y datos deben ser **ficticios y sintéticos**.

---

# 2. PERFIL DEL ESTUDIANTE

El proyecto está dirigido a estudiantes que:

- conocen fórmulas básicas;
- saben seleccionar rangos;
- pueden copiar fórmulas;
- conocen filtros;
- saben aplicar formatos de número, moneda y fecha;
- pueden crear gráficos sencillos;
- todavía están desarrollando criterio para limpiar y analizar datos.

Las instrucciones deben ser suficientemente claras para que puedan trabajar de forma independiente.

No asumas conocimientos avanzados.

---

# 3. ENTREGABLES QUE DEBES GENERAR

Genera exactamente estos tres archivos:

### Archivo 1 — Instrucciones del estudiante

`Proyecto_[nombre_corto].md`

### Archivo 2 — Proyecto del estudiante

`Proyecto_[nombre_corto]_Estudiante.xlsx`

### Archivo 3 — Proyecto resuelto para instructor

`Proyecto_[nombre_corto]_Solucion.xlsx`

Los tres archivos deben ser completamente coherentes entre sí.

**Regla crítica sobre los datos:** el archivo del estudiante debe contener el **dataset sucio**, con los errores de calidad deliberadamente introducidos. Bajo ninguna circunstancia entregues al estudiante el dataset ya limpio, normalizado, corregido o preprocesado.

El archivo del instructor debe partir exactamente del mismo dataset sucio y mostrar su transformación hasta llegar al resultado limpio.

No generes más de un proyecto por ejecución.

---

# 4. ARCHIVO MARKDOWN DE INSTRUCCIONES

El archivo `.md` debe contener las instrucciones completas del proyecto.

Utiliza la siguiente estructura.

# Proyecto: [Título]

## Introducción

Presenta un escenario profesional.

El estudiante debe asumir el rol de un **analista de datos junior** que recibe un archivo con información que necesita ser limpiada y resumida.

Describe:

- nombre de la empresa ficticia;
- sector;
- actividad principal;
- departamento que solicita el análisis;
- situación o problema de negocio;
- periodo analizado;
- por qué se necesita limpiar la información;
- qué decisión espera apoyar el análisis.

El contexto debe ser realista y sencillo.

La limpieza y el análisis deben tener una razón de negocio clara.

---

# 5. EL DESAFÍO

Explica que el estudiante recibió información que presenta distintos problemas de calidad.

Menciona de manera general problemas como:

- formatos inconsistentes;
- datos numéricos almacenados incorrectamente;
- fechas con diferentes formatos;
- texto inconsistente;
- espacios adicionales;
- uso irregular de mayúsculas y minúsculas;
- categorías equivalentes escritas de distintas formas;
- valores faltantes;
- valores que pueden recuperarse mediante otras columnas;
- duplicados;
- columnas que contienen información que puede separarse.

No identifiques todas las filas problemáticas.

El estudiante debe descubrir parte de los errores durante la exploración.

---

# 6. CONTEXTO DEL NEGOCIO

Incluye una sección específica llamada:

## Contexto del negocio

Describe claramente:

- qué hace la empresa;
- qué representa el dataset;
- qué periodo contiene;
- qué representa cada registro;
- cuál es la pregunta principal del negocio;
- qué tipo de conclusiones espera obtener el responsable del área.

Las métricas y visualizaciones posteriores deben estar directamente relacionadas con este contexto.

---

# 7. ARCHIVOS PROPORCIONADOS

Incluye una sección:

## Archivos proporcionados

Explica que el estudiante recibe:

`Proyecto_[nombre]_Estudiante.xlsx`

Describe brevemente su estructura.

---

# 8. DESCRIPCIÓN DEL DATASET

Incluye:

## Descripción de los datos

Crea un diccionario de datos en formato tabla con:

| Columna | Descripción | Tipo esperado | Ejemplo |
|---|---|---|---|

Describe todas las columnas.

El dataset debe contener aproximadamente el número de registros solicitado.

Cada columna debe tener una utilidad clara.

Evita columnas innecesarias.

---

# 9. OBJETIVOS DEL PROYECTO

Indica que el estudiante deberá demostrar que puede:

1. explorar un conjunto de datos;
2. identificar problemas de calidad;
3. conservar los datos originales;
4. limpiar texto;
5. estandarizar categorías;
6. corregir formatos numéricos;
7. corregir formatos de fecha;
8. dividir información cuando sea necesario;
9. identificar valores faltantes;
10. recuperar valores faltantes mediante relaciones lógicas;
11. tomar decisiones sencillas sobre valores faltantes no recuperables;
12. identificar y eliminar duplicados;
13. calcular métricas básicas;
14. crear gráficas sencillas;
15. redactar conclusiones para una persona de negocio.

---

# 10. ESTRUCTURA DEL EXCEL DEL ESTUDIANTE

El archivo de Excel debe venir preparado como plantilla.

Debe contener exactamente estas hojas principales:

### Datos_Originales

Contiene el **dataset crudo y deliberadamente sucio**.

Debe incluir físicamente los errores de calidad descritos en el proyecto: inconsistencias de texto, formatos incorrectos, valores faltantes, duplicados y demás problemas definidos.

No debe contener una versión previamente corregida de los datos.

El estudiante no debe modificar esta hoja.

Incluye una nota visible:

**“No modificar. Esta hoja conserva una copia de los datos originales.”**

### Datos_Limpios

Debe contener inicialmente una **copia exacta del dataset sucio de `Datos_Originales`**, no una copia del dataset limpio base usado internamente para construir el ejercicio.

Al abrir el archivo por primera vez, los errores deliberados deben seguir visibles y sin corregir en esta hoja.

Aquí realizará el estudiante todas las transformaciones.

**Prohibido en la versión del estudiante:**

- corregir automáticamente mayúsculas, espacios, categorías o nombres;
- convertir previamente números almacenados como texto a valores numéricos;
- normalizar fechas inconsistentes antes de la entrega;
- completar valores faltantes;
- eliminar duplicados;
- precargar fórmulas que resuelvan las tareas de limpieza;
- reemplazar valores inconsistentes por sus equivalentes correctos.

Las columnas auxiliares pueden estar creadas, pero deben permanecer vacías cuando formen parte del ejercicio.

Cuando sea necesario, incluye columnas adicionales vacías para ejercicios como:

- Ciudad corregida;
- Nombre limpio;
- Categoría corregida;
- Fecha corregida;
- información dividida;
- cálculos recuperados.

### Analisis

Debe contener una plantilla para calcular las métricas solicitadas.

Utiliza una estructura similar a:

| Métrica / Pregunta | Resultado |
|---|---|
| Total de ... | |
| Promedio de ... | |
| Máximo de ... | |
| ... | |

No incluyas las respuestas en el archivo del estudiante.

### Visualizaciones

Incluye una sección preparada para cada gráfica.

Ejemplo:

**Gráfica 1: Ventas por categoría**

Pregunta de negocio:

[...]

Tipo de gráfica sugerida:

Gráfico de columnas.

Deja espacio para insertar la gráfica.

### Informe_Ejecutivo

Incluye una plantilla con campos como:

**Registros originales:**

**Duplicados encontrados:**

**Valores faltantes encontrados:**

**Valores recuperados:**

**Principales métricas:**

**Hallazgo 1:**

**Hallazgo 2:**

**Hallazgo 3:**

**Recomendación 1:**

**Recomendación 2:**

---

# 11. TAREAS DE LIMPIEZA

La limpieza debe ser el componente principal del proyecto.

Distribuye deliberadamente distintos errores en el dataset.

La mayoría de los registros deben ser correctos.

Aproximadamente entre **10 % y 20 % de las filas** deben contener uno o más problemas de calidad.

Los errores deben parecer realistas.

---

# 12. LIMPIEZA DE TEXTO

Incluye ejercicios que requieran utilizar algunas de las siguientes funciones o herramientas:

### LOWER()

Convertir texto a minúsculas.

### UPPER()

Convertir texto a mayúsculas.

### PROPER()

Estandarizar nombres propios.

### TRIM()

Eliminar espacios innecesarios.

### SPLIT / TEXTSPLIT / Dividir texto en columnas

Separar información contenida en una sola columna.

### Buscar y reemplazar

Corregir valores recurrentes.

No es necesario utilizar todas las funciones en cada proyecto, pero cada proyecto debe utilizar **al menos cuatro técnicas de limpieza de texto** de esta lista.

---

# 13. VALORES INCONSISTENTES

Introduce valores categóricos inconsistentes de manera deliberada.

Ejemplo:

Una categoría correcta podría ser:

`Monterrey`

pero aparecer también como:

`MONTERREY`

`monterrey`

`Monterrey `

`MTY`

El estudiante debe recibir instrucciones explícitas sobre cuál es el valor correcto esperado.

Por ejemplo:

“Estandariza todas las variantes MTY, monterrey y MONTERREY como Monterrey.”

Incluye entre **2 y 4 columnas** con este tipo de problemas, dependiendo del contexto.

Los reemplazos deben tener sentido para el negocio.

---

# 14. FORMATOS NUMÉRICOS

Incluye datos numéricos que necesiten alguna transformación o formato.

Ejemplos:

- moneda;
- porcentaje;
- cantidades;
- decimales;
- números almacenados como texto.

Solicita al estudiante aplicar el formato correcto.

Ejemplo:

“Aplica formato de moneda con dos decimales a Precio unitario y Monto total.”

No utilices transformaciones numéricas excesivamente complejas.

---

# 15. FORMATOS DE FECHA

Cuando el dataset contenga fechas, introduce una cantidad moderada de formatos inconsistentes.

Por ejemplo:

`15/03/2026`

`2026-03-15`

`15-Mar-2026`

El estudiante deberá convertirlas a un formato único.

Define explícitamente el formato esperado.

Por ejemplo:

`dd/mm/aaaa`

Todas las fechas deben corresponder al periodo del proyecto, excepto si una fecha fuera de rango es un error deliberado que el estudiante debe identificar.

---

# 16. VALORES PERDIDOS

Los valores faltantes son obligatorios.

Deben existir dos tipos.

## Tipo A — Valores recuperables

Crea valores faltantes que puedan reconstruirse exactamente utilizando otras columnas.

El archivo de instrucciones debe explicar **cómo recuperarlos**.

Ejemplos:

Si existen:

- Cantidad
- Precio unitario
- Monto total

puedes eliminar deliberadamente algunos valores de Precio unitario e indicar:

**Precio unitario = Monto total / Cantidad**

También puedes eliminar algunos valores de Monto total e indicar:

**Monto total = Precio unitario × Cantidad**

Otros ejemplos posibles según el sector:

**Área = Base × Altura**

**Costo total = Cantidad × Costo unitario**

**Duración = Fecha final - Fecha inicial**

**Margen = Venta - Costo**

**Unidades = Monto total / Precio unitario**

Utiliza relaciones que tengan sentido en el contexto del proyecto.

Debe haber al menos **dos tipos de valores recuperables**.

Nunca elimines simultáneamente todos los campos necesarios para realizar el cálculo.

Los resultados deben ser matemáticamente consistentes.

---

# 17. VALORES FALTANTES NO RECUPERABLES DIRECTAMENTE

Incluye también algunos valores faltantes que no puedan calcularse exactamente.

Las instrucciones deben indicar al estudiante qué estrategia utilizar.

Para este nivel, evita dejar completamente abierta la decisión.

Selecciona estrategias sencillas como:

- llenar con la media;
- llenar con la mediana;
- llenar con la moda;
- llenar con el valor más frecuente;
- asignar “Desconocido”;
- conservar el valor vacío y documentarlo.

Explica brevemente por qué esa estrategia es apropiada.

Ejemplo:

“Algunos registros no contienen la calificación de satisfacción. Calcula la mediana de los valores disponibles y úsala para completar los faltantes. La mediana es conveniente porque reduce el efecto de valores extremos.”

No utilices técnicas estadísticas avanzadas.

---

# 18. USO DE IF

Incluye al menos una tarea sencilla donde pueda utilizarse:

`IF()` / `SI()`

Ejemplos:

clasificar una venta como:

`Alta`

`Media`

`Baja`

o clasificar una entrega como:

`A tiempo`

`Retrasada`

La condición debe ser sencilla y fácil de interpretar.

---

# 19. DUPLICADOS

Todos los proyectos deben contener duplicados deliberados.

Incluye aproximadamente:

- 3 a 5 duplicados si el dataset tiene 100 registros;
- una cantidad proporcional si contiene más registros.

Pueden ser duplicados completos.

Pide al estudiante:

1. identificar cuántos duplicados existen;
2. eliminarlos de `Datos_Limpios`;
3. conservar `Datos_Originales` intacto;
4. documentar cuántos eliminó en `Informe_Ejecutivo`.

Puedes utilizar:

**Datos → Quitar duplicados**

o la herramienta equivalente.

---

# 20. MÉTRICAS DE INTERÉS

Solicita entre **5 y 8 métricas sencillas**.

Las métricas deben estar relacionadas directamente con las preguntas del negocio.

Prioriza cálculos que puedan resolverse utilizando:

### COUNT()

### COUNTA()

### COUNTIF()

### SUM()

### AVERAGE()

### MAX()

### MIN()

Puedes incluir operaciones aritméticas básicas.

No requieras fórmulas avanzadas.

No requieras tablas dinámicas.

No requieras SUMIFS, XLOOKUP, INDEX/MATCH u otras funciones avanzadas salvo que se soliciten explícitamente en los parámetros.

Formula las métricas como preguntas de negocio.

Por ejemplo:

“¿Cuál fue el monto total de ventas?”

“¿Cuál fue el valor promedio por operación?”

“¿Cuál fue la venta más alta?”

“¿Cuántas operaciones pertenecen a la categoría X?”

“¿Qué porcentaje de registros corresponde a determinada clasificación?”

---

# 21. ANÁLISIS

La hoja `Analisis` debe contener las preguntas y dejar vacías las respuestas.

Ejemplo:

| # | Pregunta | Función sugerida | Resultado |
|---|---|---|---|
| 1 | ¿Cuál es el monto total? | SUM | |
| 2 | ¿Cuál es el valor promedio? | AVERAGE | |
| 3 | ¿Cuál es el valor máximo? | MAX | |
| 4 | ¿Cuántos registros son categoría A? | COUNTIF | |

La columna de función sugerida puede orientar al estudiante sin entregar la fórmula completa.

---

# 22. VISUALIZACIONES

Solicita entre **3 y 4 gráficas sencillas**.

Cada gráfica debe responder una pregunta concreta.

Utiliza principalmente:

- barras;
- columnas;
- líneas;
- circular/pastel cuando existan pocas categorías;
- dispersión únicamente si resulta muy intuitiva.

Evita visualizaciones avanzadas.

Para cada gráfica proporciona:

**Título sugerido**

**Pregunta que responde**

**Datos que debe utilizar**

**Tipo de gráfica recomendado**

Ejemplo:

### Ventas por categoría

Pregunta:

¿Qué categorías generan mayor monto de ventas?

Datos:

Categoría y ventas totales.

Tipo:

Gráfico de columnas.

---

# 23. RESUMEN EJECUTIVO

El proyecto debe finalizar con un resumen ejecutivo sencillo.

El estudiante deberá completar en `Informe_Ejecutivo`:

### Calidad de los datos

- número de registros originales;
- duplicados encontrados;
- duplicados eliminados;
- valores faltantes encontrados;
- valores faltantes recuperados;
- principales problemas de formato encontrados.

### Resultados

Debe reportar las métricas más importantes.

### Hallazgos

Debe escribir entre **3 y 5 hallazgos**.

Ejemplo:

“La categoría X concentró la mayor cantidad de ventas.”

No aceptar únicamente números sin interpretación.

### Recomendaciones

Debe incluir entre **1 y 2 recomendaciones sencillas** basadas en los resultados.

---

# 24. ARCHIVO DEL INSTRUCTOR

Genera:

`Proyecto_[nombre]_Solucion.xlsx`

Debe contener exactamente los mismos datos y estructura que el archivo del estudiante, pero completamente resuelto.

## Datos_Originales

Debe ser idéntico al archivo del estudiante.

## Datos_Limpios

Debe contener:

- datos limpios;
- formatos corregidos;
- valores inconsistentes estandarizados;
- valores recuperados;
- valores faltantes tratados;
- duplicados eliminados;
- columnas calculadas;
- resultados de las funciones solicitadas.

Siempre que sea razonable, conserva las **fórmulas utilizadas** en lugar de reemplazarlas por valores estáticos.

## Analisis

Incluye:

- fórmulas;
- resultados correctos;
- métricas completas.

## Visualizaciones

Incluye las gráficas terminadas.

Deben tener:

- título claro;
- etiquetas apropiadas;
- leyenda cuando sea necesaria;
- formato legible.

## Informe_Ejecutivo

Incluye una respuesta modelo completa con:

- problemas encontrados;
- cantidad de duplicados;
- cantidad de valores faltantes;
- cantidad recuperada;
- métricas;
- hallazgos;
- recomendaciones.

Añade además una hoja:

### Guia_Instructor

Incluye una tabla con:

| Elemento | Respuesta esperada |
|---|---|

Documenta:

- número original de registros;
- número de duplicados introducidos;
- columnas con problemas;
- número de valores faltantes por columna;
- método utilizado para recuperar cada tipo de faltante;
- reemplazos esperados;
- métricas correctas;
- principales conclusiones esperadas.

Esta hoja debe existir solamente en la versión del instructor.

---

# 25. DISEÑO DEL DATASET

Construye primero, **solo como referencia interna**, un dataset completamente correcto.

Llama conceptualmente a esta versión `dataset_base_limpio`. Esta versión sirve únicamente para validar coherencia, calcular la solución y conocer los valores correctos esperados. **No debe copiarse directamente al archivo del estudiante.**

Después crea una segunda versión, `dataset_sucio`, introduciendo deliberadamente los problemas de calidad.

El `dataset_sucio` es el que debe escribirse en el archivo del estudiante, tanto en `Datos_Originales` como en el estado inicial de `Datos_Limpios`.

El archivo solucionado del instructor debe comenzar con el mismo `dataset_sucio` en `Datos_Originales` y mostrar en `Datos_Limpios` el resultado de aplicar las correcciones.

Esto es importante para evitar errores accidentales y, al mismo tiempo, garantizar que el estudiante tenga problemas reales que resolver.

El `dataset_base_limpio` debe mantener relaciones matemáticas coherentes y utilizarse como referencia para validar que las transformaciones del instructor son correctas.

### Persistencia real de los errores en el archivo

Los errores no deben existir únicamente en una estructura interna durante la generación: deben quedar **materializados en las celdas del `.xlsx` entregado al estudiante**.

Ejemplos:

- un número que deba estar almacenado como texto debe escribirse realmente como texto;
- una fecha inconsistente puede escribirse como texto en el formato incorrecto definido para el ejercicio;
- los espacios adicionales deben existir realmente en el valor de la celda;
- los valores faltantes deben ser celdas vacías cuando corresponda;
- los duplicados deben aparecer como filas duplicadas reales;
- las variantes categóricas deben conservar exactamente la variante incorrecta introducida.

No permitas que el proceso de exportación a Excel corrija o normalice automáticamente estos errores.

---

# 26. DISTRIBUCIÓN DE PROBLEMAS

Para un dataset estándar de 100 registros utiliza aproximadamente:

- 5 duplicados completos;
- 5 a 10 problemas de espacios o formato de texto;
- 5 a 10 categorías inconsistentes;
- 4 a 8 problemas de formato numérico;
- 4 a 8 fechas inconsistentes, cuando existan fechas;
- 3 a 5 valores faltantes recuperables de un primer tipo;
- 3 a 5 valores faltantes recuperables de un segundo tipo;
- 2 a 4 valores faltantes no recuperables directamente.

Una misma fila puede contener más de un problema, pero evita concentrar todos los errores en pocas filas.

La mayor parte de los datos debe ser correcta.

Ajusta proporcionalmente estas cantidades si se solicita un número diferente de registros.

---

# 27. REGLAS DE CALIDAD DEL DATASET

Antes de generar los archivos verifica internamente que:

1. todas las columnas mencionadas en las instrucciones existen;
2. todas las tareas pueden resolverse con los datos proporcionados;
3. todos los valores faltantes recuperables realmente pueden calcularse;
4. no existe división entre cero;
5. las relaciones matemáticas son correctas;
6. todos los duplicados intencionales son detectables;
7. las categorías inconsistentes tienen una correspondencia clara;
8. las fechas pertenecen al periodo indicado;
9. las métricas pueden calcularse después de la limpieza;
10. todas las gráficas solicitadas pueden construirse;
11. los resultados del archivo solucionado corresponden al dataset;
12. el archivo del estudiante no contiene las respuestas;
13. la hoja `Datos_Originales` es idéntica en ambas versiones;
14. `Datos_Originales` del estudiante contiene realmente el `dataset_sucio`, no el `dataset_base_limpio`;
15. `Datos_Limpios` del estudiante comienza como una copia exacta del `dataset_sucio`;
16. los errores deliberados siguen presentes al abrir el archivo del estudiante;
17. la versión del estudiante no contiene fórmulas, valores o transformaciones que resuelvan anticipadamente la limpieza;
18. la versión del instructor resuelve exactamente los problemas presentes en el archivo del estudiante;
19. si la herramienta seleccionada es Google Sheets, el `.xlsx` utiliza únicamente funciones, formatos y gráficos compatibles con Google Sheets y puede importarse sin perder la lógica principal del ejercicio.

No describas esta validación interna al estudiante.

---

# 28. ESTILO DE LAS INSTRUCCIONES

Escribe las instrucciones como un proyecto educativo profesional.

Utiliza lenguaje claro y directo.

Explica qué debe hacer el estudiante.

Cuando sea útil, proporciona pistas y funciones sugeridas.

Ejemplo:

**Función útil: TRIM() / ESPACIOS()**

Cuando la tarea sea recuperar un valor faltante, proporciona explícitamente la relación necesaria.

Ejemplo:

**Para recuperar Precio unitario utiliza:**

`Precio unitario = Monto total / Cantidad`

No entregues directamente los resultados numéricos en las instrucciones del estudiante.

---

# 29. PROGRESIÓN ESPERADA

Organiza el proyecto aproximadamente de esta manera:

### Parte 1 — Exploración y diagnóstico
15 % del tiempo.

### Parte 2 — Limpieza y preparación
45 % del tiempo.

### Parte 3 — Métricas y análisis
20 % del tiempo.

### Parte 4 — Visualizaciones
10 % del tiempo.

### Parte 5 — Informe ejecutivo
10 % del tiempo.

Adapta el número de tareas a la duración objetivo indicada.

---

# 30. RESTRICCIONES

No conviertas el proyecto en un ejercicio avanzado.

No utilices:

- macros;
- VBA;
- Power Query;
- Power Pivot;
- SQL;
- Python;
- R;
- machine learning;
- análisis estadístico avanzado;
- dashboards complejos;
- fórmulas matriciales avanzadas.

El foco debe permanecer en:

**limpiar → validar → resumir → visualizar → comunicar.**

---

# 30A. COMPATIBILIDAD CON GOOGLE SHEETS

Si `HERRAMIENTA = Google Sheets`, mantén los mismos tres entregables y genera los archivos de trabajo en formato `.xlsx`.

El estudiante deberá poder subir `Proyecto_[nombre]_Estudiante.xlsx` a Google Drive y abrirlo con Google Sheets para realizar el proyecto.

En este modo:

1. utiliza funciones disponibles en Google Sheets, priorizando `TRIM`, `LOWER`, `UPPER`, `PROPER`, `IF`, `COUNT`, `COUNTA`, `COUNTIF`, `SUM`, `AVERAGE`, `MAX` y `MIN`;
2. para dividir texto, puedes recomendar `SPLIT()` en Google Sheets y mencionar `TEXTSPLIT()` o “Texto en columnas” como equivalente de Excel cuando corresponda;
3. evita tablas estructuradas de Excel, referencias estructuradas, macros, VBA, Power Query, Power Pivot y características que dependan exclusivamente del motor de Excel;
4. utiliza gráficos básicos que Google Sheets pueda recrear o importar: barras, columnas, líneas y circular;
5. conserva fórmulas en la versión del instructor siempre que sean compatibles con Google Sheets;
6. en las instrucciones del estudiante, adapta los nombres de menús o acciones cuando Excel y Google Sheets difieran;
7. el hecho de seleccionar Google Sheets **no cambia el formato de entrega**: se siguen generando archivos `.xlsx`, no archivos nativos `.gsheet`.

Si `HERRAMIENTA = Excel`, utiliza las instrucciones normales de Excel descritas en este prompt.

---

# 31. RESULTADO FINAL

Al finalizar la ejecución de este prompt debes entregar los tres archivos descargables:

1. `Proyecto_[nombre]_Instrucciones.md`
2. `Proyecto_[nombre]_Estudiante.xlsx`
3. `Proyecto_[nombre]_Solucion.xlsx`

Antes de entregar, verifica que los archivos puedan abrirse correctamente y que la versión solucionada corresponda exactamente con las tareas planteadas en la versión del estudiante.

Verifica específicamente que:

- el archivo del estudiante conserve los errores deliberados y permita ejecutar realmente las tareas de limpieza;
- el archivo solucionado parta de los mismos datos sucios y muestre las correcciones correctas;
- si la herramienta es Google Sheets, ambos `.xlsx` sean compatibles con su importación y uso en Google Sheets.

No generes únicamente una descripción de los archivos: **crea los archivos reales**.