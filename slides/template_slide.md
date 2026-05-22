<!-- 
=====================================================
PLANTILLA DE DIAPOSITIVAS (TEMPLATE SLIDES)
=====================================================
Este archivo es una guía con todos los tipos de 
diapositivas soportados por "create_slides.py".

Reglas Generales:
1. Cada diapositiva se separa de la anterior usando exactamente `---` en una línea vacía.
2. Cada diapositiva declara su tipo usando `@nombre_del_tipo`.
3. Opcionalmente, puedes pasar parámetros entre llaves: `{parametro1: "valor", parametro2: "valor"}`.
   * `title_transition`: Genera una pantalla verde dinámica de transición de n-segundos antes de mostrar la slide. Si lo omites, el salto será instantáneo.
4. El script extraerá automáticamente la línea de código que empiece con `# ` como el "Título", y `## ` como el "Subtítulo", sin importar el orden exacto dentro del texto.
5. Puedes incluir contenido externo reutilizable usando `@include(path="./ruta/al/archivo.md")` (usando llaves `{}` en lugar de paréntesis). Esto preprocesará el archivo cargando su contenido e insertará automáticamente el delimitador `---` para finalizar la diapositiva.
-->

@countdown{timer: 10 s, title_transition: "¡Comenzamos en breve!"}

# Título de Bienvenida
## Subtítulo o nombre del curso

Este texto inferior es opcional. El temporizador aceptará 's' (segundos) o 'm' (minutos).
Esta diapositiva extrae localmente la fecha de hoy usando JavaScript, colocándola en la esquina inferior izquierda.

---

@warnup-mood{title_transition: "Midamos los ánimos"}

# ¿Cómo llegas a la sesión de hoy?
## Reacciona con el emoji de tu teclado que mejor te represente

<!-- La slide 'warnup-mood' tiene una animación infinita de caída de emojis que cubre el fondo entero estilo cristal. -->

---

@warnup-question{title_transition: "¿Qué opinas al respecto?"}

# Pregunta interactiva

{left}
Escribe aquí todo tu texto reflexivo. La pantalla estará dividida en dos columnas.
Esta diapositiva utiliza un parseador legacy/antiguo con etiquetas {left} y {right}.

{right}
![Imagen de Ejemplo](https://www.python.org/static/community_logos/python-logo.png)

---

@agenda{title_transition: "Nuestra Agenda de Hoy"}

# Agenda de la sesión

<!-- 
La slide 'agenda' espera una lista con asteriscos en la cual incluyes al final el tiempo 
en minutos envuelto entre llaves `{}`.
-->

* Bienvenida {5}
* Introducción a la Teoría {25}
* Ejercicio Práctico en Plataforma {45}
* Repaso y Preguntas Anónimas {15}

---

@objectives{title_transition: "Nuestras metas"}

# Objetivos académicos de esta clase

<!-- La slide 'objectives' convierte de izquierda a derecha cada elemento de esta lista al formato "Tarjeta" (Cards). -->

* Comprender la lógica detrás del código.
* Entender qué es un Data Analytics.
* Poder exportar una visualización en Python.

---

@basic_slide{title_transition: "Conceptos Fundamentales"}

# Diapositiva Genérica (Markdown Completo)
## Tu imaginación es el límite

En la diapositiva **basic_slide** puedes usar TODO el poder de Markdown con alineación *justificada a la izquierda* sobre un panel transparente de bordes redondos.

Acepta toda clase de cosas, como esto:
1. Listas numeradas.
2. Más texto con [Enlaces hermosos](https://google.com).
3. Imágenes (se auto-centrarán con bordes curvos):

![Logo de R](https://upload.wikimedia.org/wikipedia/commons/thumb/1/1b/R_logo.svg/200px-R_logo.svg.png)

---

@quizz{time_limit: 15, title_transition: "¡Ponte a prueba!"}

# Título Principal del Quizz
## Subtítulo Evaluativo

> Texto introductorio que desaparecerá automáticamente al comenzar el Quizz interactivo 🚀

<!-- 
IMPORTANTE: El formato de los Quizz ahora se define usando YAML para permitir texto multilínea y bloques de código renderizables.
Recuerda usar EXACTAMENTE el símbolo pipe `|` inmediatamente después de keys como `body:`, `option:` o `feedback:` si el texto contiene o requiere saltos de línea (como código markdown o LaTeX). Asegúrate también de utilizar las listas mediante guiones (`-`).
-->

quizz:
  - question:
      body: |
        ¿Qué tipo de modelo agrupa datos sin etiquetas previas?
        
        *Ejemplo opcional de código bloqueado (Highlight.js los coloreará solos!):*
        ```python
        from sklearn.cluster import KMeans
        ```
      items:
        - option: "Aprendizaje Supervisado"
        - option: "Aprendizaje No Supervisado"
          correct: true
        - option: "Aprendizaje por Refuerzo"
        - option: "Deep Learning"
      feedback: |
        Es **No Supervisado** porque el algoritmo descubre estructuras libremente. Recuerda que aquí puedes usar LaTeX re-renderizable: $$E = mc^2$$

  - question:
      body: |
        Evalúa qué métrica es la que usualmente se busca minimizar por defecto al entrenar una Regresión Lineal:
      items:
        - option: "El Coeficiente de Determinación ($R^2$)."
        - option: "F1-Score."
        - option: "El Error Cuadrático Medio (MSE)."
          correct: true
      feedback: |
        ¡Excelente! La función de coste clásica busca reducir matemáticamente el $MSE$ de los residuales al mínimo posible.

---

@two_columns_slide{title_transition: "Comparación de Elementos"}

# Ventajas vs Desventajas

<!-- 
'two_columns_slide' parte la pantalla en un 50%-50%. 
La columna izquierda es un contenedor vertical inteligente que centra el texto matemáticamente.
La columna derecha es expansiva intentando que tu imagen llene el espacio disponible visual.
Usa las clases .left{...} y .right{...} literalmente con llaves para encapsular cada lado. 
-->

.left{
Aquí también puedo usar **todo tipo de estilos Markdown** sin ningún problema.

* Esta es la izquierda.
* La imagen de al lado estará perfectamente alineada al centro vertical respecto a mi.
}

.right{
![Logo Central Gigante](https://upload.wikimedia.org/wikipedia/commons/thumb/c/c3/Python-logo-notext.svg/200px-Python-logo-notext.svg.png)
}

---

@gotocode{title_transition: "Manos a la Obra"}

# Escanea el código para el ejercicio

<!-- 
La slide 'gotocode' asume que escribirás una "lista" (viñetas).
Pondrás el nombre del recurso entre llaves [] y pondrás un enlace de una IMAGEN para el Código QR entre paréntesis ().
Esto construirá visualmente los cuadros para tu pantalla. 
-->

* [Ejercicio Jupyter Notebook 1](https://upload.wikimedia.org/wikipedia/commons/thumb/8/86/Lorem_ipsum_design.svg/250px-Lorem_ipsum_design.svg.png)
* [Repositorio GitHub Oficial](https://upload.wikimedia.org/wikipedia/commons/thumb/8/86/Lorem_ipsum_design.svg/250px-Lorem_ipsum_design.svg.png)

---

<!-- 
=====================================================
INCLUSIÓN DE SLIDES EXTERNAS (@include)
=====================================================
Puedes incluir una diapositiva o un conjunto de diapositivas almacenadas en otro archivo markdown.
Esto es útil para avisos parroquiales, cambios de calendario o anuncios repetitivos en múltiples presentaciones.
Al final de la inclusión, el script agregará automáticamente la línea '---' para terminar la diapositiva.
-->

@include{path="./slides/out_office.md"}

---

@finale{title_transition: "Y para concluir..."}

# ¡Gracias inmensas!
## Quedo atento a todas tus dudas en Discord. Nos vemos.

<!-- 'finale' es tu pantalla de despedida en naranja vibrante, con el subtítulo gris oscuro imitando las estéticas iniciales. -->
