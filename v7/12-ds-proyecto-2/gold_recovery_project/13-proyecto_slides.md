@countdown{timer: 600 , title_transition: "¡Comenzamos en breve!", logo_animation: "traffic"}

# Sprint 13
## Proyecto del módulo 2

---

@warnup-mood{title_transition: "Midamos los ánimos"}

# ¿Cómo llegas a la sesión de hoy?
## Reacciona con el emoji 😎🤔🤓🙂 que mejor represente tu mood

---
@agenda{title_transition: "Nuestra Agenda de Hoy"}

# Plan de nuestra sesión


* 👋 Bienvenida {5}
* 🐍 Revisión del proyecto del módulo 2 💻📊 {75}
* 🤔 Reflexión y discusión: ¿Qué aprendimos en esta sesión? {5}

---
@objectives{title_transition: "¿Qué aprenderemos hoy?"}

# Objetivos de la sesión

* 🎯 Comprender el contexto de negocio y el reto industrial para Zyfra.
* ⚙️ Identificar las habilidades clave de Data Science a practicar en el proyecto.
* 🔬 Dominar el proceso tecnológico de flotación, la nomenclatura de variables y las métricas.

---

@basic_slide{title_transition: "1. Contexto del Proyecto"}

# Contexto de Negocio: Minería & Zyfra
## Optimización del proceso industrial de extracción de oro

* **La Empresa:** **Zyfra** desarrolla soluciones industriales basadas en IA y Machine Learning para optimizar la eficiencia y rentabilidad en minería y extracción pesada.
* **El Problema de Negocio:**
  * La extracción de oro a partir del mineral bruto es un proceso físico-químico altamente costoso.
  * Operar la planta con parámetros desfavorables o mineral de baja ley genera pérdidas económicas significativas y desperdicio de reactivos químicos.
* **El Objetivo de Machine Learning:**
  * Predecir el **coeficiente de recuperación de oro** en dos etapas críticas: flotación y purificación final.
  * Facilitar la toma de decisiones para operar la planta únicamente bajo condiciones rentables.
* **Particularidad de los Datos Industriales:**
  * Datos reales indexados cronológicamente (`date`).
  * **Desfase temporal:** Ciertas variables se miden al instante (sensores), pero otras requieren horas de laboratorio. El conjunto de prueba simula la producción en tiempo real (sin variables futuras ni targets), exigiendo evitar la fuga de datos (*data leakage*).

---

@objectives{title_transition: "2. Habilidades a Desarrollar"}

# Habilidades a Practicar en el Sprint
## Competencias técnicas y metodológicas en un entorno industrial real

* 🧪 **Preparación y Validación de Datos**
  * *Verificar fórmulas de dominio físico (`recovery`) contrastando cálculos con el MAE.*
  * *Identificar discrepancias entre datasets de train y test para evitar fuga de datos.*
  * *Manejar series temporales e imputación coherente según vecindad cronológica.*
* 📊 **Análisis Exploratorio Industrial (EDA)**
  * *Analizar la evolución de concentraciones de metales (Au, Ag, Pb) en cada etapa.*
  * *Comparar distribuciones del tamaño de grano (`feed_size`) entre entrenamiento y prueba.*
  * *Identificar y tratar valores anómalos o lecturas en cero en concentraciones totales.*
* 🤖 **Modelado Supervisado y Métrica Custom**
  * *Construir funciones personalizadas de evaluación para sMAPE y sMAPE ponderado.*
  * *Entrenar y comparar múltiples modelos de regresión (Lineal, Árboles, Random Forest).*
  * *Implementar validación cruzada (K-Fold) y evaluar el desempeño frente a un modelo base.*

---

@basic_slide{title_transition: "3. Proceso Tecnológico"}

# El Proceso Tecnológico de Extracción
## ¿Cómo se obtiene el oro a partir del mineral bruto?

1. **Alimentación y Reactivos (Rougher Feed & Additions):**
   * El mineral extraído y triturado se mezcla con reactivos químicos:
     * **Xantato:** Colector y promotor/activador de la flotación.
     * **Sulfato de sodio:** Modificador de la química de la pulpa.
     * **Depresante (Silicato de sodio):** Inhibe la flotación de impurezas y ganga.
2. **Flotación (Rougher Process):**
   * La mezcla entra a celdas de flotación con inyección de aire. Las burbujas atrapan las partículas ricas en oro formando el **concentrado rougher**, mientras que los residuos caen como **colas rougher**.
   * 🎯 **Primer Objetivo de Predicción:** `rougher.output.recovery`
3. **Purificación en Dos Etapas (Cleaner Process):**
   * **Primera etapa (Primary cleaner):** Limpieza preliminar del concentrado rougher para retirar más impurezas.
   * **Segunda etapa (Secondary cleaner):** Segunda ronda de limpieza fina.
4. **Concentrado Final (Final Output):**
   * Se obtiene el concentrado con la máxima pureza de oro junto con las colas finales.
   * 🎯 **Segundo Objetivo de Predicción:** `final.output.recovery`

---

@basic_slide{title_transition: "Estructura de Datos"}

# Nomenclatura Sistemática de Variables
## Convención: [stage].[parameter_type].[parameter_name]

Las 87 variables del dataset siguen una estructura jerárquica estandarizada:

| Elemento | Valores Posibles | Descripción / Ejemplos |
| :--- | :--- | :--- |
| **`[stage]`** | `rougher` / `primary_cleaner` / `secondary_cleaner` / `final` | Etapa tecnológica del proceso físico-químico. |
| **`[parameter_type]`** | `input` / `output` / `state` / `calculation` | Tipo de parámetro: materia prima, producto obtenido, estado operativo o cálculo derivado. |
| **`[parameter_name]`** | `feed_au`, `feed_size`, `tail_au`, `air_amount`, `recovery` | Parámetro físico, químico o métrica específica. |

* **Ejemplos prácticos en el código:**
  * `rougher.input.feed_au`: Proporción de oro en la alimentación entrante a la flotación.
  * `primary_cleaner.state.air_amount`: Volumen de aire inyectado en la purificación primaria.
  * `rougher.output.recovery` y `final.output.recovery`: Las dos variables objetivo a predecir.
* ⚠️ **¿Por qué el test set tiene solo 53 columnas?**
  En producción real, cuando el mineral entra a la planta solo se conocen variables `input` y de `state`. Los parámetros `output` y `calculation` ocurren después del proceso industrial.

---

@basic_slide{title_transition: "Métricas y Evaluación"}

# Métricas Clave de Evaluación
## Cálculo de Recuperación y sMAPE Ponderado

* **Fórmula de Recuperación de Mineral ($Recuperación$):**
  $$Recuperación = \frac{C \times (F - T)}{F \times (C - T)} \times 100\%$$
  * **$C$:** Proporción de oro en el concentrado tras la etapa correspondiente.
  * **$F$:** Proporción de oro en la alimentación antes de iniciar la etapa.
  * **$T$:** Proporción de oro en las colas residuales de dicha etapa.

* **Métrica sMAPE (Error Medio Absoluto Porcentual Simétrico):**
  $$sMAPE = \frac{1}{N} \sum_{i=1}^{N} \frac{|y_i - \hat{y}_i|}{(|y_i| + |\hat{y}_i|) / 2} \times 100\%$$
  * Evalúa el error relativo de manera simétrica, considerando equitativamente la magnitud real y la predicción.

* **Métrica Final Ponderada del Proyecto:**
  $$sMAPE_{final} = 25\% \times sMAPE(rougher) + 75\% \times sMAPE(final)$$
  * El concentrado final tiene 3 veces más peso ($75\%$) en la evaluación del negocio que la flotación preliminar ($25\%$).

---

@basic_slide{title_transition: "Ruta de Trabajo"}

# Flujo de Trabajo del Proyecto
## Paso a paso para completar el Sprint 13 con éxito

1. **Preparación de Datos:**
   * Cargar datasets (`train`, `test`, `full`) con índice temporal (`date`).
   * Verificar fórmula de recuperación calculando el MAE contra `rougher.output.recovery` ($MAE \approx 0$).
   * Analizar columnas ausentes en el test set y preprocesar nulos con imputación temporal (`ffill`).
2. **Análisis Exploratorio de Datos (EDA):**
   * Monitorear cómo cambia la concentración de metales ($Au$, $Ag$, $Pb$) entre etapas.
   * Comparar distribuciones del tamaño de grano (`feed_size`) entre train y test (deben ser consistentes).
   * Identificar y remover valores atípicos (anomalías de concentraciones totales en cero).
3. **Construcción y Evaluación de Modelos:**
   * Programar las funciones personalizadas para `sMAPE` y `sMAPE_final`.
   * Entrenar modelos de regresión (`LinearRegression`, `DecisionTreeRegressor`, `RandomForestRegressor`).
   * Evaluar con validación cruzada K-Fold, optimizar hiperparámetros y validar en test contra un modelo base (*dummy*).

---

@include{path="../../../slides/farewell.md"}
