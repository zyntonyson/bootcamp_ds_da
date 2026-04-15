@countdown{timer: 600 , title_transition: "¡Comenzamos en breve!", logo_animation: "traffic"}

# Sprint 7 Sesión 3
## Análisis estadístico para detectar patrones y outliers


---

@warnup-mood{title_transition: "Midamos los ánimos"}

# ¿Cómo llegas a la sesión de hoy?
## Reacciona con el emoji 😎🤔🤓🙂 que mejor represente tu mood

---

@agenda{title_transition: "Nuestra Agenda de Hoy"}

# Agenda de la sesión



* 👋 Bienvenida {5}
* 📚 Repaso de conceptos del sprint {10}
* 🔎 Revisión de proyectos del sprint {10}
* 🐙 Cómo publicar nuestros proyectos en GitHub {15}
* 🤝 Proyecto colaborativo: Caso Megaline {50}
* 🤔 Reflexión y discusión: ¿Qué aprendimos en esta sesión? {10}


---

@objectives{title_transition: "¿Qué aprenderemos hoy?"}

# Objetivos académicos de esta clase

 
*  Python aplicado a limpieza de datos 🐍 ♻️
    * 🔀 Uso de condicionales
    * 🛠️ Uso de funciones
    * 🔄 Uso de bucles
*  Diseño de Datapipelines 🐼 📈
    * 🧹 Limpieza de datos
    * ⚠️ Manejo de datos atípicos
    * 🚫 Manejo de datos nulos
* 📊 Análisis estadístico de datos
    * 🔪 Segmentación de datos con pandas
    * 📉 Descripción estadística de datos 
* Publicación de proyectos en GitHub 🐙
    * 🚀 Cargar un reporte de datos desde collab




---

@quizz{time_limit: 20, title_transition: "¡Repasemos algunos conceptos!"}

# Quizz de repaso
## Análisis estadístico para detectar patrones y outliers

> Responde en el chat con el emoji de la respuesta correcta

* ¿Cuál es el criterio estándar basado en el Rango Intercuartílico (IQR) para identificar un valor atípico (outlier)?
    * Options:
        * 😄 Menor a $Q1 - 1.5 \times IQR$ o mayor a $Q3 + 1.5 \times IQR${correct: true}
        * 👍 Menor a $Q1 - 2.0 \times IQR$ o mayor a $Q3 + 2.0 \times IQR$
        * 😎 Menor a $Q2 - 1.5 \times IQR$ o mayor a $Q2 + 1.5 \times IQR$
        * 😇 Mayor al 99° percentil o menor al 1° percentil
    * Feedback:
        * ¡Correcto! La regla de Tukey establece que los valores atípicos son aquellos que caen por debajo de $Q1 - 1.5 \times IQR$ o por encima de $Q3 + 1.5 \times IQR$.


* ¿Qué significa que un patrón de datos nulos sea MCAR (Missing Completely At Random)?
    * Options:
        * 😄 Los datos faltan debido a un error sistemático y predecible.
        * 👍 La probabilidad de que falte un dato depende de otras variables observadas.
        * 😎 La probabilidad de pérdida del dato es constante, aleatoria, e independiente.{correct: true}
        * 😇 La probabilidad de que falte depende del valor de la propia variable no observada.
    * Feedback:
        * ¡Muy bien! MCAR (Perdidos completamente al azar) implica que la ausencia del dato es un evento puramente aleatorio y sin relación con atributos observados o no observados.


* ¿Qué tipo de gráfico es estadísticamente el más idóneo para visualizar la distribución de los cuartiles y detectar valores atípicos rápidamente?
    * Options:
        * 😄 Gráfico de dispersión (Scatter plot)
        * 👍 Histograma de frecuencias
        * 😎 Diagrama de barras invertido
        * 😇 Diagrama de caja (Boxplot){correct: true}
    * Feedback:
        * ¡Exacto! El Boxplot dibuja la caja intercuartílica y permite visualizar directamente todos los puntos que superan el límite de los "bigotes" estadísticos.


* Cuando identificas errores o valores atípicos severos (outliers) en tu dataset, ¿cuáles son las tres técnicas metodológicas principales que solemos considerar para tratarlos?
    * Options:
        * 😄 Ocultarlos visualmente, convertirlos a string, o sumarles el valor de la media.
        * 👍 Reemplazarlos por ceros, duplicar sus filas, o multiplicarlos por el desvío estándar.
        * 😎 Hacer nada (mantenerlos), eliminarlos directamente, o acotarlos/Winsorizar.{correct: true}
        * 😇 Interpolar o usar sentinels, rellenar hacia adelante (ffill), y convertirlos a enteros negativos.
    * Feedback:
        * ¡Exacto! Frente a un outlier, dependiendo del negocio, podemos considerar **hacer nada** si son fenómenos reales, **eliminarlos** si son errores groseros, o **acotarlos (Winsorización)** para mitigar su efecto marcando umbrales máximos/mínimos.


* ¿Qué técnica de imputación de datos nulos es más apropiada si sospechas que la ausencia de un valor depende de la categoría a la que pertenece la fila (por ejemplo, el salario de un empleado podría depender de su departamento)?
    * Options:
        * 😄 Imputar siempre con la media global del dataset.
        * 👍 Imputar con el valor anterior (forward fill).
        * 😎 Imputar con la mediana o media del grupo específico (por departamento, por ejemplo).{correct: true}
        * 😇 Eliminar la fila directamente sin reemplazar el valor.
    * Feedback:
        * ¡Muy bien! Cuando la probabilidad de tener un valor nulo depende de otras variables (MAR), la imputación por grupo (usando la mediana o media de ese grupo) suele ser más precisa que la global.

---

@gotocode{title_transition: "Manos a la Obra"}

# Escanea el código para los materiales de la clase



* [Sprint 7 · Análisis estadístico para detectar patrones y outliers III](../img/qrs/21-da-v8-preparacion-datos.png)
* [Sprint 7 · Análisis estadístico para detectar patrones y outliers IV: Proyecto Megaline](../img/qrs/22-da-v8-preparacion-datos.png)

---

@finale{}

# ¡Gracias inmensas!

## Tu asistencia y participación hacen que la clase sea muy valiosa
