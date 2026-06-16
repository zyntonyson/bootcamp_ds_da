# 🐍 ¡Tu Primer Entorno de Análisis de Datos! Preparación Paso a Paso 💻📊

¡Hola! Te damos la bienvenida a este webinar. En esta sesión aprenderás a preparar tu propia computadora para realizar análisis de datos como un profesional. Configurar el entorno de trabajo puede parecer un reto al principio, pero siguiendo esta guía paso a paso verás que es muy sencillo.

Al finalizar este webinar, lograrás:
*   **Configurar tu propia computadora** para trabajar con datos de manera profesional.
*   **Instalar Python y Visual Studio Code** con sus extensiones esenciales.
*   **Crear entornos virtuales aislados** para mantener ordenados tus proyectos.
*   **Escribir y ejecutar tu primer script de análisis** en un Jupyter Notebook.

¡Comencemos! 🚀


---

## 🖥️ 1. La Terminal de Comandos: Tu Puerta al Desarrollo

### ¿Qué es una terminal?
La **terminal** (también conocida como consola o línea de comandos) es una interfaz de texto que te permite comunicarte directamente con el sistema operativo de tu computadora. 

> 💡 **Analogía sencilla:** Imagina que tu computadora es un restaurante. Usar la interfaz gráfica (hacer clic en carpetas e iconos) es como elegir platos de un menú con fotos. Usar la terminal es como hablar directamente con el chef en la cocina y darle instrucciones exactas de lo que quieres. Es más rápido, directo y potente.

### ¿Por qué es útil tener una terminal?
*   **Automatización:** Puedes realizar tareas repetitivas en segundos.
*   **Instalación rápida:** Te permite descargar y configurar herramientas escribiendo una sola línea de texto.
*   **Control total:** Es la forma en que los desarrolladores y analistas de datos interactúan con servidores y herramientas en la nube.

### ¿Qué terminal vamos a usar?
Dependiendo de tu sistema operativo, te recomendamos las siguientes opciones:
*   **En Windows:** Usaremos **GitBash**. La terminal por defecto de Windows (*CMD*) utiliza comandos diferentes a los de la mayoría de servidores en el mundo (basados en UNIX/Linux). **GitBash** nos da una terminal tipo Linux dentro de Windows.
*   **En macOS y Linux:** Usaremos la **Terminal integrada** del sistema. No necesitas instalar nada adicional.

### ¿Qué es Git y cómo funciona? 📂
**Git** es un **sistema de control de versiones**. Piensa en él como un "historial de cambios inteligente" para tus proyectos. 
*   **¿Cómo funciona?** Git toma "fotografías" (llamadas *commits*) del estado de tus archivos en momentos clave. Si cometes un error en tu código, puedes regresar en el tiempo a una versión anterior sin perder tu trabajo.
*   Además, nos permite conectar nuestra computadora con **GitHub**, la plataforma en la nube donde compartimos código y colaboramos con otros analistas de datos.

### 🧭 Comandos básicos de navegación
Abre tu terminal (**GitBash** en Windows o **Terminal** en macOS/Linux) y practica estos tres comandos esenciales:

1.  **`pwd`** (*Print Working Directory* - Mostrar Directorio de Trabajo): Te dice exactamente en qué carpeta estás ubicado actualmente.
    ```bash
    pwd
    ```
2.  **`ls`** (*List* - Listar): Muestra todos los archivos y carpetas que se encuentran dentro de tu ubicación actual.
    ```bash
    ls
    ```
3.  **`cd`** (*Change Directory* - Cambiar de Directorio): Te permite moverte entre carpetas.
    *   Para entrar a una carpeta llamada *proyectos*:
        ```bash
        cd proyectos
        ```
    *   Para subir un nivel (volver a la carpeta anterior):
        ```bash
        cd ..
        ```

---

## 🐍 2. Instalación de Python

**Python** es el lenguaje de programación más popular para el análisis de datos debido a su sintaxis sencilla y la gran cantidad de librerías especializadas disponibles.

### Cómo escoger la versión de Python
1.  Visita el sitio web oficial: [python.org](https://www.python.org/).
2.  Ve a la sección de descargas (*Downloads*).
3.  **Regla de oro:** Descarga siempre la última versión **estable**. Evita las versiones etiquetadas como *Beta*, *Alpha* o *Release Candidate (RC)*, ya que pueden contener errores. Las versiones más recomendadas y estables actualmente son las de la rama **Python 3.10, 3.11 o 3.12**.
4.  *¡Importante para Windows!* Durante el proceso de instalación, asegúrate de marcar la casilla que dice **"Add python.exe to PATH"** (Agregar Python al PATH). Esto te permitirá ejecutar Python desde cualquier terminal.

### 🔍 Ubicar Python instalado desde GitBash
Una vez completada la instalación, cierra tu terminal y vuelve a abrirla para que se actualicen las configuraciones. Escribe el siguiente comando para verificar que Python está listo para usarse:

```bash
python --version
```
*(Nota: En algunos sistemas macOS o Linux, el comando puede ser `python3 --version`).*

Deberías ver una respuesta similar a esta:
```text
Python 3.11.5
```

---

## 🛠️ 3. Instalar VSCode como Editor de Código

Para escribir nuestras instrucciones de análisis de datos de manera organizada, necesitamos un buen editor.

### ¿Qué es un IDE?
Un **IDE** (*Integrated Development Environment* o Entorno de Desarrollo Integrado) es un editor de texto supercargado diseñado para programar. Incluye herramientas como resaltado de colores para el código, detección de errores en tiempo real y una terminal integrada. El estándar de la industria hoy en día es **Visual Studio Code (VSCode)** por su velocidad y flexibilidad.

### Cargar VSCode desde la terminal 🚀
Puedes abrir VSCode directamente desde la carpeta en la que estás trabajando en la terminal.
1.  Ve a la carpeta de tu proyecto usando `cd`.
2.  Escribe el siguiente comando:
    ```bash
    code .
    ```
    *El punto `.` le indica a VSCode que se abra y cargue todo el contenido de la carpeta actual.*
    
    *(Nota para macOS: Si este comando no funciona la primera vez, abre VSCode manualmente, presiona `Cmd + Shift + P`, escribe "Shell Command" y selecciona "Install 'code' command in PATH").*

### Instalar extensiones en VSCode 🔌
VSCode se vuelve potente gracias a sus extensiones. Abre la sección de extensiones (el icono de cuatro cuadrados en la barra lateral izquierda) e instala:
1.  **Python** (de Microsoft): Te da ayuda con la sintaxis, autocompletado y formato del código.
2.  **Jupyter** (de Microsoft): Te permite trabajar con Notebooks interactivos directamente dentro de VSCode sin necesidad de usar el navegador.

---

## 📦 4. Crear un Entorno Virtual

### ¿Qué es un entorno virtual y por qué usarlo?
Imagina que estás trabajando en dos proyectos diferentes:
*   El *Proyecto A* usa una librería en su versión antigua (ej. versión 1.0).
*   El *Proyecto B* necesita esa misma librería pero en su versión más nueva (ej. versión 3.0).

Si instalas todo de forma global en tu computadora, las versiones entrarán en conflicto. Un **entorno virtual** es una carpeta aislada y dedicada exclusivamente para un proyecto. Todo lo que instales ahí dentro no afectará a otros proyectos ni a tu sistema operativo. ¡Cada proyecto tiene su propia caja de herramientas! 🧰

### Cómo crear un entorno virtual 🛠️
Ubicado en la carpeta de tu proyecto en la terminal, ejecuta el siguiente comando:

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

## 📚 5. Instalar las Librerías Necesarias en Python

Con nuestro entorno virtual activo, es hora de instalar las herramientas científicas para el análisis de datos.

### Uso de pip
**pip** es el gestor de paquetes de Python. Es la herramienta que descarga e instala librerías desde el repositorio oficial de Python (*PyPI*).

### Instalación de librerías de forma individual
Puedes instalar las herramientas clave una a una ejecutando:

```bash
pip install pandas numpy matplotlib seaborn jupyter
```

¿Qué hace cada una de estas librerías?
*   **pandas** 🐼: Es la librería estrella para el análisis de datos. Nos permite estructurar los datos en tablas llamadas *DataFrames* para limpiarlos, filtrarlos y agruparlos.
*   **numpy** 🔢: Permite realizar cálculos matemáticos de alta velocidad sobre grandes volúmenes de datos numéricos.
*   **matplotlib** 📈: Es la librería básica para crear gráficos y visualizaciones estáticas.
*   **seaborn** 🎨: Construida sobre Matplotlib, sirve para crear gráficos estadísticos con diseños modernos y profesionales de forma más sencilla.
*   **jupyter** 📓: Nos da soporte para crear y ejecutar cuadernos de código interactivos.

### Instalación estructurada con *requirements.txt* 📄
Cuando trabajas en equipo, es una buena práctica compartir una lista exacta de las librerías y versiones que utilizas para que otros puedan replicar tu entorno. Esto se hace mediante un archivo llamado *requirements.txt*.

1.  Crea un archivo llamado *requirements.txt* en la raíz de tu proyecto.
2.  Escribe el siguiente contenido:
    ```text
    pandas
    numpy
    matplotlib
    seaborn
    jupyter
    ```
3.  Guarda el archivo.
4.  Instala todas las librerías de una sola vez ejecutando en la terminal:
    ```bash
    pip install -r requirements.txt
    ```

---

## 📓 6. Trabajar con Python en VSCode

¡Es hora de ver la magia en acción! Ejecutaremos nuestro primer bloque de código.

### Crear un Notebook en Python
Un **Jupyter Notebook** (archivo con extensión *.ipynb*) es un documento interactivo que combina celdas de texto (escritas en Markdown) con celdas de código de Python ejecutable de forma independiente. Esto facilita experimentar con los datos e ir documentando los hallazgos al mismo tiempo.

1.  En VSCode, ve al menú *File* > *New File...* (o haz clic derecho en el explorador de archivos) y crea un archivo llamado *analisis.ipynb*.
2.  En la esquina superior derecha del editor de VSCode, haz clic en **"Select Kernel"** (Seleccionar Kernel).
3.  Elige **"Python Environments..."** y selecciona tu entorno virtual **.venv**. Esto asegura que VSCode use las librerías que acabamos de instalar.

### Ejecutar código en Python 🚀
1.  Verás una celda vacía en tu Notebook. Asegúrate de que el tipo de celda sea de código (se muestra un símbolo `[ ]` o un botón `+ Code`).
2.  Escribe el siguiente fragmento de código para simular y visualizar datos:

```python
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Configurar el estilo visual de los gráficos
sns.set_theme(style="whitegrid")

# 1. Crear un conjunto de datos ficticio sobre ventas
datos = {
    "Producto": ["Café Latte", "Espresso", "Capuccino", "Muffin de Chocolate", "Té Verde"],
    "Unidades_Vendidas": [120, 80, 95, 150, 45],
    "Precio_Unitario_USD": [3.50, 2.00, 3.80, 2.50, 2.80]
}

df = pd.DataFrame(datos)

# Calcular el ingreso total por producto
df["Ingreso_Total_USD"] = df["Unidades_Vendidas"] * df["Precio_Unitario_USD"]

# Mostrar la tabla en el Notebook
print("--- Datos de Ventas de la Cafetería ---")
display(df)

# 2. Generar un gráfico de barras
plt.figure(figsize=(8, 5))
sns.barplot(x="Producto", y="Ingreso_Total_USD", data=df, palette="viridis")
plt.title("Ingreso Total por Producto (USD)", fontsize=14, fontweight="bold")
plt.xlabel("Producto", fontsize=12)
plt.ylabel("Ingreso Total (USD)", fontsize=12)
plt.show()
```

3.  Haz clic en el botón de reproducción (icono de flecha o triángulo `▶`) a la izquierda de la celda de código, o presiona `Shift + Enter` en tu teclado.
4.  ¡Listo! Verás la tabla limpia de datos y un hermoso gráfico de barras generado instantáneamente debajo del bloque de código.

---

## 🎉 ¡Felicitaciones!

Has configurado con éxito un entorno local profesional para el análisis de datos. Aprendiste a usar la terminal, a instalar Python, a configurar VSCode, a crear entornos virtuales y a ejecutar tu primer análisis en un Jupyter Notebook.

¡Ahora estás listo para explorar y transformar el mundo de los datos! 🌟📊🐍
