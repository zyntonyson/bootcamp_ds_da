# Webinar 3 : Comó compartir tu proyecto en el repositorio de GitHub y ponlo en linea en render

En esta sesión el estudiante va a aprender a compartir su proyecto en el repositorio de GitHub y ponerlo en linea en render. 

Contenido tematico:

Desarrollar brevemente sobre los que git y gitHub son y por qué son importantes en el mundo del desarrollo de software.

Parte practica:

## Preparar el repositorio y establecer el ambiente de trabajo

- Decir al estudiante que cree una cuenta en github.com
- Cree un repositorio publico
- Clone el repositorio en su local con la herramienta de la paleta de comandos de VSCode

## Generar un aplicación pequeña basada en streamlit con apoyo de IA

Ahora dentro la carpeta clonada

Generación de datos: En esta parte pon un prompt donde se le pide a la IA que genere un conjuntos sintéticos en formato csv , el prompt debe poder personalizar la temática del conjunto de datos. Pero debe ser lo suficientemente especifico sobre su estructura


- decir al estudiante que cree la carpeta data y guarde alli el conjunto de datos en formato csv

Generación de la aplicación: En esta parte pon un prompt donde se le pide a la IA que genere un aplicación pequeña basada en el conjunto de datos creado. La aplicación debe tener un titulo , subtitlo algun boton de interactividad y debe mostrar al menos dos gráficos. Debe usar las librerias de plotly para los graficos y para aplicación debe usar streamlit.  Pon como una nota adicional que incluya que aplcaciones deben estar en el requirement.txt para aplicación pero sin incluir las versiones de las librerias

- decir al estudiante que salve el codigo en el archivo app.py y que ajuste el codigo para que lea el archivo csv en la u
- decir que cree el archivo requirement.txt con el contenido sugerido

- pedir que instale las librerias si fuera necesario y que pruebe la aplicación creada ( da el codigo para correr el app)

## Carga de cambios en gitHub

- Decir que haga el git add . y el git commit -m "Applicación de streamlit"  ( dando una explicación sencilla de lo que haran los comandos)
- ahora que haga el git push ( dando una explicación sencilla de lo que haran los comandos)

- Diseño del README.md: 
- pedir al estudiante que actualice el README.md apoyado por IA, da un ejemplo del prompt que puede usar para generar un buen README.md


## Despliegue del app en Render

- da los pasos necesarios para desplegar la aplicación en render

