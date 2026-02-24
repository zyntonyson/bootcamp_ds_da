# Diccionarios 📚

Un **diccionario** en Python es una colección de elementos que, a diferencia de las listas, no están ordenados por un índice numérico, sino por una **llave** (key). ¡Imagina un diccionario real! 📖 Buscas una palabra (la llave) para encontrar su definición (el valor).

Cada elemento en un diccionario es un par `llave: valor`.

- Las **llaves** deben ser únicas e inmutables (como strings, números o tuplas).
- Los **valores** pueden ser de cualquier tipo de dato (números, strings, listas, ¡incluso otros diccionarios!).

## Métodos y Operaciones Comunes 🛠️

Veamos cómo trabajar con ellos.

### `.keys()`

Este método te devuelve un objeto especial que contiene todas las llaves del diccionario. Es súper útil para saber qué "palabras" tienes en tu diccionario.

**Ejemplo 1: Frutas y sus colores** 🍎🍌

```python
colores_frutas = {
    'manzana': 'rojo',
    'banana': 'amarillo',
    'uva': 'morado'
}
print(colores_frutas.keys())
# Salida: dict_keys(['manzana', 'banana', 'uva'])
```

**Ejemplo 2: Stock de una tienda** 🏪

```python
stock_tienda = {
    'camisetas': 120,
    'pantalones': 80,
    'zapatos': 50
}
print(stock_tienda.keys())
# Salida: dict_keys(['camisetas', 'pantalones', 'zapatos'])
```

### `.values()`

De manera similar a `.keys()`, este método te regresa todos los valores del diccionario. Es perfecto para obtener un listado de todas las "definiciones".

**Ejemplo 1: Calificaciones de estudiantes** 🎓

```python
calificaciones = {
    'Ana': 95,
    'Luis': 88,
    'Elena': 100
}
print(calificaciones.values())
# Salida: dict_values([95, 88, 100])
```

**Ejemplo 2: Capitales de países** 🌍

```python
capitales = {
    'España': 'Madrid',
    'Argentina': 'Buenos Aires',
    'Japón': 'Tokio'
}
print(capitales.values())
# Salida: dict_values(['Madrid', 'Buenos Aires', 'Tokio'])
```

### `.items()`

Este método es genial porque te devuelve una lista de tuplas, donde cada tupla es un par `(llave, valor)`. Te permite recorrer el diccionario completo, llave y valor al mismo tiempo.

**Ejemplo 1: Información de un usuario** 👤

```python
usuario = {
    'nombre': 'Carlos',
    'edad': 34,
    'ciudad': 'México'
}
print(usuario.items())
# Salida: dict_items([('nombre', 'Carlos'), ('edad', 34), ('ciudad', 'México')])
```

**Ejemplo 2: Precios de un menú** 🍔🍟

```python
precios_menu = {
    'hamburguesa': 8.50,
    'refresco': 1.50,
    'papas': 2.00
}
for producto, precio in precios_menu.items():
    print(f'El precio de la {producto} es ${precio}')
```

### Consultar el valor de una llave 🔍

Para acceder al valor asociado a una llave, usas los corchetes `[]`. Es la operación más común que harás.

**Ejemplo 1: Teléfonos de contactos** 📱

```python
contactos = {
    'Juan': '555-1234',
    'Maria': '555-5678'
}
telefono_de_juan = contactos['Juan']
print(telefono_de_juan)
# Salida: 555-1234
```

> **¡Cuidado!** Si intentas acceder a una llave que no existe, Python te dará un `KeyError`. Una forma segura es usar el método `.get()`, que devuelve `None` (o un valor por defecto que tú elijas) si la llave no se encuentra.

**Ejemplo 2: Usando `.get()` para evitar errores** 🤔

```python
planetas_diametro = {
    'Tierra': 12742,
    'Marte': 6779
}
diametro_jupiter = planetas_diametro.get('Júpiter', 'No encontrado')
print(f"El diámetro de Júpiter es: {diametro_jupiter}")
# Salida: El diámetro de Júpiter es: No encontrado
```

### Eliminar elementos

#### Usando `.pop()`

El método `.pop()` elimina un elemento a partir de su **llave** y, muy importante, **devuelve el valor** del elemento eliminado. Esto es útil si necesitas usar ese valor justo después de quitarlo.

**Ejemplo 1: Atender al próximo cliente** 🙋‍♀️

Imagina que tienes una fila de turnos y quieres atender al siguiente.
```python
turnos = {"cliente_1": "Ana", "cliente_2": "Luis", "cliente_3": "Maria"}
proximo_cliente = turnos.pop("cliente_1")
print(f"Atendiendo a: {proximo_cliente}")
print(f"Turnos restantes: {turnos}")
```

**Ejemplo 2: Vender un artículo y actualizar el stock** 🛒

Quieres registrar una venta y al mismo tiempo sacar el artículo del inventario.
```python
inventario = {"laptops": 10, "ratones": 50, "teclados": 30}
articulo_vendido = inventario.pop("laptops")
print(f"Se vendió una laptop. Quedaban {articulo_vendido} unidades.")
print(f"Inventario actualizado: {inventario}")
```

#### Usando `del`

La palabra clave `del` también elimina un elemento por su **llave**, pero a diferencia de `.pop()`, **no devuelve ningún valor**. Es una operación directa y definitiva.

**Ejemplo 1: Eliminar un usuario inactivo** 🚫

Si un usuario ha cerrado su cuenta, podemos eliminar sus datos del sistema.
```python
usuarios_activos = {"user_a": "activo", "user_b": "inactivo", "user_c": "activo"}
del usuarios_activos["user_b"]
print(f"Usuarios después de la limpieza: {usuarios_activos}")
```

**Ejemplo 2: Corregir un dato erróneo** ✏️

Supongamos que se agregó una entrada incorrecta a un registro.
```python
mediciones = {"temperatura": 25.5, "humedad": 60, "presion_erronea": 1012}
del mediciones["presion_erronea"]
print(f"Mediciones corregidas: {mediciones}")
```
