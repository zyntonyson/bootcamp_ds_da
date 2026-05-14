@countdown{timer: 600 , title_transition: "¡Comenzamos en breve!", logo_animation: "traffic"}

# Sprint 9 Sesión 2
## Valida hipótesis de negocio con pruebas estadísticas


---

@warnup-mood{title_transition: "Midamos los ánimos"}

# ¿Cómo llegas a la sesión de hoy?
## Reacciona con el emoji 😎🤔🤓🙂 que mejor represente tu mood

---

@agenda{title_transition: "Nuestra Agenda de Hoy"}

# Plan de nuestra sesión



* 👋 Bienvenida {5}
* 📊🧹 Quizz de repaso: Pruebas de hipótesis {15}
* 📊🧹 Revisión del proyecto del Sprint {10}
* 🔎 Pruebas de hipótesis. Actividad colaborativa  {60}
* 🤔 Reflexión y discusión: ¿Qué aprendimos en esta sesión? {10}

---


@objectives{title_transition: "¿Qué aprenderemos hoy?"}

# Metas de contenido para esta sesión

* 🧠 Conocer qué son las pruebas de hipótesis y su estructura
    * 📝 Formular y plantear la hipótesis nula ($H_0$) y alternativa ($H_1$)
    * 🔬 Comprender el uso y la interpretación del valor $p$
* 🧪 Diseñar tests A/B
    * 🔀 Definir grupos de control y de prueba
    * 🎯 Seleccionar las métricas adecuadas para evaluar el experimento
* ⚖️ Tomar decisiones basadas en evidencia estadística 
    * 📉 Interpretar los resultados de las pruebas estadísticas
    * 💼 Traducir los hallazgos en recomendaciones de negocio accionables

---

@quizz{time_limit: 60}

# Pongamos a prueba lo aprendido en el Sprint
## Reaccciona en la llamada con el emoji de la respuesta correcta

quizz:
  - question:
      body: |
        Al realizar una prueba de hipótesis, utilizamos varios conceptos para tomar una decisión. ¿Cuál de los siguientes NO es un elemento de una prueba de hipótesis estadística?
      items:
        - option: "😇 Grupo de enfoque (Focus group)"
          correct: true
        - option: "😎 Nivel de significancia (Alfa)"
        - option: "👍 Valor p (p-value)"
        - option: "😄 Hipótesis nula y alternativa"
      feedback: |
        ¡Correcto! El grupo de enfoque es una técnica de investigación cualitativa de mercado, no un elemento matemático o estadístico de una prueba de hipótesis. Los demás son fundamentales para plantear y evaluar una prueba.

  - question:
      body: |
        Estás evaluando si un nuevo diseño de página web aumenta el tiempo de sesión. Definiste un nivel de significancia (alfa) de 0.05. Al correr la prueba, obtienes un p-valor de 0.02. ¿Cuál es la conclusión correcta?
      items:
        - option: "😇 Aceptamos la hipótesis nula porque el p-valor es menor que alfa. El diseño no tuvo ningún impacto."
        - option: "😎 Rechazamos la hipótesis nula porque el p-valor (0.02) es menor que alfa (0.05). Hay evidencia de que el nuevo diseño tiene un efecto."
          correct: true
        - option: "👍 Rechazamos la hipótesis alternativa porque el p-valor es positivo. Debemos regresar al diseño anterior."
        - option: "😄 No podemos concluir nada porque el p-valor debe ser mayor a 0.5 para poder tomar una decisión."
      feedback: |
        ¡Exacto! La regla general es: si el p-valor es menor o igual a nuestro nivel de significancia (alfa), rechazamos la hipótesis nula ($H_0$), apoyando nuestra hipótesis alternativa ($H_1$).

  - question:
      body: |
        Una tienda en línea cree que ofrecer "Envío Gratis" aumentará el gasto promedio de sus clientes y quieren comprobarlo estadísticamente. ¿Cómo deberían plantear sus hipótesis?
      items:
        - option: "😇 $H_0$: El gasto promedio es diferente. $H_1$: El gasto promedio es igual."
        - option: "😎 $H_0$: El envío gratis aumenta las visitas a la página. $H_1$: El envío gratis no aumenta las visitas."
        - option: "👍 $H_0$: El gasto promedio es igual con o sin envío gratis. $H_1$: El gasto promedio es diferente con envío gratis."
          correct: true
        - option: "😄 $H_0$: El envío gratis disminuye el gasto promedio. $H_1$: El envío gratis aumenta el gasto promedio."
      feedback: |
        ¡Así es! La Hipótesis Nula ($H_0$) siempre asume que no hay diferencia o efecto (el gasto es igual). La Hipótesis Alternativa ($H_1$) plantea que sí hay un cambio (el gasto es diferente).

  - question:
      body: |
        Quieres saber si existe una relación o dependencia entre el "Tipo de suscripción" (Básica o Premium) y el "Dispositivo principal" que usan los usuarios (Celular, Tablet, Computadora). Ambas variables son categóricas. ¿Qué prueba estadística debes elegir?
      items:
        - option: "😇 Prueba T de Student para medias"
        - option: "😎 Prueba Z para proporciones"
        - option: "👍 Prueba ANOVA para múltiples grupos"
        - option: "😄 Prueba de Independencia Chi-cuadrada"
          correct: true
      feedback: |
        ¡Correcto! La prueba Chi-cuadrada de independencia se utiliza cuando queremos ver si dos variables categóricas están relacionadas o son independientes, analizando las frecuencias conjuntas en una tabla de contingencia.

  - question:
      body: |
        Un analista presenta el siguiente plan: "Queremos probar si la nueva campaña funciona. Mi hipótesis alternativa ($H_1$) es que las ventas se mantienen igual. Si el p-valor es mayor a mi alfa de 0.05, entonces la campaña fue un éxito." ¿Cuál es el principal error en este planteamiento?
      items:
        - option: "😇 El alfa debió ser 0.10, de lo contrario la prueba no funciona."
        - option: "😎 Está usando la hipótesis alternativa ($H_1$) para asumir que 'no hay cambios', cuando eso le corresponde a la hipótesis nula ($H_0$)."
          correct: true
        - option: "👍 El error es comparar el p-valor con el alfa; ambos valores deberían sumarse."
        - option: "😄 No hay ningún error, el planteamiento es estadísticamente perfecto."
      feedback: |
        ¡Muy bien detectado! El analista confundió las hipótesis. La Hipótesis Nula ($H_0$) es la que debe plantear el statu quo ("no pasa nada", las ventas se mantienen igual), mientras que la Alternativa ($H_1$) es lo que quiere demostrar.

---

@gotocode{title_transition: "Manos a la Obra"}

# Escanea el código para los materiales de la clase



* [Sprint 9 · Valida hipótesis de negocio con pruebas estadísticas II](../img/qrs/26-pruebas-hipotesis.png)


---


@finale{}

# ¡Gracias inmensas!

## Tu asistencia y participación hacen que la clase sea muy valiosa
