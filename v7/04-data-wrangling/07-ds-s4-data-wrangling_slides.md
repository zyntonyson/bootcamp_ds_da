@countdown{timer: 600 , title_transition: "¡Comenzamos en breve!", logo_animation: "traffic"}

# Sprint 4 Sesión 1
## Manipulación de datos (Data Wrangling)

---

@warnup-mood{title_transition: "Midamos los ánimos"}

# ¿Cómo llegas a la sesión de hoy?
## Reacciona con el emoji 😎🤔🤓🙂 que mejor represente tu mood

---
@agenda{title_transition: "Nuestra Agenda de Hoy"}

# Plan de nuestra sesión



* 👋 Bienvenida {5}
*  📊🧹 Revisión de conceptos de Data-Wranglig con datos de salud  (continuación) {60}
* 🔍👩‍💻 Quizz de repaso {10}
* 🤔 Reflexión y discusión: ¿Qué aprendimos en esta sesión? {5}

---
@objectives{title_transition: "¿Qué aprenderemos hoy?"}

# Metas de contenido para esta sesión

* 🛡️ **Realizar un casteo seguro de variables**
    * *Convertir tipos de datos evitando pérdida de información*
    * *Manejar valores inválidos o nulos durante la conversión*
* ⚙️ **Aplicar ingeniería de características en pandas**
    * *Crear nuevas variables a partir de datos existentes*
    * *Enriquecer el dataset para obtener mejores insights*
* 🧮 **Construir y manipular tablas pivote**
    * *Resumir y estructurar grandes volúmenes de datos*
    * *Agrupar información para facilitar su interpretación*
* 🔗 **Unir múltiples DataFrames**
    * *Combinar distintas fuentes de datos usando `merge` 
* 📊 **Generar gráficos de exploración en pandas**
    * *Visualizar la distribución y relación de los datos rápidamente*
    * *Identificar patrones, tendencias y valores atípicos*

---
@gotocode{title_transition: "Vamos al ejercicio"}


# Escanea el código para los materiales de la clase



* [Data Wrangling II](../../img/qrs/07-S4-Data-Wrangling-II.png)
---

@quizz{time_limit: 45}

# Pongamos a prueba lo aprendido
## Reaccciona en la llamada con el emoji de la respuesta correcta

quizz:
  - question:
      body: |
        Si ejecutas la siguiente línea de código en pandas, ¿cuál es su efecto principal?
        
        `df['precio'] = pd.to_numeric(df['precio'], errors='coerce')`
      items:
        - option: "😇 Convierte la columna 'precio' a texto y elimina los errores"
        - option: "😎 Convierte la columna a tipo numérico; los valores no convertibles serán NaN"
          correct: true
        - option: "👍 Suma todos los valores de la columna 'precio' ignorando los errores"
        - option: "😄 Redondea los números de la columna 'precio' a enteros"
      feedback: |
        ¡Exacto! El argumento `errors='coerce'` obliga a la función a transformar a NaN cualquier valor que no sea convertible a un número (por ejemplo, una letra o un símbolo suelto).

  - question:
      body: |
        Observa el siguiente DataFrame `ventas`:
        
        | Producto | Precio | Cantidad |
        | :--- | :--- | :--- |
        | A | 10 | 2 |
        | B | 15 | 3 |
        
        ¿Qué código usarías para crear una nueva columna llamada `Total` multiplicando `Precio` por `Cantidad`?
      items:
        - option: "😇 `ventas['Total'] = ventas['Precio'] + ventas['Cantidad']`"
        - option: "😎 `ventas['Total'] = ventas['Precio'] * ventas['Cantidad']`"
          correct: true
        - option: "👍 `ventas.Total = ventas.Precio % ventas.Cantidad`"
        - option: "😄 `ventas.insert('Total', ventas['Precio'] * ventas['Cantidad'])`"
      feedback: |
        ¡Correcto! En pandas, la manera más directa de crear una columna a partir de operaciones matemáticas con otras columnas es realizando la operación directamente sobre las Series (columnas).

  - question:
      body: |
        Analiza la siguiente línea de código:
        
        `df['precio_con_iva'] = df['precio_base'] * 1.16`
        
        ¿Cuál es la interpretación correcta de esta operación?
      items:
        - option: "😇 Calcula el promedio de 'precio_base' y lo multiplica por 1.16"
        - option: "😎 Filtra las filas donde 'precio_base' es mayor a 1.16"
        - option: "👍 Crea una columna nueva aplicando un aumento del 16% a cada valor individual de 'precio_base'"
          correct: true
        - option: "😄 Multiplica todos los valores del DataFrame entero por 1.16"
      feedback: |
        ¡Muy bien! Esta operación toma cada uno de los valores de la columna 'precio_base', lo multiplica por 1.16 y asigna el resultado a una columna nueva llamada 'precio_con_iva'.

  - question:
      body: |
        Tienes dos DataFrames (`clientes` y `compras`) y aplicas el siguiente código:
        
        `resultado = clientes.merge(compras, on='id_cliente')`
        
        ¿Qué describe mejor lo que hace este código?
      items:
        - option: "😇 Combina ambas tablas apilando las filas de `compras` debajo de las de `clientes`"
        - option: "😎 Une las columnas de ambas tablas, pero solo mantiene las filas donde el `id_cliente` coincide en ambos DataFrames"
          correct: true
        - option: "👍 Mezcla las tablas aleatoriamente sin importar si los datos corresponden al mismo cliente"
        - option: "😄 Elimina la columna `id_cliente` de ambos DataFrames"
      feedback: |
        ¡Así es! El método `merge` utiliza la columna indicada en `on` como clave para combinar las columnas de ambas tablas. Por defecto, solo conserva los registros que existen en ambos DataFrames.

  - question:
      body: |
        Tienes un DataFrame `empleados` y quieres visualizar rápidamente cómo se distribuyen sus edades en diferentes rangos para ver dónde se concentra la mayoría.
        
        ¿Cuál es la línea de código adecuada en pandas para generar este gráfico?
      items:
        - option: "😇 `empleados['edad'].plot(kind='hist')`"
          correct: true
        - option: "😎 `empleados['edad'].plot(kind='scatter')`"
        - option: "👍 `empleados['edad'].plot(kind='pie')`"
        - option: "😄 `empleados['edad'].plot(kind='bar')`"
      feedback: |
        ¡Excelente! El histograma (`kind='hist'`) es el gráfico ideal para observar la distribución de frecuencias de una variable numérica continua, agrupando los datos en intervalos.

---


@basic_slide{title_transition: "Ahora para finalizar"}

# 🎉 Espero que hayas disfrutado la sesión
## Qué te parece si:

* 🏃‍♂️ Continúa con tu avance en el sprint.
* 🚀 Trata de aplicar lo aprendido en un proyecto personal o tema de tu interés.
* 🤝 Participa en el Co-Learning para afianzar tus conocimientos mientras ayudas a otros a entenderlos.
* 💬 Comparte en nuestro canal de `community` algo que te haya gustado o llamado la atención de esta sesión.
* 🤖 Utiliza la IA de preferencia para que te genere alguna actividad extra para practicar lo aprendido.
* 📝 Al finalizar la sesión recibirás una encuesta de satisfacción, tus comentarios son muy valiosos para nosotros y me ayudará a mejorar como tutor.

---

@finale{}

# ¡Excelente trabajo! 🚀📊

## ¡Gracias por participar!
