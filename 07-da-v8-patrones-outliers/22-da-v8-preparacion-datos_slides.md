@countdown{timer: 600 , title_transition: "¡Comenzamos en breve!", logo_animation: "traffic"}

# Sprint 7 Sesión 4
## Análisis estadístico para detectar patrones y outliers


---

@warnup-mood{title_transition: "Midamos los ánimos"}

# ¿Cómo llegas a la sesión de hoy?
## Reacciona con el emoji 😎🤔🤓🙂 que mejor represente tu mood

---

@agenda{title_transition: "Nuestra Agenda de Hoy"}

# Agenda de la sesión



* 👋 Bienvenida {5}
* 🔎 Revisión del proyecto del sprint {10}
* 🤝 Proyecto colaborativo: Caso Megaline {60}
* 📚 Quizz de repaso de conceptos del sprint {10}
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

@gotocode{title_transition: "Manos a la Obra"}

# Escanea el código para los materiales de la clase


* [Sprint 7 · Análisis estadístico para detectar patrones y outliers IV: Proyecto Megaline](../img/qrs/22-da-v8-preparacion-datos.png)

---
@quizz{time_limit: 70, title_transition: "¡Repasemos algunos conceptos!"}

# Quizz de repaso
## Análisis estadístico para detectar patrones y outliers

> Reacciona en el chat con el emoji de la respuesta correcta

quizz:
  - question:
      body: |
        Si calculamos el rango intercuartílico (IQR) de los ingresos mensuales de nuestros clientes y nos da un valor muy grande. ¿Qué nos indica principalmente esto en el contexto de la detección de datos atípicos?
      items:
        - option: "😄 Que no existen datos atípicos en absoluto."
        - option: "👍 Que el 50% central de los datos tiene una gran dispersión, lo que puede alejar los límites (bigotes) y dificultar clasificar como atípico un valor distante."
          correct: true
        - option: "😇 Que la mayoría de los usuarios ganan el salario mínimo."
        - option: "❤️ Que la media es exactamente igual a la mediana."
      feedback: |
        El IQR mide la dispersión del 50% central. Un IQR grande empuja los límites $Q_1 - 1.5 \times IQR$ y $Q_3 + 1.5 \times IQR$ hacia los extremos, minimizando la cantidad de atípicos pero requiriendo que los puntos sean excesivamente altos o bajos para ser detectados.

  - question:
      body: |
        Imagina que tienes una base de datos médicos con mediciones. Descubres 3 pacientes con valores imposibles en presión arterial (ej. -50 mmHg). Al revisar, notas que fue un error de captura aislado, pero el resto de las columnas para estos individuos son clave para el modelo. ¿Qué harías?
      items:
        - option: "😄 Eliminar los renglones completos para limpiar el dataset."
        - option: "👍 Acotar los valores a los percentiles 5 y 95."
        - option: "😇 Imputar estos valores atípicos con la media o mediana, ya que la información de las demás columnas de esos pacientes es valiosa."
          correct: true
        - option: "❤️ No tocar, es mejor dejar los datos tal y como llegaron al sistema."
      feedback: |
        Dado que eliminar la fila causaría pérdida de información útil en otras columnas y el error está focalizado, lo más recomendable es **imputar** el valor irreal con un estadístico para conservar la muestra.

  - question:
      body: |
        Observa la siguiente tabla sobre datos atípicos detectados al segmentar el tipo de suscripción:
        
        | Plan | % de la base | % de Atípicos detectados |
        |------|-------------|---------------|
        | Básico | 60% | 2% |
        | Pro  |   30%   | 4% |
        | Premium | 10% | 45% |
        
        Si decides **eliminar** todos los datos atípicos del dataset, ¿cuál será el patrón principal de pérdida de datos?
      items:
        - option: "😄 Perderemos principalmente usuarios del Plan Básico por ser la mayoría de la base."
        - option: "👍 La pérdida de datos será aleatoria y equitativa entre todos los planes."
        - option: "😇 Perderemos a casi la mitad de los usuarios del plan Premium, afectando fuertemente la representatividad de ese segmento clave."
          correct: true
        - option: "❤️ No hay pérdida real de datos porque los atípicos siempre son falsos."
      feedback: |
        ¡Excelente análisis! Al eliminar los atípicos a ciegas estamos borrando sistemáticamente casi el 50% del comportamiento de los usuarios **Premium**, creando un sesgo grave en nuestro conjunto de datos.

  - question:
      body: |
        Si decides calcular tus métricas estadísticas sin tratar antes los datos atípicos extremos que existen en tu dataset, ¿cuál será el impacto más probable en tu análisis?
      items:
        - option: "😄 La precisión de tus estadísticas aumentará porque estás usando absolutamente todos los datos disponibles."
        - option: "👍 Las funciones de pandas generarán los resultados más rápidos al no tener que filtrar."
        - option: "😇 Las medidas como la media (promedio) se verán fuertemente sesgadas, siendo empujadas artificialmente hacia los valores atípicos."
          correct: true
        - option: "❤️ No hay impacto real, las fórmulas estadísticas básicas ignoran automáticamente los valores atípicos."
      feedback: |
        Recordemos que medidas estadísticas como la media aritmética son **muy sensibles** a los atípicos. Un solo dato extremo (como una compra multimillonaria de error) puede inflar drásticamente el promedio, dándote una visión distorsionada de tu población y llevando a un análisis incorrecto.

  - question:
      body: |
        En tu pipeline de preprocesamiento, en pandas, agregaste el siguiente código:
        
        ```python
        q1 = df['ventas'].quantile(0.25)
        q3 = df['ventas'].quantile(0.75)
        iqr = q3 - q1
        
        limite_superior = q3 + 1.5 * iqr
        
        df.loc[df['ventas'] > limite_superior, 'ventas'] = limite_superior
        ```
        ¿Qué estrategia técnica para el tratamiento de valores atípicos se está ejecutando aquí?
      items:
        - option: "😄 Imputación utilizando la mediana."
        - option: "👍 Eliminación (pérdida de renglones completos)."
        - option: "😇 No hacer nada, se están copiando los mismos valores."
        - option: "❤️ Acotar los datos extremos, reemplazándolos con un valor umbral (Clipping)."
          correct: true
      feedback: |
        ¡Correcto! En lugar de eliminar las filas, se identifican los valores por encima del umbral y se **acotan** para que sean exactamente iguales al _límite superior_. Esto permite retener el resto de la información válida sin crear ceros u omitir renglones enteros.

---

@finale{}

# ¡Gracias inmensas!

## Tu asistencia y participación hacen que la clase sea muy valiosa
