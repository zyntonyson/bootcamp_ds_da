# Instrucciones Maestras: Generador de Presentaciones Python a HTML 🚀

*Este documento contiene el "prompt" o las especificaciones técnicas exhaustivas necesarias para que tú u otra Inteligencia Artificial puedan regenerar desde cero nuestro script Python (`create_slides.py`), respetando exactamente las funcionalidades únicas, las reglas visuales y la arquitectura iterada en nuestras sesiones.*

## 1. Descripción Principal y Dependencias
Debes crear un script CLI en Python llamado `create_slides.py` que reciba un archivo `.md` estructurado y genere automáticamente una presentación en HTML5 en un solo archivo (Single Page).
No está permitido usar frameworks complejos ni librerías HTML enormes de terceros. Usa Vanilla HTML, CSS puro, JavaScript plano, y confía la conversión de texto crudo exclusivamente al módulo de Python `markdown` (`pip install markdown`). Además incluye los módulos clásicos: `re`, `json`, `argparse`, `html`, `random` y `time`.

## 2. Paradigma de Interfaz y CSS (Estética "Glassmorphism")
La presentación está anclada a la tecnología y el minimalismo:
1. **Contenedor Principal (`.presentation`)**: Abarca `100vw` y `100vh` con `overflow: hidden`, ocultando y mostrando "slides" posicionados de forma absoluta.
2. **Glassmorphism (`.content-wrapper`)**: La abrumadora mayoría del contenido se sienta allí. Es un panel semitransparente con `rgba(255, 255, 255, 0.2)`, `backdrop-filter: blur(15px)`, bordes de 20px, y sombra sofisticada flotante. En su mejor versión, este contenedor domina hasta el 95% del ancho de la pantalla (`max-width: 1600px`).
3. **Logo Condicionado**: Carga un `<img>` absoluto en la esquina superior izquierda de la pantalla. Un CSS animation inyectado por un JavaScript en cada transición (`showAndHideLogo`) hace que descienda estéticamente por unos segundos y luego vuelva a esconderse hacia arriba lentamente, asegurando no hostigar visualmente al usuario.

## 3. Lógica del JavaScript (Navegación y Estados)
1. **Slides (Array)**: Controla el índice activo y manipula la clase `.active` afectando la opacidad y visibilidad de las capas.
2. **Cortinilla Verde Animada (`#transition-overlay`)**: Si el JS detecta que la siguiente diapositiva tiene atado un atributo HTML llamado `data-transition-title`, invoca una cortinilla pura (Verde esmeralda y textos negros gigantes) diciendo el título, la mantiene un segundo como entremés, y luego arroja al usuario a la verdadera diapositiva. *Nota: Esto solo ocurre cuando se avanza hacia adelante temporalmente; si se retrocede en los botones, el cambio es instantáneo*.
3. **Controles**: Flechas en pantalla (botones) empalmadas en esquina inferior derecha y *Listeners* para las flechas izquierda/derecha del teclado.

## 4. Parser de Markdown (Python Reglas Puras)
La arquitectura obliga a la rutina particionar primero el gran `.md` por la marca separadora: saltos de línea envueltos con `\n---\n`.
Una vez separados los bloques, el parseo aplica estas reglas:
- **Etiquetas Modulares**: La primera línea que elija su tipo usando el framework con llaves `@nombredeltipo{...}` (Ej. `@countdown{timer: 10 m, title_transition: "Tutor"}`). Es procesado usando un regex perdonable para leer diccionarios con comas dentro de comillas (para no cortar strings que lleven comas).
- **Títulos Automáticos**: Se tragan cualquier línea que empiece con exactamente `# ` y la designan como `<h1>`. `## ` pasa a ser `<h2>`.
- **Indulgencia de Espaciados**: Para mitigar errores de los usuarios escribiendo sub-listas de dos espacios de sangría que quiebren a la librería `markdown`, el Python ejecuta silenciosamente `re.sub(r'^ {2,3}([-*])', r'    \1')` para volverlos 4 espacios de forma forzada.

## 5. El Diccionario de Tipos de Slide 
Cada tipo de diapositiva lanza una función `_generate_[X]_html(slide)` distinta. Es vital reproducirlos con exactitud:

### `@countdown`
- **Misión**: Una pantalla espera naranja corporativa. Muestra un contador regresivo JS gigantesco. Tras agotarse, despliega "¡Comenzamos!". Inserta la Fecha Diaria generada mediante JS en la inferior izquierda. Excluye la insignia del Logo.

### `@warnup-mood`
- **Misión**: Sin cortinilla de cristal. Un contenedor HTML lanza infinitamente div's de emojis generados dinámicamente en Python (usando la librería `random`). Escoge de un array de 20 emojis, asignándoles anchos, opacidades, retrasos `-retraso s` y posiciones en viewport aleatorias forzándolos a descender por gravedad en CSS puramente ilimitado. Excluye Logo.

### `@agenda`
- **Misión**: Presenta los temas de clase en una lista desmarcada. Detecta regex en el formato `* Nombre {25}` y reemplaza automáticamente los datos en llaves para convertirlos a "25 min" pegados con un estilo gris suave.

### `@objectives`
- **Misión**: Interpreta listas crudas Markdown dentro de un contenedor `.objectives-container` gobernadas por Flexbox. 
- *CSS Rule*: Agarra los `<li>` primarios (el padre de las filas) y los forza a que se estiren en modo Card plástica con un `flex: 1`, `min-width: 300px`, `background: light-gray`, bordes fuertes, etc. Sus viñetas internas adquieren color corporativo. Si tienen un `<img>` crudo markdown como decoración, éste se enjaula en el centro con un rígido `max-height: 100px` para no escupirse de la tarjeta.

### `@gotocode`
- **Misión**: Una slide modo noche (`color-dark-mode`) diseñada para extraer expresiones RegEx de `* [Texto enlace](url.png)`. Coloca el PNG como código QR grandote con texto centrado abajo.

### `@two_columns_slide`
- **Misión**: Procesa bloques de `.left{}` y `.right{}`. Lo que esté en el centro izquierda pasará como string puro inyectado hacia `markdown.markdown()` a una div verticalizada flexible que centra por gravedad (`flex-direction: column; justify-content: center`). Lo que quede en medio de `.right{}` pasará al bloque derecho imponiendo a cualquier imagen que exista allí a tener `max-height: 70vh` acoplada bajo `object-fit: contain`. El Título Global (`# `) queda fuera, pegado en lo alto del vidrio.

### `@basic_slide`
- **Misión**: Simplemente vuelca el `markdown.markdown(content)` remanente alineado a la izquierda. Su tipografía base tiene márgenes amplísimos (`3rem` en pre-paddings, `1.5rem` el texto) asumiendo lectura intensiva. 

### `@overlay`
- **Misión**: "La Cortinilla Estática". Apaga el logo corporativo. Extradita la caja de vidrio esmerilado para que el fondo sea la pura negritud (`var(--color-black)`) de la pantalla. 
- *CSS Rule*: Cualquier texto nativo en Markdown que escape como simple párrafo `<p>` está predestinado por CSS a estirarse masivamente a `3rem` en negritas medias y con color totalmente blanco brillante (`color-white-soft`) alineado al estricto centro para fungir como subtítulo cinematográfico.

### `@quizz`
- **Misión**: Presenta un cuestionario interactivo de forma cronometrada y de revelación autónoma ("Flashcards flip"). 
- *Formato de Entrada*: Acepta un parámetro `{time_limit: N}` (siempre un entero en segundos). Extrae la estructura markdown usando reconocimiento estricto de indentación: Las preguntas base inician con `* `, las opciones se encierran bajo un item principal titulado `    * Options:` y la justificación bajo `    * Feedback:`. La opción verdadera debe estar marcada explícitamente con `{correct: true}` en el mismo renglón de la alternativa.
- *Lógica JS/CSS*: Instala una máquina de estados independiente. Tras iniciar, retira ocultamente su texto introductorio (bloque `> `), dibuja la pregunta en curso y detona el reloj interno. Al agotar sus recursos visuales (0s), evalúa sin clics: opaca a grises tenues las respuestas estipuladas como incorrectas y le inyecta una vigorosa animación de rotación 3D sobre su eje `X` (`.flip-correct`) bañando de verde a la tarjeta acertada, revelando concurrentemente la caja transparente del Feedback y atando temporalmente el botón de Continuidad para habilitar proseguir a placer del portavoz (sino salta reevaluándolo pasados `N` segundos adicionales). Posee mini-paginador enumerado para viajes no-lineales entre la trivia, e integra a nivel CDN la asincronía de la librería nativa **MathJax**, invocando `MathJax.typesetPromise()` como refresco visual en cada salto para resolver las sentencias formales cerradas con signaturas `$$...$$` a la perfección de papel impreso.

### `@finale`
- **Misión**: Exime logos y vidrios. Toda la pantalla se baña en Naranja y sus letras quedan oscuras, finalizando.

## Output
Al correr en la terminal mediante `python create_slides.py --input_file slide.md --output_file final.html`, el script ensambla una cadena gigante inyectando un bloque f-string universal con el viewport, las librerías `style`, los motores CSS documentados arriba, el HTML iterado en el loop, y el JS cerrando todo.
