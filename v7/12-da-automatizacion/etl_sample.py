import requests
import sqlite3
import pandas as pd

def extract():
    """EXTRACT: Obtener datos de la API pública"""
    print("Iniciando extracción...")
    url = "https://jsonplaceholder.typicode.com/users"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Error al conectar con la API: {response.status_code}")

def transform(raw_data):
    """TRANSFORM: Limpiar y dar formato a los datos"""
    print("Iniciando transformación...")
    # Creamos un DataFrame para manipular los datos fácilmente
    df = pd.DataFrame(raw_data)
    
    # Seleccionamos solo las columnas que nos interesan
    # Y extraemos el nombre de la compañía (que viene en un dict interno)
    df_clean = df[['id', 'name', 'email', 'phone']].copy()
    df_clean['company_name'] = df['company'].apply(lambda x: x['name'])
    
    # Una transformación simple: nombres en mayúsculas
    df_clean['name'] = df_clean['name'].str.upper()
    
    return df_clean

def load(df):
    """LOAD: Cargar los datos en SQLite"""
    print("Iniciando carga en SQLite...")
    conn = sqlite3.connect('etl_example.db')
    
    # Guardamos el DataFrame en una tabla llamada 'usuarios'
    # if_exists='replace' sobrescribe la tabla si ya existe
    df.to_sql('usuarios', conn, if_exists='replace', index=False)
    
    conn.close()
    print("¡Carga completada con éxito!")

# --- EJECUCIÓN DEL PIPELINE ---
try:
    data = extract()
    transformed_data = transform(data)
    load(transformed_data)
    
    # Verificación rápida
    print("\nPrimeras filas del resultado:")
    print(transformed_data.head(3))
except Exception as e:
    print(f"Error en el pipeline: {e}")