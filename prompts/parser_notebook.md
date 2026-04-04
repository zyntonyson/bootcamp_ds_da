# Instrucciones para Conversión de Markdown a Jupyter Notebook (.ipynb)

Para asegurar que los archivos `.ipynb` generados sean válidos y se abran sin errores (ej. "bad control character"), se deben seguir de forma estricta las siguientes reglas técnicas.

### 1. Estructura Base del JSON

El notebook debe ser un único objeto JSON con las claves principales: `nbformat`, `nbformat_minor`, `metadata`, y `cells`. La clave `cells` es un array de objetos, donde cada objeto es una celda.

### 2. Formato de Celda

Cada objeto de celda debe tener, como mínimo, las siguientes claves:
- `cell_type`: Un string, `"markdown"` o `"code"`.
- `metadata`: Un objeto JSON, generalmente vacío (`{}`).
- `source`: El contenido de la celda, que sigue reglas muy específicas.

### 3. La Regla Crítica para el Campo `source`

Esta es la regla más importante para evitar errores de formato.

- El valor de `source` **siempre** debe ser un **array de strings** en formato JSON.
- Cada string dentro de este array representa **una y solo una línea** del contenido de la celda.
- **Fundamental:** Los strings dentro del array `source` **no deben contener ni terminar con caracteres de nueva línea (`
`) o retorno de carro (``)**. El formato del notebook espera líneas de texto limpias. El software que renderiza el notebook es el responsable de unir cada elemento del array con un salto de línea.

#### Ejemplo Práctico:

**Incorrecto (Causa el error "bad control character"):**
```json
"source": [
  "Esta es la línea 1.
",
  "Esta es la línea 2.
"
]
```
o
```json
"source": "Línea 1
Línea 2"
```

**Correcto:**
```json
"source": [
  "Esta es la línea 1.",
  "Esta es la línea 2."
]
```

### 4. Manejo de Caracteres Especiales (Escapado)

Dentro de los strings del array `source`, los caracteres especiales del formato JSON deben ser escapados.

- **Comillas Dobles (`"`):** Cualquier comilla doble que sea parte del texto debe ser escapada con una barra invertida (`"`).
  - Ejemplo: `dijo "hola"` se convierte en `"dijo "hola""`.
- **Barra Invertida (``):** Cualquier barra invertida literal debe ser escapada, convirtiéndose en ``.
  - Ejemplo: `C:\Users` se convierte en `"C:\Users"`.

### Flujo de Trabajo para la Conversión

1.  **Leer** el archivo `.md` de origen.
2.  **Dividir** el contenido en bloques lógicos que corresponderán a celdas individuales (basado en encabezados, bloques de código, etc.).
3.  **Para cada bloque/celda:**
    a. Dividir su contenido en una lista de líneas.
    b. Procesar **cada línea individualmente** para **eliminar** cualquier carácter de `
` o ``.
    c. Procesar **cada línea ya limpia** para escapar correctamente los caracteres especiales (`"` y ``).
    d. Almacenar estas líneas limpias y escapadas en el array `source` para esa celda.
4.  **Ensamblar** el objeto JSON final del notebook con todas las celdas procesadas.
5.  **Escribir** el objeto JSON en el archivo de destino con extensión `.ipynb`.
