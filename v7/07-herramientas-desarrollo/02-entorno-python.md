# 🛠️ Trabajando con Python y el Entorno de Desarrollo 🐍🚀

¡Hola! Te damos la bienvenida al segundo webinar del módulo de herramientas de desarrollo. En esta sesión práctica, daremos el salto de trabajar en cuadernos aislados a estructurar un **proyecto real de Python** de manera local en tu computadora. 

Aprenderás a estructurar carpetas, gestionar dependencias con entornos virtuales, interactuar con Inteligencia Artificial utilizando prompts profesionales para generar código, y finalmente, crear una **aplicación interactiva web** usando **Streamlit**.

---

## 🎯 Objetivos de la Sesión

Al finalizar este webinar, serás capaz de:
*   **Estructurar proyectos de desarrollo** de forma limpia y profesional.
*   **Crear y activar entornos virtuales** en Python para el control de dependencias.
*   **Diseñar prompts efectivos** para automatizar la escritura de scripts y aplicaciones.
*   **Escribir y ejecutar scripts** de Python desde la terminal.
*   **Crear e interactuar con Jupyter Notebooks** organizados dentro de un proyecto.
*   **Construir un panel interactivo (Dashboard)** con Streamlit para la visualización de tus análisis.

---

## 📂 1. Estructura de un Proyecto Profesional

Antes de escribir una sola línea de código, necesitamos organizar nuestra área de trabajo. Trabajar de forma profesional requiere estructurar nuestro proyecto para que otros (y nosotros mismos en el futuro) entiendan dónde está cada componente.

### 📐 La Estructura en Formato ASCII

Crea una carpeta raíz en tu computadora llamada `mi-proyecto-datos` y dentro de ella crea la siguiente estructura de archivos y carpetas:

```text
mi-proyecto-datos/
├── data/              # Archivos de datos (CSV, JSON, datasets, etc.)
├── notebooks/         # Cuadernos de Jupyter para análisis exploratorio (EDA)
├── prompts/           # Plantillas de texto y prompts enviados a la IA
├── scripts/           # Archivos .py de automatización y procesos
├── app.py             # Archivo principal de nuestra aplicación Streamlit
└── requirements.txt   # Listado de librerías necesarias para el proyecto
```


### 📂 ¿Qué contendrá cada carpeta?
*   `prompts/`: Guardaremos plantillas de instrucciones textuales (prompts) que usaremos con la IA para generar código. Esto nos permite documentar cómo generamos nuestro código.
*   `scripts/`: Guardaremos scripts de automatización de Python (por ejemplo, para generar datos o descargar archivos).
*   `notebooks/`: Guardaremos los cuadernos de Jupyter para análisis de datos interactivos y visualizaciones rápidas.
*   `data/`: Para almacenar archivos de entrada y salida (como archivos CSV).
*   `requirements.txt`: Para registrar todas las librerías externas que instalemos y asegurar la replicabilidad.
*   `app.py`: El punto de entrada de nuestra aplicación visual e interactiva con Streamlit.

---

## 🧰 2. Entorno Virtual: Tu Aislante de Trabajo

Para que nuestro proyecto funcione correctamente y no interfiera con otros programas o proyectos de tu computadora, crearemos un entorno virtual.

### Paso 1: Crear el entorno
Ejecuta el siguiente comando en la raíz de tu proyecto para crear la carpeta aislada `.venv`:

```bash
python -m virtualenv .venv
```
*(Este comando le pide a Python que use el módulo `virtualenv` para crear una carpeta llamada `.venv` donde se guardará nuestro entorno aislado).*

> 💡 **Nota:** Si la terminal te indica que `virtualenv` no está instalado, puedes instalarlo primero con `pip install virtualenv` o utilizar el módulo integrado de Python ejecutando: `python -m venv .venv`.

### Activar el entorno virtual ⚡
Crear el entorno no es suficiente; debemos entrar en él (activarlo). El comando varía según tu sistema operativo:

*   **En Windows (usando GitBash):**
    ```bash
    source .venv/Scripts/activate
    ```
*   **En macOS y Linux (Terminal):**
    ```bash
    source .venv/bin/activate
    ```

**¿Cómo saber si funcionó?**
Notarás que al inicio de tu línea de comandos en la terminal aparecerá el nombre del entorno entre paréntesis, por ejemplo:
`(.venv) usuario@computadora:~$`

---

## 📝 3. Generando Datos con Inteligencia Artificial (Prompts)

Usar Inteligencia Artificial para acelerar tu desarrollo es una habilidad clave. En lugar de escribir un código de simulación desde cero, vamos a diseñar un prompt que le pida a la IA que cree el script por nosotros.

### 🤖 El Prompt de Generación de Datos
Crea un archivo llamado `prompts/generar_data.md` y guarda en él la siguiente instrucción para la IA:

```text
Actúa como un desarrollador experto en Python para ciencia de datos. Escribe un script de Python generate_data.py que genere un conjunto de datos ficticio sobre ventas de una tienda en línea. El script debe:
1. Generar 200 filas de datos aleatorios.
2. Contener las columnas:
   - ID_Pedido (con formato PED-001, PED-002...)
   - Fecha (dentro del último mes)
   - Producto (a elegir entre: Laptop, Smartphone, Tablet, Auriculares, Monitor)
   - Categoria (a elegir entre: Electrónica, Accesorios)
   - Cantidad (entero aleatorio entre 1 y 5)
   - Precio_Unitario (valor decimal adecuado al producto)
   - Total (calculado como Cantidad * Precio_Unitario)
3. Guardar el dataframe resultante como un archivo CSV en data/ventas.csv.
4. Asegurar que los datos sean lógicos (por ejemplo, que una Laptop siempre tenga el mismo precio unitario).
5. Usar pandas y numpy. Imprimir un mensaje al finalizar indicando que el archivo se ha creado.
```

### 📄 El Script Resultante: `scripts/generate_data.py`
Envía el prompt a la IA de tu elección y guarda el script generado en `scripts/generate_data.py`. A continuación tienes una versión de referencia robusta:

```python
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Configurar semilla para reproducibilidad
np.random.seed(42)

# Productos y precios base preestablecidos
productos_info = {
    "Laptop": ("Electrónica", 800.0),
    "Smartphone": ("Electrónica", 500.0),
    "Tablet": ("Electrónica", 300.0),
    "Auriculares": ("Accesorios", 50.0),
    "Monitor": ("Accesorios", 150.0)
}

productos_lista = list(productos_info.keys())

n_filas = 200
datos = []
fecha_inicio = datetime.now() - timedelta(days=30)

for i in range(1, n_filas + 1):
    prod = np.random.choice(productos_lista)
    cat, precio_u = productos_info[prod]
    cant = np.random.randint(1, 6)
    total = cant * precio_u
    fecha = fecha_inicio + timedelta(days=np.random.randint(0, 30), hours=np.random.randint(0, 24))
    
    datos.append({
        "ID_Pedido": f"PED-{i:03d}",
        "Fecha": fecha.strftime("%Y-%m-%d"),
        "Producto": prod,
        "Categoria": cat,
        "Cantidad": cant,
        "Precio_Unitario": precio_u,
        "Total": total
    })

df = pd.DataFrame(datos)
df.to_csv("data/ventas.csv", index=False)
print("✅ ¡Archivo 'data/ventas.csv' generado con éxito con 200 registros!")
```

### ⚡ Instalando Librerías y Ejecutando el Script
Dado que nuestro script utiliza la librería externa `pandas`, primero debemos instalarla en nuestro entorno activo y registrarla en nuestro archivo de requerimientos:

```bash
# Instalar pandas en nuestro entorno virtual activo
pip install pandas

# Registrar la instalación en requirements.txt
pip freeze > requirements.txt

# Ejecutar el script para generar el archivo CSV
python scripts/generar_datos.py
```

*Verifica que en la carpeta `data/` se haya creado correctamente el archivo `ventas.csv`.*

---

## 📊 4. Análisis Exploratorio de Datos (EDA) en un Notebook

Ahora que tenemos los datos simulados, crearemos un cuaderno interactivo para explorarlos de forma rápida.

1.  Crea un cuaderno de Jupyter llamado `notebooks/EDA.ipynb`.
2.  Abre el archivo en VSCode y asegúrate de elegir tu entorno virtual `.venv` en la esquina superior derecha del editor (**Select Kernel**).
3.  Agrega y ejecuta los siguientes bloques de código por celdas:

### Celda 1: Carga de Datos
```python
import pandas as pd

# Cargar el archivo generado (usando la ruta relativa para salir de 'notebooks/' e ir a 'data/')
df = pd.read_csv("../data/ventas.csv")

# Mostrar las primeras 5 filas del conjunto de datos
df.head()
```

### Celda 2: Información General del Dataset
```python
# Inspeccionar tipos de datos y presencia de valores nulos
df.info()
```

### Celda 3: Resumen Estadístico
```python
# Obtener resumen estadístico de las variables numéricas
df.describe()
```

---

## 🎨 5. Creando una Aplicación Interactiva con Streamlit

El paso final es construir una aplicación web interactiva que permita a cualquier usuario explorar nuestros datos visualmente. Usaremos de nuevo la IA para generar el código base.

### 🤖 El Prompt de Streamlit
Crea un archivo llamado `prompts/prompt_streamlit.txt` y guarda en él la siguiente instrucción para la IA:

```text
Actúa como un desarrollador experto en Streamlit y Python. Escribe el código para app.py que cargue el archivo data/ventas.csv. La app debe incluir:
1. Un título y un subtítulo llamativos sobre ventas.
2. Un checkbox que permita al usuario decidir si desea ver las primeras 5 filas del conjunto de datos en una tabla interactiva.
3. Un selector múltiple (st.multiselect) en la barra lateral para filtrar los datos por Categoria.
4. Dos gráficos generados con matplotlib o seaborn colocados uno al lado del otro (st.columns):
   - Un gráfico de barras que muestre el Total de Ventas por Producto.
   - Un histograma o gráfico de barras que muestre la Cantidad total vendida por Producto.
5. El diseño debe lucir profesional, limpio y manejar adecuadamente excepciones si el archivo CSV no existe.
```

### 📄 El Código de la Aplicación: `app.py`
Envía el prompt a la IA y guarda el código resultante en tu archivo `app.py`. A continuación tienes la implementación interactiva lista para usarse:

```python
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 1. Configurar la página de Streamlit
st.set_page_config(page_title="Dashboard de Ventas 📊", layout="wide")

# Estilo de gráficos de seaborn
sns.set_theme(style="whitegrid")

# Título de la Aplicación
st.title("📊 Panel de Control e Insights de Ventas")
st.markdown("Bienvenido al dashboard interactivo. Filtra los datos y explora el rendimiento comercial en tiempo real.")

# 2. Cargar los Datos de forma segura
@st.cache_data
def cargar_datos():
    return pd.read_csv("data/ventas.csv")

try:
    df = cargar_datos()
except FileNotFoundError:
    st.error("❌ Error: No se pudo encontrar el archivo 'data/ventas.csv'. Asegúrate de ejecutar primero el script 'generar_datos.py'.")
    st.stop()

# 3. Barra Lateral (Sidebar) para Filtros
st.sidebar.header("⚙️ Configuración y Filtros")

# Filtro por Categoría
categorias = df["Categoria"].unique()
seleccion_categorias = st.sidebar.multiselect(
    "Selecciona las Categorías a incluir:",
    options=categorias,
    default=categorias
)

# Filtrar el DataFrame según la selección del usuario
df_filtrado = df[df["Categoria"].isin(seleccion_categorias)]

# 4. Métricas Rápidas
col_m1, col_m2, col_m3 = st.columns(3)
with col_m1:
    st.metric(label="Ingresos Totales (USD)", value=f"${df_filtrado['Total'].sum():,.2f}")
with col_m2:
    st.metric(label="Productos Vendidos", value=f"{df_filtrado['Cantidad'].sum()} uds")
with col_m3:
    st.metric(label="Total de Transacciones", value=f"{len(df_filtrado)}")

st.write("---")

# 5. Checkbox para ver datos crudos
if st.checkbox("🔍 Mostrar primeras 5 filas de los datos filtrados"):
    st.subheader("Datos Originales")
    st.dataframe(df_filtrado.head())

st.write("---")

# 6. Visualizaciones de Datos en Columnas
col_grafico1, col_grafico2 = st.columns(2)

with col_grafico1:
    st.write("### 📈 Ventas Totales por Producto (USD)")
    if not df_filtrado.empty:
        ventas_producto = df_filtrado.groupby("Producto")["Total"].sum().reset_index()
        fig, ax = plt.subplots(figsize=(6, 4))
        sns.barplot(x="Total", y="Producto", data=ventas_producto, palette="viridis", ax=ax)
        ax.set_xlabel("Ventas Totales ($)")
        ax.set_ylabel("")
        st.tight_layout()
        st.pyplot(fig)
    else:
        st.warning("⚠️ No hay datos seleccionados para mostrar.")

with col_grafico2:
    st.write("### 🛍️ Cantidad de Unidades Vendidas por Producto")
    if not df_filtrado.empty:
        cantidad_producto = df_filtrado.groupby("Producto")["Cantidad"].sum().reset_index()
        fig, ax = plt.subplots(figsize=(6, 4))
        sns.barplot(x="Cantidad", y="Producto", data=cantidad_producto, palette="magma", ax=ax)
        ax.set_xlabel("Unidades Vendidas")
        ax.set_ylabel("")
        st.tight_layout()
        st.pyplot(fig)
    else:
        st.warning("⚠️ No hay datos seleccionados para mostrar.")
```

### 🚀 Instalación de Requisitos y Lanzamiento
Para correr la aplicación web de Streamlit, necesitamos instalar `streamlit`, `matplotlib` y `seaborn` en nuestro entorno virtual activo y ejecutar la app:

```bash
# Instalar los nuevos paquetes requeridos
pip install streamlit matplotlib seaborn

# Actualizar el archivo requirements.txt con todas las librerías del entorno
pip freeze > requirements.txt

# Iniciar la aplicación de Streamlit
streamlit run app.py
```

Streamlit iniciará un servidor local y abrirá automáticamente una pestaña en tu navegador web (usualmente en la dirección `http://localhost:8501`). ¡Interactúa cambiando los filtros de categoría en la barra lateral y observa cómo cambian las métricas y los gráficos en tiempo real! 🤩

---

## 🎉 ¡Felicidades, has creado un proyecto completo!

En esta sesión has logrado:
1.  **Diseñar la arquitectura física** de tu proyecto.
2.  **Gestionar un entorno virtual aislado** para mantener ordenadas tus librerías.
3.  **Hacer ingeniería de prompts** sencilla para automatizar código repetitivo.
4.  **Desarrollar y probar tus scripts y análisis exploratorios**.
5.  **Crear un Dashboard interactivo** en Streamlit listo para mostrar tus descubrimientos de datos.

