# 🐛 Manejo y lectura de errores en Python 🐍

¡Hola! 👋 En esta sesión vamos a explorar una de las habilidades más importantes en el mundo del análisis de datos: **cómo entender y solucionar errores en nuestro código**. Cometer errores es normal y aprender a manejarlos nos hará programadores más eficientes y resilientes. ¡Vamos a perderle el miedo a los errores! 💪

## 🎯 Objetivos de la sesión

Al finalizar este webinar, serás capaz de:

1.  **Leer e interpretar** un `traceback` para identificar la causa de un error.
2.  **Reproducir un error** de manera controlada para poder diagnosticarlo.
3.  **Corregir errores comunes** en Python y pandas.
4.  **Prevenir errores** utilizando `try-except` para que tus scripts sean más robustos.

## 💥 Errores al ejecutar código

> "Errar es humano, pero echarle la culpa a la computadora es más humano todavía." - Robert Orben

Escribir código es un proceso creativo y, como en todo proceso creativo, los errores son parte del camino. Un analista de datos no solo sabe crear modelos o visualizaciones, sino que también es un **detective de errores**.

Aquí algunos tipos de errores que encontraremos:

-   **Errores de código 📝**: Una variable mal escrita, una función con los parámetros incorrectos, o intentar acceder a un índice que no existe. ¡A todos nos pasa!
-   **Errores por datos 📊**: Columnas con espacios extra, números que en realidad son texto, fechas en formatos extraños o los famosos valores faltantes (`NaN`).
-   **Errores por entorno 💻**: La clásica ruta de archivo que no funciona en otra computadora, o librerías que olvidamos instalar.

## 🔍 Anatomía de un error (Tracebacks)

Cuando Python encuentra un error, nos grita... ¡pero de una forma muy estructurada! A esto se le llama **Traceback**. Es un mapa que nos guía desde el punto donde se ejecutó el script hasta la línea exacta que causó el problema.

La clave es leerlo de **abajo hacia arriba**:

1.  **La última línea** te dice el **tipo de error** y un mensaje descriptivo.
2.  **Las líneas de en medio** te muestran el **camino** que siguió el código hasta llegar al error, como migas de pan.
3.  **La línea de código** que falló se muestra claramente para que sepas dónde mirar.

### 🕵️‍♀️ Lectura de errores de código

¡Vamos a practicar! Aquí tienes varios errores. Tu misión es leer el traceback y entender por qué ocurre.

#### Traceback A: `IndentationError`

Este es el "error del espacio fantasma". Ocurre cuando Python no entiende la estructura de nuestro código por un problema de indentación.

```python
def mi_funcion():
print("¡Hola, mundo!") # Esta línea debería estar indentada
```

#### Traceback B: `TypeError`

Aparece cuando intentamos hacer una operación con tipos de datos que no son compatibles. ¿Sumar un número y un texto? ¡Python no sabe cómo hacerlo!

```python
resultado = "El total es: " + 100
```

#### Traceback C: `ZeroDivisionError`

Las matemáticas tienen reglas, y una de ellas es: ¡nunca dividirás por cero!

```python
promedio = 100 / 0
```

#### Traceback D: `IndexError`

Intentas acceder a un elemento de una lista usando un índice que está fuera de los límites.

```python
mi_lista = [10, 20, 30]
print(mi_lista[3]) # El último índice es 2
```

#### Traceback E: `KeyError`

Similar al anterior, pero con diccionarios. Ocurre cuando intentas acceder a una llave que no existe.

```python
mi_diccionario = {"nombre": "Ana", "edad": 25}
print(mi_diccionario["profesion"]) # La llave "profesion" no existe
```

### 🐼 Manejo de errores al trabajar con datos

Ahora, veamos cómo se ven estos errores en el campo de batalla de un analista: ¡los DataFrames de pandas!

#### `TypeError` en operaciones con pandas

Imagina que cargas datos y una columna que debería ser numérica es de tipo `object` (texto).

```python
import pandas as pd
import numpy as np

df = pd.DataFrame({'ventas': ['100', '200', 'no disponible', '300']})

# Esto dará un TypeError porque no podemos sumar texto
# df['ventas'] * 1.10 
```

**Solución:** ¡Limpiar y convertir! Debemos asegurarnos de que la columna sea numérica.

```python
# Convertimos a numérico, y los errores los ponemos como NaN
df['ventas_limpias'] = pd.to_numeric(df['ventas'], errors='coerce') 

# Rellenamos los NaN con 0 o la media/mediana si es apropiado
df['ventas_limpias'] = df['ventas_limpias'].fillna(0)

# ¡Ahora sí podemos hacer operaciones!
df['ventas_con_iva'] = df['ventas_limpias'] * 1.16
print(df)
```

#### `KeyError` y nombres de columnas

Un clásico: escribir mal el nombre de una columna o que tenga espacios ocultos.

```python
data = {'Nombre Completo': ['Ana', 'Luis'], 'Edad': [30, 25]}
df = pd.DataFrame(data)

# Esto dará KeyError porque 'nombre completo' no es 'Nombre Completo'
# print(df['nombre completo'])
```

**Solución:** Estandarizar los nombres de las columnas.

```python
# Hacemos todo a minúsculas y reemplazamos espacios por guiones bajos
df.columns = df.columns.str.lower().str.replace(' ', '_')

# ¡Ahora es más fácil y seguro!
print(df['nombre_completo'])
```

#### `ValueError` al convertir datos (fechas, números)

Cuando intentas convertir un dato a un formato que no corresponde.

```python
fechas = ['2023-01-01', '02/02/2023', 'Fecha inválida']
# pd.to_datetime(fechas) # Esto daría un ValueError
```

**Solución:** Usar `errors='coerce'` para que los valores no válidos se conviertan en `NaT` (Not a Time).

```python
fechas_limpias = pd.to_datetime(fechas, errors='coerce')
print(fechas_limpias)
```

#### `IndexError` + `ZeroDivisionError`

Una combinación peligrosa. Imagina que quieres calcular una métrica, pero no tienes datos.

```python
datos_ventas = []
primera_venta = datos_ventas[0] # IndexError
# total_ventas = sum(datos_ventas)
# promedio = total_ventas / len(datos_ventas) # ZeroDivisionError
```

**Solución:** ¡Siempre verificar si tienes datos antes de operar!

```python
if datos_ventas: # Una lista vacía se evalúa como False
    print("Hay datos, podemos proceder.")
else:
    print("La lista está vacía, no se puede calcular nada.")
```

### 🛡️ Prevención de errores con `try-except`

A veces, no podemos controlar todo. Un archivo puede no existir o una API puede fallar. Para esos casos, usamos `try-except`.

> La estructura es: **Intenta** hacer esto (`try`), y si sale un **error específico**, en lugar de detener todo, **haz esto otro** (`except`).

```python
try:
    # Código que podría fallar
    resultado = 10 / 0
except ZeroDivisionError:
    # Código que se ejecuta SI Y SOLO SI ocurre el error esperado
    print("¡Oye, no se puede dividir por cero! Asignando 0 al resultado.")
    resultado = 0

print(f"El resultado es: {resultado}")
```

**Ejemplo práctico:** Leer un CSV que podría no existir.

```python
ruta_correcta = 'incomes.csv'
ruta_incorrecta = 'incomess.csv' # oops, un typo

try:
    df = pd.read_csv(ruta_incorrecta)
    print("Archivo leído con éxito!")
except FileNotFoundError:
    print(f"😥 No se encontró el archivo en la ruta: {ruta_incorrecta}")
    print("Asegúrate de que el archivo esté en la carpeta correcta.")
    df = pd.DataFrame() # Creamos un DF vacío para no romper el resto del script

# assert nos sirve para verificar condiciones. Si no se cumple, lanza un error.
# Es una forma de autodebugging.
assert not df.empty, "El DataFrame está vacío, algo salió mal al leer el archivo."

print("El programa continúa...")

```

### 🏆 Actividad final: Debuggeo de script

¡Tu turno de ser el detective! Te daré un script con varios problemas. Tu misión es usar todo lo que aprendimos para hacerlo funcionar.

**Paso 1: Generar los datos**

Primero, ejecuta este código para crear el archivo `incomes_2_gb.csv`.

```python
import pandas as pd
import numpy as np

# Generar datos de ejemplo
data = {
    'region': np.random.choice(['Norte', 'Sur', 'Este', 'Oeste'], 50),
    'channel': np.random.choice(['Online', 'Tienda', 'Teléfono'], 50),
    'income': np.random.uniform(1000, 5000, 50).round(2)
}
df_incomes = pd.DataFrame(data)

# Guardar como CSV
df_incomes.to_csv('incomes_2_gb.csv', index=False)

print("¡Archivo incomes_2_gb.csv creado con éxito!")
```

**Paso 2: El script con errores**

Aquí está el script que debes depurar. ¡Tiene 3 errores ocultos!

```python
# ---- Script a depurar ----

import pandas as pd

# Error 1: La ruta del archivo está mal escrita
df = pd.read_csv('incomes_2_gb.csvv') 

# Error 2: La columna 'income' se tratará como texto y dará error al sumar
# (Imaginemos que al guardarse/cargarse se convierte a string)
df['income'] = df['income'].astype(str)

print("Resumen de ventas:")

# Error 3: La columna 'country' no existe
resumen_por_pais = df.groupby('country')['income'].sum()

print(resumen_por_pais)

total_ventas = df['income'].sum()
print(f"Ventas totales: ${total_ventas:,.2f}")
```

**Instrucciones:**

Crea una rutina que solucione o prevenga los siguientes errores usando `try-except` o `assert`:

1.  `FileNotFoundError`: Por la ruta incorrecta.
2.  `TypeError`: Al intentar sumar la columna `income` que está como texto.
3.  `KeyError`: Al intentar agrupar por la columna `country` que no existe.

¡Manos a la obra! 🕵️‍♂️

---

### ✅ Solución propuesta

Aquí tienes una forma de abordar el problema:

```python
import pandas as pd

def analizar_ingresos(ruta_archivo):
    # 1. Prevenir FileNotFoundError
    try:
        df = pd.read_csv(ruta_archivo)
        print("✅ Archivo encontrado y leído.")
    except FileNotFoundError:
        print(f"❌ Error: No se encontró el archivo en '{ruta_archivo}'.")
        return

    # 2. Prevenir TypeError asegurando que 'income' es numérico
    if 'income' in df.columns:
        # Usamos errors='coerce' para manejar valores que no sean números
        df['income'] = pd.to_numeric(df['income'], errors='coerce')
        # Eliminamos filas donde la conversión falló, si las hubiera
        df.dropna(subset=['income'], inplace=True)
        print("✅ Columna 'income' convertida a tipo numérico.")
    else:
        print("❌ Error: La columna 'income' no se encuentra en el archivo.")
        return

    # 3. Prevenir KeyError al verificar si la columna de agrupación existe
    columna_agrupacion = 'region' # Usamos 'region' que sí existe
    
    if columna_agrupacion in df.columns:
        print(f"
Resumen por '{columna_agrupacion}':")
        resumen = df.groupby(columna_agrupacion)['income'].sum()
        print(resumen)
    else:
        print(f"⚠️ Advertencia: La columna '{columna_agrupacion}' no existe. No se puede generar el resumen.")

    # Calcular el total
    total_ventas = df['income'].sum()
    print(f"
🎉 Ventas totales: ${total_ventas:,.2f}")


# --- Ejecutamos la función con la ruta correcta ---
analizar_ingresos('incomes_2_gb.csv')

print("-" * 30)

# --- Probamos con una ruta incorrecta para ver el control de errores ---
print("Probando con una ruta incorrecta:")
analizar_ingresos('ruta_que_no_existe.csv')

```

¡Felicidades! Has aprendido a enfrentarte a los errores como un profesional. Recuerda: un error es solo una oportunidad para aprender algo nuevo sobre tu código y tus datos. 🚀
