@countdown{timer: 600 , title_transition: "¡Comenzamos en breve!", logo_animation: "traffic"}

# Sprint 2 Sesión 1
## Transformar datos para insights de negocio

---

@warnup-mood{title_transition: "Midamos los ánimos"}

# ¿Cómo llegas a la sesión de hoy?
## Reacciona con el emoji 😎🤔🤓🙂 que mejor represente tu mood

---
@agenda{title_transition: "Nuestra Agenda de Hoy"}

# Plan de nuestra sesión


* 👋 Bienvenida {5}
* De los datos al insight: Preguntas análiticas de negocio 💼📊{35}
* Analisis exploratorio de datos: Caso Almacen Global   {45}
* 🤔 Reflexión y discusión: ¿Qué aprendimos en esta sesión? {5}

---
@objectives{title_transition: "¿Qué aprenderemos hoy?"}

# Metas de contenido para esta sesión

* 🎯 Conocer cómo definir el tipo de preguntas que se pueden hacer para analizar datos:
  * Comprender el problema central y los objetivos estratégicos del negocio.
  * Identificar stakeholders y sus necesidades.
* 📏 Conocer las diferentes métricas que se pueden calcular para analizar datos (KPIs, OKRs, Guardrails):
  * Definir indicadores clave de rendimiento (KPIs) para medir el éxito.
  * Conocer OKRs (Objectives and Key Results) y cómo utilizarlos para establecer metas.
* 🛠️ Aplicar herramientas de procesamiento y análisis de datos:
  * Funciones de búsqueda y concatenación de tablas (Vlookup).
  * Aplicar filtros avanzados para obtener información específica.
  * Crear tablas dinámicas para analizar datos.
* 💡 Crear visualizaciones para comunicar insights de negocio:
  * Seleccionar el gráfico más adecuado según la información a transmitir.
  * Aplicar principios de *storytelling* para facilitar la toma de decisiones.

---

@gotocode{title_transition: "Momento de trabajar en equipo"}

# ¡A trabajar en equipo!


* [Transformar datos para insights de negocio](../img/qrs/03-da-v8-insights-negocio.png)

---
@quizz{time_limit: 45}

# Pongamos a prueba lo aprendido
## Reaccciona en la llamada con el emoji de la respuesta correcta

quizz:
  - question:
      body: |
        Tu equipo de producto quiere entender por qué cayeron las ventas el mes pasado. Al estructurar la pregunta analítica de negocio, debes considerar varios aspectos para que sea accionable.
        
        ¿Cuál de los siguientes elementos **NO** es indispensable considerar al formular la pregunta de negocio?
      items:
        - option: "😇 El horizonte temporal (ej. 'durante el último mes')"
        - option: "😎 El mecanismo técnico de captura de datos (ej. 'API vs Webhook')"
          correct: true
        - option: "👍 La identidad del tomador de decisión"
        - option: "😄 Las variables para segmentación (ej. 'por tipo de usuario')"
      feedback: |
        ¡Correcto! El mecanismo de captura de datos es un detalle técnico. Las preguntas analíticas de negocio deben centrarse en el contexto del problema (tiempo, tomadores de decisión, segmentos) para generar *insights* accionables, sin importar cómo se extrajo la información.

  - question:
      body: |
        Una empresa de software lanza una agresiva campaña para adquirir nuevos usuarios ofreciendo un mes gratis. Para asegurar que este crecimiento no afecte la experiencia actual, monitorean constantemente la "Tasa de interrupciones del servicio (SAIFI)".
        
        ¿Qué tipo de métrica representa esta tasa en este contexto?
      items:
        - option: "😇 Un OKR (Objective and Key Result)"
        - option: "😎 Una métrica de vanidad"
        - option: "👍 Un KPI (Key Performance Indicator)"
        - option: "😄 Un Guardrail (Métrica de protección)"
          correct: true
      feedback: |
        ¡Exacto! Es un *Guardrail*. Mientras la empresa busca crecer agresivamente, necesita una métrica de protección para asegurarse de que ese crecimiento no degrade la calidad del servicio para los usuarios existentes.

  - question:
      body: |
        El director de operaciones de una red de distribución eléctrica revisa un tablero de control cada mañana. Su indicador principal para evaluar la eficiencia operativa del día a día es el "Costo promedio de mantenimiento por kWh distribuido".
        
        ¿A qué concepto corresponde esta métrica?
      items:
        - option: "😇 Un KPI (Key Performance Indicator)"
          correct: true
        - option: "😎 Un OKR estratégico"
        - option: "👍 Un Guardrail (Métrica de protección)"
        - option: "😄 Una métrica cualitativa"
      feedback: |
        ¡Muy bien! Es un KPI porque mide el desempeño continuo y la salud operativa del negocio a lo largo del tiempo, permitiendo evaluar si las operaciones son eficientes de manera constante.

  - question:
      body: |
        Al inicio del trimestre, el equipo de infraestructura de una startup define su gran meta transformacional: "Aumentar la disponibilidad promedio del sistema del 97.5% al 99% para el final del Q3".
        
        ¿Qué representa esta declaración?
      items:
        - option: "😇 Un Guardrail (Métrica de protección)"
        - option: "😎 Un OKR (Objective and Key Result)"
          correct: true
        - option: "👍 Un indicador descriptivo"
        - option: "😄 Una métrica de vanidad"
      feedback: |
        ¡Correcto! Es un OKR porque establece una meta específica, temporal y retadora (pasar de 97.5% a 99% en un trimestre), diseñada para alinear el esfuerzo del equipo hacia una mejora o salto cualitativo.

  - question:
      body: |
        Una cadena de supermercados notó una caída en sus ventas. El equipo de datos formula la siguiente pregunta: *"¿Qué factores y comportamientos causaron la disminución del 15% en las ventas de la categoría de lácteos durante el mes pasado?"*
        
        ¿Qué tipo de pregunta analítica es esta?
      items:
        - option: "😇 Descriptiva (¿Qué pasó?)"
        - option: "😎 Diagnóstica (¿Por qué pasó?)"
          correct: true
        - option: "👍 Predictiva (¿Qué pasará?)"
        - option: "😄 Prescriptiva (¿Qué deberíamos hacer?)"
      feedback: |
        ¡Excelente! Es una pregunta diagnóstica porque busca entender las **causas** o los factores detrás de un evento que ya ocurrió (la caída del 15% en ventas).

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
