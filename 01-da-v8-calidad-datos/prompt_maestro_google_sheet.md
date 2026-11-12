# PARÁMETROS DEL PROYECTO
- **Sector / Temática:** [Ej. E-commerce de moda / Logística / Clínica dental]
- **País o Región:** [Ej. México / Colombia / España (o "Automático")]
- **Periodo de análisis:** [Ej. Q1 2026 / Enero-Marzo 2026 (o "Automático")]
- **Número de registros:** [Por defecto: 50 | Recomendado en Sheets: 40 a 80 para evitar cortes]
- **Modo de entrega:** [Plantilla Estudiante / Solución Instructor]

---

# ROL Y OBJETIVO
Actúa como diseñador instruccional y analista de datos senior. Crea un caso práctico de limpieza y análisis de datos en Google Sheets para un analista de datos junior (nivel básico-intermedio). 

**Restricciones técnicas:** Usa únicamente funciones nativas básicas compatibles con Google Sheets (`TRIM/ESPACIOS`, `LOWER/MINUSC`, `UPPER/MAYUSC`, `PROPER/NOMPROPIO`, `SPLIT`, `IF/SI`, `COUNT/CONTAR`, `COUNTA/CONTARA`, `COUNTIF/CONTAR.SI`, `SUM/SUMA`, `AVERAGE/PROMEDIO`, `MAX`, `MIN`) y herramientas de menú (Quitar duplicados, Buscar y reemplazar). Prohibido usar SQL, tablas dinámicas, macros, `XLOOKUP/BUSCARX` o `SUMIFS/SUMAR.SI.CONJUNTO`. Todos los datos deben ser 100% sintéticos.

---

# ESTRUCTURA DE SALIDA (6 TABLAS PARA GOOGLE SHEETS)
Genera el proyecto dividido en las siguientes **6 secciones exactas**. Presenta el contenido de cada sección como una **tabla independiente** para poder insertarla directamente en cada pestaña de Google Sheets:

### 1) Pestaña: `descripcion_problema`
Genera una tabla de dos columnas (`Sección | Detalle`) que incluya:
- **Contexto de negocio:** Nombre de la empresa ficticia, departamento solicitante, problema de negocio y qué decisión se busca tomar.
- **El Desafío:** Resumen general de los problemas de calidad presentes en el archivo.
- **Guía paso a paso de limpieza:** Instrucciones claras de lo que debe hacer el usuario:
  1. Qué variantes de texto/categorías estandarizar y a qué valor oficial.
  2. Qué columna dividir con `SPLIT()`.
  3. **Faltantes recuperables (Tipo A):** Las 2 fórmulas matemáticas exactas para reconstruir celdas vacías a partir de otras columnas (ej. `Monto = Precio * Cantidad`).
  4. **Faltantes no recuperables (Tipo B):** Qué estrategia simple aplicar (media, mediana, moda o "Desconocido") y por qué.
  5. **Clasificación lógica:** La regla exacta para crear una columna nueva usando `IF() / SI()`.

### 2) Pestaña: `raw`
Genera la tabla completa de datos sucios. El 80-85% de las filas deben ser correctas y el **15-20% debe contener errores deliberados y materializados en las celdas**:
- **Duplicados:** hasta 15% de filas completamente duplicadas.
- **Texto sucio:** Espacios extra, mezcla de mayúsculas/minúsculas y 1 columna con datos combinados para separar.
- **Categorías inconsistentes:** 2 a 3 columnas con variantes mal escritas o abreviadas (ej. `MTY`, `monterrey`, `Monterrey `).
- **Formatos:** Números guardados como texto o con símbolos mezclados, y fechas en distintos formatos (`dd/mm/aaaa`, `aaaa-mm-dd`, `15-Mar-2026`).
- **Valores faltantes (celdas vacías):**
  - *Tipo A (Recuperables):* 3 a 5 celdas vacías en al menos 2 columnas numéricas que puedan calcularse exactamente con otras columnas presentes en la misma fila.
  - *Tipo B (No recuperables):* 2 a 4 celdas vacías para imputar con estadística básica o etiqueta.
*(Nota crítica: Entrega todas las filas solicitadas sin abreviar ni truncar la tabla).*

### 3) Pestaña: `analisis`
Genera una tabla con las columnas: `# | Pregunta de Negocio | Función Sugerida (EN / ES) | Resultado`.
- Incluye de **5 a 8 preguntas de negocio** que se respondan con `SUM`, `AVERAGE`, `MAX`, `MIN`, `COUNT`, `COUNTA`, `COUNTIF` o aritmética básica.
- Si el Modo es **Plantilla Estudiante**, deja la columna `Resultado` vacía. Si es **Solución Instructor**, incluye la fórmula y el valor correcto (calculado sobre los datos ya limpios).

### 4) Pestaña: `visualizaciones`
Genera una tabla de especificaciones para **3 a 4 gráficas básicas** (columnas, barras, líneas o circular) con las columnas: `# Gráfica | Título Sugerido | Pregunta de Negocio que Responde | Columnas / Datos a Utilizar | Tipo de Gráfico Recomendado`.

### 5) Pestaña: `reporte_ejecutivo`
Genera una plantilla en formato tabla (`Sección | Campo | Respuesta`) que contenga:
- **Auditoría de Calidad:** Registros originales, Duplicados eliminados, Faltantes encontrados, Faltantes recuperados y Principales problemas corregidos.
- **Métricas Clave:** Resumen de los 3 indicadores principales.
- **Conclusiones:** Espacio para 3 Hallazgos interpretados y 2 Recomendaciones accionables de negocio (vacíos en modo Estudiante; contestados en modo Instructor).

### 6) Pestaña: `diccionario_datos`
Genera una tabla con las columnas: `Columna | Descripción | Tipo de Dato Esperado | Ejemplo Correcto | Regla de Limpieza Aplicable`. Describe todas las columnas de `datos_crudos` y las columnas calculadas solicitadas.