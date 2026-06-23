# Webinar 2 : Trabajando con Python y el entorno de desarrollo

En esta sesión, la idea es que el estudiante puede crear un proyecto pequeño de Python en su computadora. Pueda crear una estructura de proyecto, un entorno virtual y pueda ejecutar un script de Python.

Estructura del proyecto: carpeta de scripts, carpeta de datos, carpeta de notebook,carpeta de prompt, requirements, script principal que incluye una implementación simple en streamlit. 

## Estructura de la sesión:


1. Incluye el titulo de la sesión, los objetivos de la sesión en forma de lista

2. Desarrolla la siguiientes intrucciones del proyecto, incluye los bloque de ejemplo para los prompts  

Instrucciones del proyecto
    - Describe la estructura del proyecto en formato ascii y pide a los estudiantes que creen las carpetas correspondientes y explica que contendrá cada carpeta

        - En la carpeta prompts, colocaremos algunos prompts que nos ayudaran a generar código para nuestro proyecto.
        - En la carpeta scripts, colocaremos algunos scripts de Python que nos ayudaran.
        - En la carpeta notebooks, colocaremos algunos notebooks de Python .
    
    - En la carpeta `prompts`, salva un prompt para pedir a la IA que genere un script de python que genere un archivo csv en la carpeta de datos. 
    - Salva el script en la carpeta scripts y ejecutalo para generar el archivo csv.
    - instala los paquetes faltantes que sean necesarios y ve agregandolos al archivo requirements
    - Crear un notebook en la carpeta notebooks llamada EDA.ipynb, donde cargaras el archivo csv y realizaras un analisis exploratorio de datos.
    - En la carpeta prompts pide un script donde se pida una implementación sencilla en streamlit donde:
        - que cargue el archivo csv
        - Título y subtítulo
        - muestra las primeras 5 filas del archivo csv
        - muestre un grafico de barras de las columnas categoricas
        - muestre un histograma de las columnas numericas
        - incluya algun filtro, ya sea un boton o lista despegable. Por ejemplo, si el archivo csv tiene una columna de tipo fecha, se puede incluir un filtro para mostrar los datos de un rango de fechas. Si el archivo csv tiene una columna de tipo categoria, se puede incluir un filtro para mostrar los datos de una categoria en especifico.
    - Salva el script generado en la carpeta principal con el nombre app.py



            




# Webinar 3 : Comó compartir tu proyecto en el repositorio de GitHub y ponlo en linea en render
