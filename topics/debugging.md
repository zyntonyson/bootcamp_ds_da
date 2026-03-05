# Manejo y lectura de errores en python

## Objetivos
 Aqui propon 4 objetivos del tipo poder leer errores, reproducir un error, corregir errores y usar try/catch para prevenir errores.

## Errores al ejecutar código

En esta sección comenta que es normal cometer errores al escribir código y que una habilidad necesaria para un analista de datos es poder identificarlos, entenderlo y corregirlos. Comenta un poco sobre tipos de errores


Errores de código: variables mal escritas, funciones usadas mal, índices fuera de rango.
Errores por datos: columnas con espacios, números en texto, fechas inválidas, valores faltantes.
Errores por entorno: rutas de archivos, librerías no instaladas.

## Anatomia de un error (Tracebacks)

En este punto comenta la estructura de los traceback en python y sobre cómo leerlo

### Lectura de errores de código
> en cada punto genera un codigo que manda un error especifico, la idea es que los estudiantes puedan leer el traceback y entender la razon del error. Los bloques de codigo deben devolver los siguientes errores

Traceback A IndentationError

Traceback B TypeError

Traceback  C ZeroDivisionError


Traceback  D IndexError


Traceback  E KeyError

### Manejo de errores al trabajar con datos 

En este punto vamos a generar algunos errores al trabajar con dataframes. Para cada error propon un codigo donde se muestre el error y posteriormente una propuesta para solucionarlo. En este punto aun no usamos try/catch, solo operaciones basicas de python y pandas

- TypeError en operaciones con pandas

- KeyError y nombres de columnas

-  ValueError al convertir datos (fechas,numeros)

- IndexError + ZeroDivisionError 


### Prevención de errores con try/catch

Aqui deja una explicación sobre la estructura base del uso de try/catch, incluye  un bloque de codigo de ejemplo, asi como recomendaciones al usarlo. Vamos a incluir un ejemplo practico donde Provocaremos FileNotFoundError al leer un CSV con ruta incorrecta.
Lo manejaremos con try/except. Agregaremos una validación con assert.


### Actividad final. Debuggeo de script

La idea es proporcionar un script que lea un archivo csv y que haga un resumen donde muestre ventas totales. 

- primero genera un codigo donde se genere  un dataframe con las tres columnas llamadas region,channel,income. Genera 50 registros y salvalo en formato csv con el nombre incomes_2_gb.csv 

- Ahora haz el script donde se lee el archivo csv, pero que se escriba mal la ruta para genere el primer error
- Cuando se lea que la columna income se cargue como texto para que al hacer operaciones se genere el segundo error
- Que se llame a la columna country para hacer un resumen por pais (la columna no existe en el set de datos)


En las instrucciones decirle al estudiante que cree una rutina que solucione o prevenga los errores de filenotfound, typerror, keyerror y valueerror usando ya sea try/catch o assert.

al final incluye la solucion propuesta