# 📊 Valida hipótesis de negocio con pruebas estadísticas I

¡Hola a todos y bienvenidos a este webinar! 👋 Hoy vamos a sumergirnos en el fascinante mundo de las pruebas de hipótesis. Aprenderemos a usar la estadística para tomar decisiones de negocio basadas en datos. ¡Prepárense para potenciar sus habilidades analíticas! 🚀

## Objetivos academicos 🎯

Al final de esta sesión, serás capaz de:

1.  **Formular hipótesis de negocio**: Aprenderás a traducir una pregunta de negocio en una hipótesis nula y una alternativa.
2.  **Aplicar pruebas estadísticas**: Realizarás pruebas T y chi-cuadrado para comparar grupos y evaluar resultados de experimentos.
3.  **Interpretar resultados**: Sabrás cómo interpretar un p-value y comunicar tus conclusiones en un lenguaje claro y accionable para el negocio.

## Ejercicio de práctica 📈

Imagina que trabajas para **"E-Shop Now"**, una tienda online que quiere mejorar su tasa de conversión. El equipo de diseño ha creado una nueva página de destino (landing page) y cree que es mucho más atractiva que la actual. Pero, ¿realmente funciona mejor? 🤔

Para descubrirlo, han lanzado un experimento A/B:
*   **Grupo A**: Ve la página de destino antigua.
*   **Grupo B**: Ve la nueva página de destino.

Nuestro trabajo es analizar los datos de este experimento y determinar si la nueva página (B) es realmente mejor que la A. ¡Vamos a usar nuestros superpoderes de datos para encontrar la respuesta! 💪

### Dinamica de la actividad 🤝

¡Es hora de trabajar en equipo! 🎉

Vamos a dividirlos en salas de Zoom. Cada equipo será un equipo de analistas de datos de "E-Shop Now". Su misión será:

1.  **Limpiar los datos**: Asegurarse de que el conjunto de datos esté listo para el análisis.
2.  **Explorar los datos**: Calcular métricas clave y visualizar los resultados.
3.  **Realizar pruebas de hipótesis**: Aplicar las pruebas estadísticas correctas para comparar las páginas A y B.
4.  **Sacar conclusiones**: Presentar sus hallazgos como si se los estuvieran mostrando al CEO.

¡La colaboración es clave! Discutan sus ideas, compartan sus pantallas y ayúdense mutuamente. ¡El equipo que presente las conclusiones más claras y fundamentadas ganará... nuestro eterno respeto! 😎

### Datos 💾

Empecemos por cargar nuestro conjunto de datos. Usaremos un archivo CSV que simula los resultados del experimento A/B.

Columnas del dataset:

*   `user_id`: identificador único del usuario.
*   `date`: fecha en que el usuario participó en el experimento.
*   `landing`: variante del experimento (A o B).
*   `converted`: si convirtió (1) o no (0).
*   `gasto`: gasto del usuario.
*   `region`: región del usuario.
*   `dispositivo`: dispositivo usado por el usuario.
*   `traffic_source`: fuente de tráfico.
*   `user_type`: tipo de usuario (nuevo o recurrente).

¡Manos al código! 💻

```python
import pandas as pd

df = pd.read_csv("https://raw.githubusercontent.com/ljpiere/tpdata_python/refs/heads/main/DA/datasets/landing_experiment_sintetico_40k.csv")
df.head()
```

### Calidad de datos y limpieza 🧹

> "La basura entra, la basura sale".

Un buen análisis siempre comienza con datos de alta calidad. Vamos a aplicar un checklist para asegurarnos de que nuestros datos estén limpios y sean confiables.

**Checklist de limpieza:**

*   **¿Hay valores faltantes?**: `df.isnull().sum()`
*   **¿Hay user_id duplicados?**: `df.user_id.duplicated().sum()`
*   **¿`landing` solo tiene 'A' y 'B'?**: `df.landing.value_counts()`
*   **¿`converted` solo tiene 0 y 1?**: `df.converted.value_counts()`
*   **¿`gasto` tiene valores negativos?**: `df[df.gasto < 0]`
*   **Definir la ventana temporal del experimento**: `df.date.min(), df.date.max()`

```python
# Valores faltantes
print("Valores faltantes por columna:")
print(df.isnull().sum())

# Duplicados
print(f"\nNúmero de user_id duplicados: {df.user_id.duplicated().sum()}")

# Valores únicos en columnas categóricas
print("\nValores en 'landing':")
print(df.landing.value_counts())

print("\nValores en 'converted':")
print(df.converted.value_counts())

# Revisar gastos negativos
print(f"\nGastos negativos: {len(df[df.gasto < 0])}")

# Ventana temporal
df['date'] = pd.to_datetime(df['date'])
print(f"\nVentana del experimento: {df.date.min().date()} a {df.date.max().date()}")

```
Parece que no tenemos problemas serios de calidad. ¡Genial! 🎉

### Analisis exploratorio (EDA) 📊

Ahora que nuestros datos están limpios, vamos a explorarlos para entender mejor el comportamiento de los usuarios.

**Conversión global:**

```python
conversion_global = df.converted.mean()
print(f"Tasa de conversión global: {conversion_global:.2%}")
```

**Métricas por grupo (landing page):**

```python
import matplotlib.pyplot as plt
import seaborn as sns

# Tasa de conversión por landing
conversion_por_landing = df.groupby('landing')['converted'].mean()
print("Tasa de conversión por landing:")
print(conversion_por_landing)

sns.barplot(x=conversion_por_landing.index, y=conversion_por_landing.values)
plt.title('Tasa de Conversión (A vs B)')
plt.ylabel('Tasa de Conversión')
plt.show()

# Gasto promedio por landing (solo convertidos)
gasto_por_landing = df[df.converted == 1].groupby('landing')['gasto'].mean()
print("\nGasto promedio por landing (solo convertidos):")
print(gasto_por_landing)

sns.barplot(x=gasto_por_landing.index, y=gasto_por_landing.values)
plt.title('Gasto Promedio (A vs B) - Convertidos')
plt.ylabel('Gasto Promedio')
plt.show()
```

**Análisis por otras dimensiones:**

Exploremos si la fuente de tráfico, el dispositivo o la región tienen algún impacto.

```python
# Conversion por fuente de tráfico
conv_traffic = df.groupby(['traffic_source', 'landing'])['converted'].mean().unstack()
print("\nConversión por Fuente de Tráfico y Landing:")
print(conv_traffic)
conv_traffic.plot(kind='bar', title='Conversión por Fuente de Tráfico', ylabel='Tasa de Conversión')
plt.show()

# Conversion por dispositivo
conv_device = df.groupby(['dispositivo', 'landing'])['converted'].mean().unstack()
print("\nConversión por Dispositivo y Landing:")
print(conv_device)
conv_device.plot(kind='bar', title='Conversión por Dispositivo', ylabel='Tasa de Conversión')
plt.show()
```

> 💡 **Reflexión**: El análisis exploratorio nos da pistas. Vemos algunas diferencias, pero... ¿son estas diferencias *estadísticamente significativas* o solo producto del azar? ¡Las pruebas de hipótesis nos darán la respuesta!

### Experimentos 🔬

¡Llegó el momento de la verdad! Vamos a realizar las pruebas estadísticas para tomar una decisión basada en datos.

#### Gasto promedio (A vs B)

**Pregunta**: Entre quienes convirtieron (converted = 1), ¿el gasto promedio es diferente en A vs B?

*   **Hipótesis Nula (H₀)**: El gasto promedio es el *mismo* en A y B.
*   **Hipótesis Alternativa (H₁)**: El gasto promedio es *diferente* en A y B.

Usaremos una **prueba T de Student** para muestras independientes, ya que estamos comparando la media de dos grupos.

```python
from scipy import stats

# Paso 1: Filtrar solo convertidos
convertidos_A = df[(df.landing == 'A') & (df.converted == 1)]
convertidos_B = df[(df.landing == 'B') & (df.converted == 1)]

# Paso 2: Calcular promedios y tamaños
promedio_A = convertidos_A.gasto.mean()
promedio_B = convertidos_B.gasto.mean()
n_A = len(convertidos_A)
n_B = len(convertidos_B)

print(f"Promedio A: {promedio_A:.2f}, Muestra A: {n_A}")
print(f"Promedio B: {promedio_B:.2f}, Muestra B: {n_B}")

# Paso 3: Visualizar
sns.histplot(convertidos_A.gasto, color='skyblue', label='A', kde=True)
sns.histplot(convertidos_B.gasto, color='red', label='B', kde=True)
plt.title('Distribución del Gasto (Convertidos)')
plt.legend()
plt.show()

# Paso 4: Correr prueba T
t_stat, p_value = stats.ttest_ind(convertidos_A.gasto, convertidos_B.gasto)

print(f"\nP-value de la prueba T: {p_value:.4f}")
```

**Conclusión en lenguaje de negocio**

Completa:

*   **Promedio A**: `______`
*   **Promedio B**: `______`
*   **p-value**: `______`
*   **Conclusión (1–2 frases)**:
    > "Con un nivel de significancia del 5%, _________ evidencia de que el gasto promedio entre convertidos sea diferente entre A y B.
    En términos prácticos, B tiene un gasto promedio _________ que A (mayor/menor/similar)."

#### Tasa de conversión (A vs B)

**Pregunta**: ¿La versión B convierte una proporción distinta de usuarios que la A?

*   **Hipótesis Nula (H₀)**: La tasa de conversión es la *misma* en A y B.
*   **Hipótesis Alternativa (H₁)**: La tasa de conversión es *diferente* en A y B.

Usaremos una **prueba de Chi-cuadrado (χ²)** porque estamos comparando proporciones entre dos grupos.

```python
from scipy.stats import chi2_contingency

# Paso 1: Crear tabla de contingencia
tabla_contingencia = pd.crosstab(df.landing, df.converted)
print("Tabla de contingencia:")
print(tabla_contingencia)

# Paso 2: Correr prueba chi-cuadrado
chi2, p_value, _, _ = chi2_contingency(tabla_contingencia)

print(f"\nP-value de la prueba Chi-cuadrado: {p_value:.4f}")
```

**Conclusión en lenguaje de negocio**

Completa:

*   **Tasa de conversión A**: `______` (ej. 10.5%)
*   **Tasa de conversión B**: `______` (ej. 12.2%)
*   **p-value**: `______`
*   **Conclusión (1–2 frases)**:
    > "Con un nivel de significancia del 5%, ________ evidencia para afirmar que la tasa de conversión de la página B es diferente a la de la A.
    En términos prácticos, esto sugiere que la nueva página B ________ un impacto significativo en la conversión (tiene/no tiene)."

¡Excelente trabajo, equipo! 🚀 Han aprendido a usar datos para validar decisiones de negocio. Este es uno de los superpoderes más importantes de un analista de datos. ¡Sigan practicando y nunca dejen de preguntar "por qué"!