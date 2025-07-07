
🎓 *Webinar 1: Del dato a la decisión: fundamentos de experimentación A/B*

**Formato:** Guía del docente + participación  
**Duración sugerida:** 75-90 min

---

🎯 *Objetivos académicos*

* Comprender los fundamentos de la verificación de hipótesis y su aplicación en negocios.
* Aplicar los criterios ICE y RICE para evaluar hipótesis y tomar decisiones informadas.

---

📌 *¿Por qué experimentar en negocios?*

En un entorno competitivo, las decisiones deben estar respaldadas por datos. El enfoque *data-driven* permite tomar decisiones informadas en lugar de actuar por intuición. Experimentar permite validar ideas, reducir riesgos y maximizar impacto con evidencia.

**Ejemplos de experimentos en negocios:**
* *Cualitativo*: entrevistas para conocer motivaciones de cancelación de suscripciones.
* *Cuantitativo*: test A/B para evaluar si una nueva oferta mejora la tasa de conversión.
* *Test A/A*: evaluar si la infraestructura de medición es confiable.

> *Una empresa que decide rediseñar su landing page debe medir el impacto del cambio, no solo lanzarlo a ciegas.*

---

🧪 *¿Qué hace buena una experimentación cuantitativa?*

Todo parte de una **hipótesis clara, medible y comprobable**. Si una hipótesis es ambigua o demasiado general, los resultados no ofrecerán conclusiones útiles.

**Ejemplo de hipótesis vaga:**
> Cambiar la página principal mejorará la experiencia del usuario.

**Ejemplo de hipótesis clara:**
> Si reducimos el tiempo de carga de la homepage en un 30%, la tasa de conversión aumentará al menos un 5%.

🔑 Criterios para una buena hipótesis:
* Clara y específica
* Medible con una métrica relevante
* Falsable
* Basada en observaciones o datos previos

---

📊 *¿Cómo decidir qué hipótesis probar?*

📋 *Framework ICE*

Fórmula:  
`ICE = (Impact × Confidence) / Effort`

📋 *Framework RICE*

Fórmula:  
`RICE = (Reach × Impact × Confidence) / Effort`

---

🧪 *Ejemplo práctico en Python*
```python
import pandas as pd

hipotesis = pd.DataFrame({
    'idea': ['Agregar CTA', 'Reducir pasos de compra', 'Cambiar color del botón'],
    'reach': [8, 6, 9],
    'impact': [7, 9, 4],
    'confidence': [8, 6, 5],
    'effort': [3, 7, 2]
})

hipotesis['ICE'] = (hipotesis['impact'] * hipotesis['confidence']) / hipotesis['effort']
hipotesis['RICE'] = (hipotesis['reach'] * hipotesis['impact'] * hipotesis['confidence']) / hipotesis['effort']

print(hipotesis.sort_values(by='RICE', ascending=False))
```

---

🔬 *Pruebas A/B: Diseño de un buen test*

Una prueba A/B compara dos versiones de algo para identificar cuál tiene mejor rendimiento en una métrica clave.

🧠 *Conceptos fundamentales*

📏 *Tamaño de muestra*
Fórmula:
```
n = (2 * (Z_alpha/2 + Z_beta)^2 * p(1 - p)) / d^2
```
Donde:
- `Z_alpha/2`: valor z para el nivel de significancia (ej. 1.96 para 95%)
- `Z_beta`: valor z para la potencia deseada (ej. 0.84 para 80%)
- `p`: tasa de conversión estimada
- `d`: diferencia mínima detectable

⏱️ *Duración mínima*  
Debe cubrir ciclos naturales (días de semana y fines de semana). No se debe cortar la prueba antes del tiempo estimado.

⚠️ *Errores comunes*  
- **Tipo I (α)**: Falso positivo.
- **Tipo II (β)**: Falso negativo.

🔢 *Comparaciones múltiples: A/B/n*

Al probar más de 2 versiones aumenta la probabilidad de falsos positivos. Por eso se ajustan los p-valores con:

* **Bonferroni**: α' = α / n → Muy conservador.
* **Holm**: Ajuste progresivo. Menos conservador.
* **Sidak**: Asume independencia.
  `α' = 1 - (1 - α)^(1/n)`

> *La idea central es proteger la tasa de error cuando se hacen muchas comparaciones.*

---

🚫 *¿Cuándo no hacer un test A/B?*

* Poca muestra (no alcanza potencia).
* Hipótesis mal definida.
* Entorno incontrolable.
* Hay evidencia previa sólida.

---

🧪 *Ejemplo práctico de prueba A/B en Python*
```python
from scipy import stats

grupo_a = [1]*40 + [0]*960  # 40 conversiones / 1000 visitas
grupo_b = [1]*55 + [0]*945  # 55 conversiones / 1000 visitas

stat, p = stats.ttest_ind(grupo_a, grupo_b)

print(f"Estadístico: {stat:.4f}, p-valor: {p:.4f}")

if p < 0.05:
    print("✅ Hay diferencia significativa")
else:
    print("❌ No hay diferencia significativa")
```
