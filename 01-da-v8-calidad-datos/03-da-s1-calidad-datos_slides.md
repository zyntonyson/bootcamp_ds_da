@countdown{timer: 600 , title_transition: "¡Comenzamos en breve!", logo_animation: "traffic"}

# Sprint 1 Sesión 3
## Asegura la calidad de los datos y genera reportes básicos

---

@warnup-mood{title_transition: "Midamos los ánimos"}

# ¿Cómo llegas a la sesión de hoy?
## Reacciona con el emoji 😎🤔🤓🙂 que mejor represente tu mood

---
@agenda{title_transition: "Nuestra Agenda de Hoy"}

# Plan de nuestra sesión



* 👋 Bienvenida {10}
*  📊🧹 Proyecto colaborativo: MexStay   {55}
* 🔍👩‍💻 Quizz de repaso {10}
* 🤔 Reflexión y discusión: ¿Qué aprendimos en esta sesión? {5}

---
@objectives{title_transition: "¿Qué aprenderemos hoy?"}

# Metas de contenido para esta sesión

* 🧹 **Aplicar técnicas de limpieza de datos**
    * *Corregir formatos inconsistentes*
    * *Tratar valores nulos o duplicados*
* 🧮 **Calcular métricas descriptivas**
    * *Obtener promedios, medianas y frecuencias*
    * *Resumir información clave del dataset*
* 📊 **Generar visualizaciones de datos**
    * *Crear gráficos básicos para analizar tendencias*
    * *Facilitar la interpretación de la información*
* 💡 **Descubrir insights en los datos**
    * *Identificar patrones y relaciones ocultas*
    * *Generar conclusiones útiles a partir de los datos*
---


@gotocode{title_transition: "Momento de trabajar en equipo"}

# ¡A trabajar en equipo!


* [Trabajo en equipo: MexStay](../img/qrs/03-da-s1-calidad-datos.png)


---

@quizz{time_limit: 60}

# Pongamos a prueba lo aprendido
## Reaccciona en la llamada con el emoji de la respuesta correcta

quizz:
  - question:
      body: |
        Observa la siguiente tabla de datos sobre ciudades:
        
        | Ciudad Original | Ciudad Limpia |
        | :--- | :--- |
        | `  mExiCo  ` | `Mexico` |
        | `bOgOtA ` | `Bogota` |
        
        ¿Qué funciones de Google Sheets nos permiten pasar de la "Ciudad Original" a la "Ciudad Limpia"?
      items:
        - option: "😇 SUMAR() y EXTRAE()"
        - option: "😎 ESPACIOS()  y NOMPROPIO()"
          correct: true
        - option: "👍 BUSCARV() y LIMPIAR()"
        - option: "😄 FILTRAR() y ORDENAR()"
      feedback: |
        ¡Excelente! La función ESPACIOS() (o TRIM) elimina los espacios extra al principio y al final, y NOMPROPIO() (o PROPER) estandariza la primera letra en mayúscula y las demás en minúscula, logrando el formato limpio.

  - question:
      body: |
        Si tienes el texto `"manzana-pera-platano"` en la celda A1 y aplicas la fórmula `=SPLIT(A1, ",")`, ¿cuál será el resultado?
      items:
        - option: "😇 Tres celdas con `manzana`, `pera` y `platano`"
        - option: "😎 Un error porque faltan comillas en la fórmula"
        - option: "👍 El texto queda igual en una sola celda "
          correct: true
        - option: "😄 Dos celdas con `manzana-pera` y `platano`"
      feedback: |
        ¡Así es! Para que la función SPLIT divida el texto, el carácter separador indicado en la fórmula debe estar presente en la cadena original. Como aquí usamos una coma pero el texto tiene guiones, no se realiza ninguna separación.

  - question:
      body: |
        ¿Para qué nos sirve principalmente la función `UNIQUE()` en Google Sheets cuando estamos limpiando datos?
      items:
        - option: "😇 Para sumar los valores de una columna sin contar los repetidos"
        - option: "😎 Para extraer una lista de valores únicos, eliminando automáticamente los duplicados"
          correct: true
        - option: "👍 Para encontrar errores ortográficos en una columna de texto"
        - option: "😄 Para combinar dos columnas en una sola sin mezclar los datos"
      feedback: |
        ¡Correcto! La función `UNIQUE()` analiza un rango de celdas y nos devuelve únicamente los valores distintos, siendo una herramienta muy rápida y eficiente para deshacernos de la información repetida.
  - question:
      body: |
        Observas que en una columna de "Ventas", al intentar sumar los valores usando la fórmula `=SUMA(A1:A10)`, el resultado es `0`. Al revisar, notas que los números están alineados a la izquierda. ¿Cuál es la causa más probable de este error?
      items:
        - option: "😇 La función SUMA() no funciona con más de 5 celdas a la vez"
        - option: "😎 Los números tienen un tamaño de fuente muy pequeño y Sheets los ignora"
        - option: "👍 Los valores están guardados con formato de Texto, no como Números"
          correct: true
        - option: "😄 La celda donde pusiste el resultado no tiene suficiente espacio"
      feedback: |
        ¡Exacto! Cuando los números están guardados como texto (generalmente se alinean a la izquierda por defecto), las funciones matemáticas como SUMA o PROMEDIO los ignoran. Para solucionarlo, debemos cambiar el formato de la columna a "Número" o usar funciones como VALOR().
  - question:
      body: |
        Tienes una tabla donde el nombre de una ciudad aparece de diferentes formas por errores de tipeo: `CDMX`, `Cdmx` y `Cd. de Mexico`. Si quieres unificar todos a `Ciudad de México` de forma rápida sin usar fórmulas, ¿qué herramienta de Google Sheets es la mejor opción?
      items:
        - option: "😇 La función EXTRAE() para sacar letra por letra"
        - option: "😎 La herramienta integrada de 'Buscar y reemplazar' (Find and Replace)"
          correct: true
        - option: "👍 Borrar la columna y volver a escribir todo manualmente para evitar errores"
        - option: "😄 Ordenar la columna de la Z a la A y pintarlas de colores"
      feedback: |
        ¡Correcto! La herramienta 'Buscar y reemplazar' (Ctrl + H o Cmd + Shift + H) es excelente para la limpieza de datos rápida. Nos permite buscar un patrón incorrecto específico y cambiarlo masivamente por el valor estandarizado correcto en segundos.

---



@include{path="../slides/farewell.md"}

