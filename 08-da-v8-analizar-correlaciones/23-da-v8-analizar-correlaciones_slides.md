@countdown{timer: 600 , title_transition: "¡Comenzamos en breve!"}

# Sprint 8 Sesión 1 
## Explorar conexiones de datos con correlaciones 


---

@warnup-mood{title_transition: "Midamos los ánimos"}

# ¿Cómo llegas a la sesión de hoy?
## Reacciona con el emoji 😎🤔🤓🙂 que mejor represente tu mood

---

@agenda{title_transition: "Nuestra Agenda de Hoy"}

# Agenda de la sesión

* 👋 Bienvenida {5}
* 💼 Caso de estudio: German city Bank {40}
* 🤔 Reflexión y discusión: ¿Qué aprendimos en esta sesión? {5}


---
@objectives{title_transition: "¿Qué vamos a practicar?"}

# Objetivos académicos de esta clase

* 📈 Calcular métricas de correlaciones
    * **Calcular Pearson** para medir la fuerza y dirección de relaciones lineales continuas.
    * **Calcular Spearman** para evaluar relaciones monótonas y mitigar el impacto de outliers.
    * **Calcular la correlación punto biserial** para medir asociaciones entre variables continuas y binarias.
    * **Calcular la V de Cramér** para determinar la fuerza de asociación entre variables categóricas.
* 🧠 Interpretar resultados de análisis de correlación
    * **Analizar visualmente** relaciones complejas usando herramientas gráficas como `pairplot` y `heatmap`.
* ⚖️ Integrar pensamiento ético en el análisis de correlación
    * **Evaluar críticamente** el uso analítico de variables sensibles como género, edad o vivienda.
    * **Prevenir sesgos discriminatorios** al estructurar modelos de decisión basados en correlaciones.
    * **Documentar supuestos y limitaciones** estadísticas para asegurar un uso responsable del análisis.


---

@gotocode{title_transition: "Manos a la Obra"}

# Escanea el código para los materiales de la clase



* [Explorar conexiones de datos con correlaciones I](../img/qrs/23-da-v8-analizar-correlaciones.png )

---
@quizz{time_limit: 80}

# Pongamos a prueba lo aprendido
## Reaccciona en la llamada con el emoji de la respuesta correcta

quizz:
  - question:
      body: |
        Si calculamos el coeficiente de correlación de Pearson entre el número de horas que un cliente demora en pagar su saldo y su historial de crédito, y obtenemos un valor de $-0.78$, ¿cómo debemos interpretar este resultado?
      items:
        - option: "😇 Existe una relación fuerte y directa: a mayor retraso en el pago, mejor historial de crédito del cliente."
        - option: "😎 Existe una relación inversa fuerte: a mayor retraso en el pago, menor tiende a ser su historial de crédito."
          correct: true
        - option: "👍 No existe ninguna relación lineal entre las dos variables debido a que el coeficiente es menor a cero."
        - option: "😄 El tiempo de demora en el pago es la causa directa del deterioro en un 78% del historial de crédito."
      feedback: |
        ¡Correcto! Un coeficiente de Pearson de $-0.78$ indica una relación lineal negativa (inversa) y fuerte. Significa que al aumentar una variable, la otra tiende a disminuir.

  - question:
      body: |
        El equipo de riesgos de German City Bank quiere medir si existe alguna relación o asociación entre la **Situación Habitacional** de un cliente (casa propia, rentada o libre) y si el cliente es clasificado como **Riesgo Alto o Riesgo Bajo**. ¿Qué métrica de correlación o asociación es la más adecuada?
      items:
        - option: "😇 Coeficiente de Pearson, porque ambas variables son continuas."
        - option: "😎 Coeficiente de Spearman, ya que las variables no siguen una distribución normal."
        - option: "👍 Correlación punto biserial, debido a que una variable es continua y la otra es binaria."
        - option: "😄 V de Cramér, porque ambas variables son categóricas (cualitativas)."
          correct: true
      feedback: |
        ¡Excelente! Tanto la 'Situación Habitacional' como el 'Riesgo' son variables categóricas. La **V de Cramér** es la métrica adecuada para evaluar el nivel de asociación entre dos variables cualitativas.

  - question:
      body: |
        Observa la siguiente matriz de correlación lineal simulada para tres variables de los clientes del banco:
        
        ```text
        | Variables      | Edad | Monto_Credito | Ingresos |
        |----------------|------|---------------|----------|
        | Edad           | 1.00 |  0.15         |  0.45    |
        | Monto_Credito  | 0.15 |  1.00         |  0.72    |
        | Ingresos       | 0.45 |  0.72         |  1.00    |
        ```
        
        ¿Cuál de las siguientes afirmaciones es estadísticamente correcta?
      items:
        - option: "😇 La edad del cliente determina e incrementa de forma directa el monto de crédito que se le aprueba."
        - option: "😎 Existe una relación lineal positiva fuerte entre los ingresos del cliente y el monto de crédito ($0.72$)."
          correct: true
        - option: "👍 No existe ninguna relación entre la edad y los ingresos de los clientes, ya que su valor es de $0.45$."
        - option: "😄 La correlación de $0.15$ entre la edad y el monto del crédito es la asociación más fuerte de la matriz."
      feedback: |
        ¡Correcto! El coeficiente de $0.72$ entre `Ingresos` y `Monto_Credito` representa la relación positiva más fuerte de la matriz. Las relaciones de $0.45$ y $0.15$ indican asociaciones moderada-débil y débil respectivamente.

  - question:
      body: |
        Si descubrimos una correlación estadística en los datos históricos del banco entre la variable 'Género' del solicitante y la tasa de incumplimiento, es éticamente correcto y justificable usar esta correlación de manera automática para rechazar créditos y mitigar riesgos.
      items:
        - option: "😇 Verdadero"
        - option: "😎 Falso"
          correct: true
      feedback: |
        ¡Así es! Usar variables sensibles como género o etnia para tomar decisiones automatizadas de crédito refuerza sesgos históricos. Aunque exista una asociación estadística, la ética exige no discriminar por características demográficas.

  - question:
      body: |
        Un análisis en una tienda muestra que las ventas de helados y las ventas de bloqueadores solares tienen una correlación positiva fuerte ($0.85$). Por lo tanto, podemos concluir que comprar helado provoca directamente que la gente compre bloqueador solar.
      items:
        - option: "😇 Verdadero"
        - option: "😎 Falso"
          correct: true
      feedback: |
        ¡Correcto! Este es un ejemplo de correlación espuria producida por una variable oculta (el clima cálido o el verano). Ambas variables aumentan debido al calor, pero comer helado no causa la compra de bloqueador solar. ¡Correlación no implica causalidad!


---

@include{path="./slides/farewell.md"}