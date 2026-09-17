# Proyecto: Control de producción de discos duros y memorias — TecnoMem 2020

## Introducción

Eres analista de datos junior en **AndeByte Components**, una empresa ficticia dedicada a fabricar componentes de almacenamiento y memoria para equipos de cómputo: discos duros HDD, unidades SSD y módulos de memoria RAM.

El área de **Operaciones de Manufactura** te entregó un archivo con registros de lotes producidos en distintas plantas de Latinoamérica durante **2020**. Antes de utilizar la información en una reunión de cierre anual, el gerente necesita confirmar que los datos son consistentes, eliminar registros duplicados, recuperar algunos valores faltantes y obtener un resumen sencillo de volumen, costo y calidad.

El archivo proviene de varias capturas manuales y exportaciones de sistemas internos, por lo que contiene errores de formato e inconsistencias. Tu trabajo apoyará una decisión operativa: **identificar el tamaño de la producción anual, revisar el costo acumulado y detectar qué proporción de lotes requiere atención por calidad**.

---

# El desafío

La información recibida no está lista para analizarse. Durante tu exploración encontrarás problemas como:

- formatos de fecha inconsistentes;
- números almacenados como texto;
- espacios adicionales;
- uso irregular de mayúsculas y minúsculas;
- nombres equivalentes escritos de distintas maneras;
- valores faltantes;
- valores faltantes que pueden recuperarse con otras columnas;
- registros duplicados;
- una columna que combina dos datos y debe separarse.

No se indican todas las filas problemáticas. Parte del ejercicio consiste en descubrirlas mediante filtros, ordenamientos y revisión visual.

---

## Contexto del negocio

**AndeByte Components** fabrica HDD, SSD y memoria RAM en plantas distribuidas en Latinoamérica.

El dataset representa lotes de producción registrados durante 2020. Cada fila corresponde a un lote e incluye información como fecha, planta, país, producto, línea/turno, supervisor, unidades producidas, costo y unidades defectuosas.

La pregunta principal del negocio es:

> **¿Qué volumen se produjo durante 2020, cuánto costó esa producción y cuántos lotes requieren revisión por una tasa de defectos superior al nivel aceptable?**

El responsable de Operaciones espera obtener conclusiones sobre:

- cantidad de lotes y unidades producidas;
- costo total y costo unitario promedio;
- lotes con mayor volumen;
- distribución por tipo de producto;
- cantidad de lotes que requieren revisión de calidad;
- volumen producido por planta.

---

## Archivos proporcionados

Recibirás:

`DA-S1-L3-TechnoMem`

El archivo contiene cinco hojas:

- `Datos_Originales`: copia del dataset crudo. **No debes modificarla.**
- `Datos_Limpios`: copia inicial del mismo dataset sucio. Aquí realizarás la limpieza.
- `Analisis`: plantilla para calcular métricas.
- `Visualizaciones`: espacios y tablas auxiliares para preparar tres gráficas.
- `Informe_Ejecutivo`: plantilla para comunicar los resultados.

---

## Descripción de los datos

| Columna | Descripción | Tipo esperado | Ejemplo |
|---|---|---|---|
| ID_Lote | Identificador único del lote de producción | Texto | LT-2020-001 |
| Fecha_Produccion | Fecha en que se registró el lote | Fecha | 03/01/2020 |
| Planta | Ciudad de la planta de manufactura | Texto categórico | Monterrey |
| Pais | País donde se encuentra la planta | Texto categórico | México |
| Codigo_Producto | Código interno del producto | Texto | SSD-512-N |
| Categoria | Tipo de componente fabricado | Texto categórico | SSD |
| Linea_Turno | Línea y turno en un solo campo, separados por `|` | Texto | L2 \| Tarde |
| Supervisor | Responsable operativo del lote | Texto | Ana Torres |
| Unidades_Producidas | Cantidad de unidades producidas | Número entero | 1200 |
| Costo_Unitario_USD | Costo de producción por unidad | Número decimal / moneda | 39.50 |
| Costo_Total_USD | Costo total del lote | Número decimal / moneda | 47400.00 |
| Unidades_Defectuosas | Unidades defectuosas detectadas | Número entero | 24 |
| Linea | Columna auxiliar para separar `Linea_Turno` | Texto | L2 |
| Turno | Columna auxiliar para separar `Linea_Turno` | Texto | Tarde |
| Tasa_Defectos | Unidades defectuosas / unidades producidas | Porcentaje | 2.00% |
| Nivel_Calidad | Clasificación del lote con una condición `IF()` / `SI()` | Texto | Aceptable |

---

## Objetivos del proyecto

Al finalizar deberás demostrar que puedes:

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

# Parte 1 — Exploración y diagnóstico

1. Abre `Datos_Originales` y revisa las columnas y formatos.
2. Confirma el número de registros recibidos.
3. Usa filtros para revisar valores distintos en `Planta`, `Pais` y `Categoria`.
4. Busca celdas vacías en columnas numéricas.
5. Identifica fechas que no tengan el mismo formato que el resto.
6. Identifica valores numéricos que estén almacenados como texto.
7. Revisa si existen registros duplicados completos.
8. No modifiques `Datos_Originales`. Trabaja únicamente en `Datos_Limpios`.

---

# Parte 2 — Limpieza y preparación

## 1. Limpiar texto

Aplica técnicas de limpieza en `Datos_Limpios`.

### Código de producto
El valor esperado debe estar **sin espacios al inicio/final y en mayúsculas**.

Funciones útiles:

- `TRIM()` / `ESPACIOS()`
- `UPPER()` / `MAYUSC()`

Ejemplo conceptual:

`" ssd-512-n "` → `SSD-512-N`

### Supervisor
Los nombres deben quedar sin espacios extra y con formato de nombre propio.

Funciones útiles:

- `TRIM()` / `ESPACIOS()`
- `PROPER()` / `NOMPROPIO()`

### Estandarizar categorías

Utiliza Buscar y reemplazar, filtros o edición controlada para dejar únicamente los valores correctos siguientes.

**Planta**

- `SAN JOSE`, `San Jose` o `SJO` → `San José`
- `guadalajara`, `GDL` → `Guadalajara`
- las demás plantas deben conservar su nombre estándar: `Monterrey`, `Bogotá`, `Lima`, `São Paulo`

**País**

- `mexico`, `MEX` → `México`
- `BRASIL` → `Brasil`
- los demás valores esperados son `Colombia`, `Perú` y `Costa Rica`

**Categoría**

- `hdd` o variantes con espacios → `HDD`
- `solid state` → `SSD`
- `Memoria RAM` → `RAM`

Puedes usar también `LOWER()` / `MINUSC()` para comparar variantes antes de reemplazarlas.

## 2. Separar Línea y Turno

La columna `Linea_Turno` contiene dos datos separados por el carácter `|`.

Completa las columnas auxiliares `Linea` y `Turno`.

Puedes utilizar:

- **Datos → Texto en columnas** en Excel;
- `TEXTSPLIT()` en versiones compatibles de Excel.

Asegúrate de eliminar espacios sobrantes después de dividir.

## 3. Corregir fechas

Convierte todas las fechas de `Fecha_Produccion` a valores de fecha reales y aplica un formato único:

`dd/mm/aaaa`

Todas las fechas válidas del ejercicio pertenecen a 2020.

## 4. Corregir números almacenados como texto

Revisa:

- `Unidades_Producidas`
- `Costo_Unitario_USD`
- `Costo_Total_USD`
- `Unidades_Defectuosas`

Convierte a número cualquier valor numérico almacenado como texto.

Aplica los siguientes formatos:

- `Unidades_Producidas`: número entero;
- `Costo_Unitario_USD`: moneda USD con dos decimales;
- `Costo_Total_USD`: moneda USD con dos decimales;
- `Unidades_Defectuosas`: número entero.

## 5. Identificar y eliminar duplicados

1. Identifica cuántos registros duplicados completos existen.
2. Elimínalos únicamente de `Datos_Limpios`.
3. Mantén `Datos_Originales` intacto.
4. Registra la cantidad eliminada en `Informe_Ejecutivo`.

Puedes usar **Datos → Quitar duplicados** seleccionando todas las columnas originales.

## 6. Recuperar valores faltantes

Existen dos tipos de faltantes que pueden reconstruirse exactamente.

### Tipo A — Costo unitario faltante

Cuando `Costo_Unitario_USD` esté vacío y existan `Costo_Total_USD` y `Unidades_Producidas`, utiliza:

`Costo_Unitario_USD = Costo_Total_USD / Unidades_Producidas`

### Tipo B — Costo total faltante

Cuando `Costo_Total_USD` esté vacío y existan `Costo_Unitario_USD` y `Unidades_Producidas`, utiliza:

`Costo_Total_USD = Costo_Unitario_USD × Unidades_Producidas`

No reemplaces con cero los valores faltantes.

## 7. Tratar faltantes no recuperables directamente

Algunos registros no contienen `Unidades_Defectuosas`.

Después de eliminar duplicados:

1. calcula la **mediana** de los valores disponibles de `Unidades_Defectuosas`;
2. utiliza esa mediana para completar los faltantes.

Función útil:

`MEDIAN()` / `MEDIANA()`

La mediana es apropiada porque proporciona un valor central sencillo y reduce el efecto de valores extremos.

## 8. Calcular la tasa de defectos

En `Tasa_Defectos`, utiliza:

`Tasa_Defectos = Unidades_Defectuosas / Unidades_Producidas`

Aplica formato de porcentaje con dos decimales.

## 9. Clasificar la calidad con IF

En `Nivel_Calidad`, clasifica cada lote así:

- si `Tasa_Defectos <= 2%` → `Aceptable`
- si `Tasa_Defectos > 2%` → `Revisar`

Función útil:

`IF()` / `SI()`

---

# Parte 3 — Métricas y análisis

Dedica aproximadamente **12 minutos**.

Completa la hoja `Analisis`. Calcula las siguientes preguntas de negocio sin usar tablas dinámicas.

1. ¿Cuántos lotes únicos quedan después de la limpieza?  
   Función sugerida: `COUNTA()` / `CONTARA()`

2. ¿Cuántas unidades se produjeron en total?  
   Función sugerida: `SUM()` / `SUMA()`

3. ¿Cuál fue el costo total de producción?  
   Función sugerida: `SUM()` / `SUMA()`

4. ¿Cuál fue el costo unitario promedio por lote?  
   Función sugerida: `AVERAGE()` / `PROMEDIO()`

5. ¿Cuál fue la mayor cantidad de unidades producidas en un solo lote?  
   Función sugerida: `MAX()`

6. ¿Cuántos lotes requieren revisión de calidad?  
   Función sugerida: `COUNTIF()` / `CONTAR.SI()`

7. ¿Cuántos lotes pertenecen a la categoría SSD?  
   Función sugerida: `COUNTIF()` / `CONTAR.SI()`

---

# Parte 4 — Visualizaciones

Dedica aproximadamente **6 minutos**.

Completa las tablas auxiliares de `Visualizaciones` y crea tres gráficas.

## Gráfica 1: Lotes por categoría

**Pregunta que responde:**  
¿Cómo se distribuyen los lotes entre HDD, SSD y RAM?

**Datos que debe utilizar:**  
Categoría y cantidad de lotes.

**Función sugerida para preparar la tabla:**  
`COUNTIF()` / `CONTAR.SI()`

**Tipo de gráfica recomendado:**  
Gráfico de columnas.

## Gráfica 2: Estado de calidad de los lotes

**Pregunta que responde:**  
¿Qué proporción de lotes es aceptable y qué proporción requiere revisión?

**Datos que debe utilizar:**  
`Nivel_Calidad` y cantidad de lotes.

**Función sugerida:**  
`COUNTIF()` / `CONTAR.SI()`

**Tipo de gráfica recomendado:**  
Gráfico circular.

## Gráfica 3: Unidades producidas por planta

**Pregunta que responde:**  
¿Qué plantas concentraron mayor volumen de unidades producidas?

**Datos que debe utilizar:**  
Planta y suma de `Unidades_Producidas`.

**Función sugerida:**  
`SUMIF()` / `SUMAR.SI()`

**Tipo de gráfica recomendado:**  
Gráfico de barras.

---

# Parte 5 — Informe ejecutivo

Dedica aproximadamente **5 minutos**.

Completa `Informe_Ejecutivo`.

## Calidad de los datos

Documenta:

- número de registros originales;
- duplicados encontrados;
- duplicados eliminados;
- valores faltantes encontrados;
- valores faltantes recuperados mediante relaciones matemáticas;
- valores faltantes tratados mediante mediana;
- principales problemas de formato encontrados.

## Resultados

Incluye las métricas más importantes calculadas en `Analisis`.

## Hallazgos

Escribe entre **3 y 5 hallazgos**. No escribas únicamente números: interpreta qué significan.

Ejemplo de estructura:

> “La categoría ___ concentró la mayor cantidad de lotes, lo que indica que…”

## Recomendaciones

Incluye **1 o 2 recomendaciones sencillas** basadas en tus resultados.

Piensa en acciones como:

- priorizar la revisión de lotes con alta tasa de defectos;
- mejorar las reglas de captura para reducir inconsistencias;
- revisar la distribución de producción entre plantas.

---

## Criterios de entrega

Antes de terminar verifica que:

- `Datos_Originales` no haya sido modificado;
- `Datos_Limpios` no tenga duplicados completos;
- las categorías estén estandarizadas;
- las fechas tengan formato `dd/mm/aaaa`;
- las columnas numéricas sean realmente numéricas;
- los faltantes recuperables se hayan reconstruido correctamente;
- los faltantes de defectos se hayan tratado con la mediana;
- `Tasa_Defectos` y `Nivel_Calidad` estén completas;
- las siete métricas estén calculadas;
- existan tres gráficas;
- el informe ejecutivo incluya interpretación y recomendaciones.
