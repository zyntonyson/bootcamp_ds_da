# Diseño de un Pipeline ETL en Python 🐍🔧

¡Hola, equipo! 👋 En esta sesión vamos a construir nuestro primer **pipeline de ETL (Extract, Transform, Load)** en Python. Es una de las tareas más comunes y fundamentales en el mundo de los datos.

> 🧠 **Analogía:** Piensa en un ETL como el proceso de **cocinar**. Primero, **extraes** los ingredientes (datos) del supermercado (API, base de datos, etc.). Luego, los **transformas**: los lavas, cortas y preparas. Finalmente, los **cargas** en un plato para servirlos (una base de datos, un dashboard).

## Objetivos del Webinar 🎯

1.  **Explicar qué es ETL** (y cuándo usarlo).
2.  **Extraer (E)** datos desde el API de OpenAQ.
3.  **Transformar (T)** aplicando limpieza, cambios de tipo y validaciones.
4.  **Crear tablas de resumen** (nuestra capa de "oro" o `gold_data`).
5.  **Cargar (L)** los datos en una base de datos SQLite.
6.  **Ensamblar un pipeline** simple y reutilizable con funciones.

---

## 🏛️ ¿Qué es ETL y por qué es tan importante?

**ETL** significa **Extract, Transform, Load** (Extraer, Transformar, Cargar). Es el proceso que usamos para mover datos desde una o varias fuentes, limpiarlos, darles una estructura útil y almacenarlos en un destino final, como una base de datos o un Data Warehouse.

-   **Extract (Extraer):** Obtener los datos desde su origen.
-   **Transform (Transformar):** Limpiar, validar, enriquecer y modelar los datos. ¡Aquí es donde ocurre la magia! ✨
-   **Load (Cargar):** Guardar los datos transformados en su destino final.

Usamos ETL para consolidar datos, prepararlos para análisis, alimentar dashboards o para cualquier tarea que requiera datos limpios y estructurados.

---

## 1. Extract: Extrayendo datos del API de OpenAQ 🌍

Vamos a usar el API de [OpenAQ](https://openaq.org/) para obtener datos de calidad del aire. Ya vimos cómo conectarnos en sesiones anteriores, ¡así que vamos a aplicar lo aprendido!

Nuestro objetivo será extraer las mediciones de `pm25` para un país específico en un rango de fechas.

```python
import requests
import pandas as pd

def extract_measurements(country_code='MX', date_from='2024-01-01', date_to='2024-01-02'):
    """
    Extrae mediciones de calidad del aire (pm25) desde el API de OpenAQ para un país y rango de fechas.
    """
    print(f"🌍 Extrayendo datos para el país: {country_code}")
    
    api_url = "https://api.openaq.org/v2/measurements"
    params = {
        'country': country_code,
        'parameter': 'pm25',
        'date_from': date_from,
        'date_to': date_to,
        'limit': 10000  # Aumentamos el límite para obtener más datos
    }
    
    try:
        response = requests.get(api_url, params=params)
        response.raise_for_status()  # Lanza un error si la petición falla
        data = response.json()['results']
        
        print(f"✅ ¡Extracción exitosa! Se encontraron {len(data)} mediciones.")
        return data
    except requests.exceptions.RequestException as e:
        print(f"🔥 Error en la extracción: {e}")
        return None

# Probemos nuestra función de extracción
raw_data = extract_measurements()
# Convertimos a DataFrame para una vista rápida
if raw_data:
    df_raw = pd.DataFrame(raw_data)
    print(df_raw.head())
```

---

## 2. Transform: Limpieza y modelado de datos 🧹

Los datos crudos rara vez son perfectos. La etapa de transformación es crucial para asegurar la calidad.

Nuestras tareas serán:
- Convertir la lista de diccionarios a un DataFrame de pandas.
- Seleccionar solo las columnas que nos interesan.
- Convertir la fecha a un formato `datetime`.
- Desanidar la información de las coordenadas.
- Renombrar columnas para que sean más claras.
- Validar que los valores de `pm25` no sean negativos.

```python
def transform_data(data):
    """
    Transforma los datos crudos de OpenAQ en un DataFrame limpio y estructurado.
    """
    if not data:
        print(" transformação ignorada: datos de entrada vacíos.")
        return pd.DataFrame()

    print("🧹 Transformando y limpiando datos...")
    
    df = pd.json_normalize(data, sep='_')
    
    # 1. Seleccionar y renombrar columnas de interés
    columns_of_interest = {
        'location': 'location',
        'city': 'city',
        'date_utc': 'datetime_utc',
        'value': 'value',
        'unit': 'unit',
        'coordinates_latitude': 'latitude',
        'coordinates_longitude': 'longitude'
    }
    
    # Asegurarnos de que todas las columnas existan, si no, se llenan con None
    for col in columns_of_interest.keys():
        if col not in df.columns:
            df[col] = None

    df_transformed = df[list(columns_of_interest.keys())].rename(columns=columns_of_interest)
    
    # 2. Conversión de tipos
    df_transformed['datetime_utc'] = pd.to_datetime(df_transformed['datetime_utc'])
    df_transformed['value'] = pd.to_numeric(df_transformed['value'])
    
    # 3. Validación de datos: eliminar valores negativos que no tienen sentido físico
    initial_rows = len(df_transformed)
    df_transformed = df_transformed[df_transformed['value'] >= 0]
    removed_rows = initial_rows - len(df_transformed)
    
    print(f"📊 Transformación completa. Se eliminaron {removed_rows} registros con valores inválidos.")
    
    return df_transformed

# Usemos la función con los datos extraídos
df_silver = transform_data(raw_data)
if not df_silver.empty:
    print(df_silver.info())
    print(df_silver.head())
```
> En la industria, a esta capa de datos limpios y estructurados a menudo se le llama **"Silver Layer"** (Capa de Plata).

---

## 3. Creando la capa "Gold": Tablas de resumen 🏆

La capa "Gold" (Oro) contiene datos agregados y listos para el negocio. Son las tablas que un analista o un modelo de Machine Learning consumiría directamente.

Vamos a crear una tabla que resuma el promedio diario de `pm25` por ciudad.

```python
def create_gold_data(df):
    """
    Crea una tabla de resumen (capa Gold) con el promedio diario de pm25 por ciudad.
    """
    if df.empty:
        return pd.DataFrame()

    print("🏆 Creando la tabla de resumen (Gold)...")
    
    df['date'] = df['datetime_utc'].dt.date
    
    df_gold = df.groupby(['city', 'date']).agg(
        avg_pm25=('value', 'mean'),
        max_pm25=('value', 'max'),
        min_pm25=('value', 'min'),
        num_measurements=('value', 'count')
    ).reset_index()
    
    df_gold['avg_pm25'] = df_gold['avg_pm25'].round(2)
    
    print("✨ ¡Tabla Gold creada exitosamente!")
    return df_gold

# Creemos nuestra tabla de oro
df_gold = create_gold_data(df_silver.copy()) # Usamos .copy() para evitar warnings
if not df_gold.empty:
    print(df_gold.head())
```

---

## 4. Load: Cargando los datos a una Base de Datos SQLite 💾

¡Es hora de guardar nuestro trabajo! Usaremos **SQLite**, una base de datos súper ligera que guarda todo en un solo archivo. Es perfecta para proyectos como este.

Pandas hace que este proceso sea increíblemente fácil con el método `.to_sql()`.

```python
import sqlite3

def load_to_sqlite(tables, db_name='openaq.db'):
    """
    Carga un diccionario de DataFrames a tablas en una base de datos SQLite.
    - tables: {'nombre_tabla': DataFrame}
    """
    print(f"💾 Cargando datos a la base de datos '{db_name}'...")
    
    try:
        conn = sqlite3.connect(db_name)
        
        for table_name, df in tables.items():
            if not df.empty:
                df.to_sql(table_name, conn, if_exists='replace', index=False)
                print(f"  - Tabla '{table_name}' cargada con {len(df)} filas.")
        
        conn.close()
        print("✅ Carga finalizada.")
        
    except sqlite3.Error as e:
        print(f"🔥 Error al cargar a SQLite: {e}")

# Preparamos el diccionario de tablas y ejecutamos la carga
tables_to_load = {
    'raw_measurements': df_raw, # Guardamos también la data cruda por si acaso
    'silver_measurements': df_silver,
    'gold_daily_summary': df_gold
}

load_to_sqlite(tables_to_load)
```

### Verificación

¿Cómo sabemos que funcionó? ¡Leamos los datos de vuelta desde la base de datos!

```python
def verify_load(db_name='openaq.db'):
    conn = sqlite3.connect(db_name)
    
    try:
        print("
🔍 Verificando datos en la base de datos:")
        # Leemos los nombres de las tablas
        tables = pd.read_sql("SELECT name FROM sqlite_master WHERE type='table';", conn)
        print("Tablas encontradas:", tables['name'].tolist())

        # Leemos algunas filas de la tabla gold
        df_check = pd.read_sql("SELECT * FROM gold_daily_summary LIMIT 5", conn)
        print("
Primeras 5 filas de 'gold_daily_summary':")
        print(df_check)
        
    finally:
        conn.close()

verify_load()
```

---

## 5. ¡Juntando todo en un Pipeline! 🚀

Hemos creado funciones para cada paso. Ahora, podemos unirlas en un solo script que ejecute todo el proceso de forma ordenada.

```python
def run_openaq_etl_pipeline(country_code='MX', date_from='2024-01-01', date_to='2024-01-02'):
    """
    Ejecuta el pipeline ETL completo para OpenAQ.
    """
    print("=============================================")
    print(f"🚀 INICIANDO PIPELINE ETL PARA {country_code} 🚀")
    print("=============================================")
    
    # 1. Extract
    raw_data = extract_measurements(country_code, date_from, date_to)
    
    # 2. Transform
    df_silver = transform_data(raw_data)
    
    # 3. Create Gold Data
    df_gold = create_gold_data(df_silver.copy())
    
    # 4. Load
    if raw_data:
        df_raw = pd.DataFrame(raw_data) # Necesitamos el DF crudo para cargarlo
        tables_to_load = {
            'raw_measurements': df_raw,
            'silver_measurements': df_silver,
            'gold_daily_summary': df_gold
        }
        load_to_sqlite(tables_to_load)
        
        # 5. Verify
        verify_load()
    
    print("
🎉 ¡Pipeline finalizado exitosamente! 🎉")

# ¡Ejecutemos todo el flujo con una sola llamada!
run_openaq_etl_pipeline(country_code='CL', date_from='2024-03-01', date_to='2024-03-02')
```

¡Y ahí lo tienes! Un pipeline de ETL funcional. Este es el pilar para construir sistemas de datos robustos y automatizados.

## Conclusión y Próximos Pasos 🏁

Hoy aprendimos a:
- Estructurar un proceso ETL con funciones claras.
- Manejar datos desde una API hasta una base de datos.
- Diferenciar entre capas de datos (Raw, Silver, Gold).
- Usar SQLite para almacenar nuestros resultados de forma sencilla.

**Para seguir aprendiendo:**
- **Mejora el pipeline:** Añade manejo de errores más robusto, logs para cada paso o un sistema de configuración.
- **Automatízalo:** Investiga cómo programar la ejecución de este script una vez al día (¡hola, `cron` o Airflow!).
- **Expande las transformaciones:** ¿Qué otras métricas podrías calcular en la capa Gold?

¡Excelente trabajo, equipo! 💪✨
