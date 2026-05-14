@countdown{timer: 600 , title_transition: "¡Comenzamos en breve!", logo_animation: "traffic"}

# Sprint 9 Sesión 1
## Valida hipótesis de negocio con pruebas estadísticas


---

@warnup-mood{title_transition: "Midamos los ánimos"}

# ¿Cómo llegas a la sesión de hoy?
## Reacciona con el emoji 😎🤔🤓🙂 que mejor represente tu mood

---

@agenda{title_transition: "Nuestra Agenda de Hoy"}

# Plan de nuestra sesión



* 👋 Bienvenida {5}
* 🔎 Pruebas de hipótesis  {90}
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

@gotocode{title_transition: "Manos a la Obra"}

# Escanea el código para los materiales de la clase



* [Sprint 9 · Valida hipótesis de negocio con pruebas estadísticas](../img/qrs/25-pruebas-hipotesis.png)


---

@quizz{time_limit: 50}

# Pongamos a prueba lo aprendido
## Reaccciona en la llamada con el emoji de la respuesta correcta

quizz:
  - question:
      body: |
        ¿Cuál es la importancia principal de realizar experimentación en los negocios?
      items:
        - option: "😇 Asegurar que todas las decisiones de la empresa se tomen por instinto o experiencia previa."
        - option: "😎 Permite medir el impacto causal de los cambios y decisiones, reduciendo la incertidumbre y maximizando métricas clave."
          correct: true
        - option: "👍 Identificar únicamente correlaciones sin evidencia formal, acelerando los procesos de lanzamiento a ciegas."
        - option: "😄 Detener los desarrollos ágiles debido al inmenso costo y tiempo que representan las pruebas estadísticas."
      feedback: |
        **La experimentación de negocio y las pruebas A/B** proveen información causal rigurosa, limitando drásticamente el riesgo de tomar decisiones basadas únicamente en la intuición de la gerencia.

  - question:
      body: |
        Al momento de plantear una prueba de hipótesis estadística, ¿cuál de las siguientes opciones describe correctamente a su diseño?
      items:
        - option: "😇 La hipótesis nula ($H_0$) se asume inicialmente como cierta y usualmente representa 'no hay efecto', mientras la hipótesis alternativa ($H_1$) es la afirmación que tratamos de demostrar experimentalmente."
          correct: true
        - option: "😎 Ambas hipótesis deben afirmar exactamente lo contrario a lo que intenta el experimento, para descartar primero las posibilidades lógicas."
        - option: "👍 La hipótesis alternativa ($H_1$) sirve solo como punto de partida extremo o poco probable, donde se asume que existe poco o ninguna relación entre variables."
        - option: "😄 La hipótesis nula ($H_0$) siempre debe reflejar un salto extremo en las métricas y la alternativa ($H_1$) probar todo lo contrario."
      feedback: |
        ¡Correcto! **$H_0$ parte del statu quo o de la igualdad**, y buscamos recolectar la suficiente información muestral (evidencia) para rechazarla formalmente y estar tranquilos validando nuestra $H_1$.

  - question:
      body: |
        Desde la formalidad y la estadística, ¿cuál de estas declaraciones es la que interpreta genuinamente al valor $p$ (p-value)?
      items:
        - option: "😇 Nos dice directamente si la hipótesis nula ($H_0$) es totalmente falsa en el mundo real."
        - option: "😎 Es qué tan 'raros' o extremos serían nuestros resultados si asumiéramos que la hipótesis nula ($H_0$) es cierta."
          correct: true
        - option: "👍 Mide exactamente la probabilidad de que nuestra hipótesis alternativa sea cierta."
        - option: "😄 Nos da la certeza absoluta (100%) de que nuestra hipótesis nula ($H_0$) sea  verdad."
      feedback: |
        ¡Excelente! Recuerda que **el $p$-valor NO es una medida incondicional** de la veracidad de la hipótesis. Concretamente nos cuenta qué tan _'raros'_ habrían sido nuestros datos observados si, de facto, no existiera un efecto o anomalía.

  - question:
      body: |
        **Caso Práctico:** Estás analizando el comportamiento de varios clientes en una plataforma. 
        Quieres saber si el *sistema operativo* que utilizan (iOS, Android, Web) está relacionado estadísticamente con el *plan al que están suscritos* (Básico, Premium, VIP). 
        
        ¿Qué técnica estadística es la más adecuada para responder tus sospechas?
      items:
        - option: "😇 Una prueba $t$ de Student  para los conteos."
        - option: "😎 Usar una prueba de proporciones por categoria o Z-test."
        - option: '👍 Construir una prueba $\chi^2$ (Chi-cuadrada) de independencia.'
          correct: true
        - option: "😄 Aplicar una prueba de homogeneidad de varianzas para los grupos."
      feedback: |
        Utilizamos Chi-cuadrada precisamente para evaluar en el nivel cualitativo la **relación probabilística o de independencia entre dos o más variables categóricas** (Sistema Operativo frente a Plan Suscrito).

  - question:
      body: |
        Si tuvieras que explicarlo con tus propias palabras... ¿Qué significa realmente fijar un umbral alfa (Nivel de Significancia, $\alpha$) antes de empezar un experimento?
      items:
        - option: "😇 Es el riesgo máximo que aceptamos correr para equivocarnos diciendo que descubrimos algo nuevo, cuando en la realidad eso era falso."
          correct: true
        - option: "😎 Es el porcentaje de veces que nos vamos a equivocar a propósito concluyendo que no hubo cambios, cuando la idea en el fondo sí era verdadera."
        - option: "👍 Es simplemente un medida que nos avisa a cuántos usuarios exactos tenemos que encuestar para que el estudio funcione."
        - option: "😄 Es la herramienta que usamos para obligar a nuestros datos a que se acomoden a una perfecta forma de campana normal."
      feedback: |
        ¡Exactamente! Con $\alpha$ ($0.05, 0.01$, etc.) le estamos marcando un límite realista al experimento. Básicamente le decimos a la estadística: **"Solo vamos a celebrar que descubrimos algo si hay muy poco riesgo de que sea pura coincidencia"**. Así controlamos el riesgo de equivocarnos y rechazar la $H_0$ cuando era verdadera.

---

@finale{}

# ¡Gracias inmensas!

## Tu asistencia y participación hacen que la clase sea muy valiosa
