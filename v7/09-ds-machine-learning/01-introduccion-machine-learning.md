# 🤖 Introducción al *Machine Learning*

> *"El Machine Learning le da a las computadoras la capacidad de aprender sin ser explícitamente programadas."* — Arthur Samuel

Bienvenid@ a esta sesión. Hoy daremos nuestros primeros pasos en el fascinante mundo del **aprendizaje automático**. No te preocupes si es la primera vez que escuchas estos términos, vamos paso a paso 🚀.

---

## 🎯 Objetivos de la sesión

Al finalizar esta sesión serás capaz de:

- 🧠 Comprender qué es el Machine Learning y sus tipos principales (regresión y clasificación).
- 🔄 Describir el ciclo de vida de un modelo de ML desde la definición del problema hasta su monitoreo.
- 🌿 Entrenar y comparar modelos de clasificación usando scikit-learn (Regresión Logística, Árbol de Decisión, Random Forest).
- 📏 Evaluar modelos con métricas apropiadas e identificar sobreajuste y subajuste.

---

## 🤔 ¿Qué es el Aprendizaje Automático?

El **Machine Learning (ML)** es una rama de la Inteligencia Artificial que permite a las computadoras **aprender patrones a partir de datos** y tomar decisiones sin necesidad de programar reglas explícitas.

> 💡 **Analogía:** Imagina que quieres enseñarle a un niño a distinguir perros de gatos. No le das una lista de reglas; simplemente le muestras muchas fotos. Con el tiempo, aprende solo. ¡Eso es Machine Learning!

Existen dos grandes tipos de tareas en ML supervisado:

### 📈 Regresión

Predice un **valor numérico continuo**.

- *Ejemplo:* ¿Cuál será el precio de una casa dado su tamaño y ubicación?
- La salida es un número: `$250,000`, `$3,200`, etc.

### 🏷️ Clasificación

Predice una **categoría o etiqueta**.

- *Ejemplo:* ¿Es este tumor maligno o benigno?
- La salida es una clase: `maligno` / `benigno`, `spam` / `no spam`.

---

## 🔄 Ciclo de Vida de un Modelo de Machine Learning

Todo proyecto de ML sigue un flujo estructurado. Conocerlo te ayudará a no perderte en el proceso:

```
📋 Definición del problema
        ↓
📦 Recolección de datos
        ↓
🧹 Preparación de datos
        ↓
🏋️ Entrenamiento del modelo
        ↓
📊 Evaluación y mejora del modelo
        ↓
🚀 Despliegue del modelo
        ↓
👁️ Monitoreo del modelo
```

| Etapa | Descripción |
|---|---|
| 📋 **Definición del problema** | ¿Qué queremos predecir? ¿Clasificación o regresión? |
| 📦 **Recolección de datos** | Obtener datos relevantes y suficientes para el problema |
| 🧹 **Preparación de datos** | Limpieza, transformación y división en train/test |
| 🏋️ **Entrenamiento** | El algoritmo aprende los patrones en los datos de entrenamiento |
| 📊 **Evaluación y mejora** | Medir el desempeño con métricas y ajustar hiperparámetros |
| 🚀 **Despliegue** | Poner el modelo en producción para que genere predicciones reales |
| 👁️ **Monitoreo** | Vigilar que el modelo siga funcionando bien con datos nuevos |

---

## 🏷️ Clasificación con scikit-learn

### ¿Qué es una tarea de clasificación?

En clasificación, el modelo aprende a **asignar una etiqueta** a cada observación. La salida siempre es una **categoría discreta**.

> 🎯 **Tarea de hoy:** Predecir si un tumor es **maligno (1)** o **benigno (0)** usando el dataset *Breast Cancer* de scikit-learn.

---

### 📦 Cargar y explorar los datos

```python
from sklearn.datasets import load_breast_cancer
import pandas as pd

# Cargar el dataset
data = load_breast_cancer()
df = pd.DataFrame(data.data, columns=data.feature_names)
df['target'] = data.target

print(f"Filas: {df.shape[0]} | Columnas: {df.shape[1]}")
df.head()
```

```python
# Distribución de clases
df['target'].value_counts()
```

```python
# Estadísticas descriptivas básicas
df.describe()
```

---

### 🧹 Preparar y dividir los datos

```python
from sklearn.model_selection import train_test_split

X = df.drop('target', axis=1)
y = df['target']

# División 80% entrenamiento / 20% prueba
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

print(f"Entrenamiento: {X_train.shape[0]} muestras")
print(f"Prueba:        {X_test.shape[0]} muestras")
```

> 💡 **¿Por qué dividir?** Queremos que el modelo aprenda con un conjunto de datos y sea evaluado con datos **que nunca ha visto**, para medir su capacidad de generalizar.

---

### 🏋️ Entrenamiento: Regresión Logística

La **Regresión Logística** usa una función matemática (la sigmoide) para transformar una combinación lineal de variables en una probabilidad entre 0 y 1.

$$P(y=1) = \frac{1}{1 + e^{-(\beta_0 + \beta_1 x_1 + \cdots + \beta_n x_n)}}$$

> 🧠 **Intuición:** El modelo busca la "línea" que mejor separa las dos clases en el espacio de características.

```python
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score

# Crear y entrenar el modelo
lr = LogisticRegression(max_iter=10000, random_state=42)
lr.fit(X_train, y_train)

# Evaluar
y_pred_lr = lr.predict(X_test)
acc_lr = accuracy_score(y_test, y_pred_lr)
print(f"✅ Exactitud - Regresión Logística: {acc_lr:.4f}")
```

---

### 🌳 Entrenamiento: Árbol de Decisión

Un **Árbol de Decisión** divide los datos en ramas basándose en preguntas sobre las características, como un diagrama de flujo.

> 🌿 **Intuición:** Es como un juego de 20 preguntas. El árbol aprende cuáles preguntas hacen la mejor separación entre clases, eligiendo en cada nodo la característica más informativa.

```python
from sklearn.tree import DecisionTreeClassifier

# Crear y entrenar el modelo
dt = DecisionTreeClassifier(random_state=42)
dt.fit(X_train, y_train)

# Evaluar
y_pred_dt = dt.predict(X_test)
acc_dt = accuracy_score(y_test, y_pred_dt)
print(f"✅ Exactitud - Árbol de Decisión: {acc_dt:.4f}")
```

---

### 🌲 Entrenamiento: Random Forest

Un **Random Forest** es un conjunto (*ensemble*) de muchos árboles de decisión. Cada árbol se entrena con una muestra aleatoria de los datos y características; la predicción final es la **votación mayoritaria** de todos los árboles.

> 🌲🌲🌲 **Intuición:** Si un árbol puede equivocarse, ¡muchos árboles juntos son más difíciles de engañar! La diversidad reduce el error.

#### ⚙️ Hiperparámetros importantes

| Hiperparámetro | Descripción | Efecto |
|---|---|---|
| `n_estimators` | Número de árboles | Más árboles → más estable, pero más lento |
| `max_depth` | Profundidad máxima de cada árbol | Profundidad alta → riesgo de sobreajuste |
| `min_samples_split` | Mínimo de muestras para dividir un nodo | Valor alto → árboles más simples |

```python
from sklearn.ensemble import RandomForestClassifier

# Modelo base
rf = RandomForestClassifier(n_estimators=100, random_state=42)
rf.fit(X_train, y_train)

# Evaluar
y_pred_rf = rf.predict(X_test)
acc_rf = accuracy_score(y_test, y_pred_rf)
print(f"✅ Exactitud - Random Forest: {acc_rf:.4f}")
```

```python
# Experimenta con los hiperparámetros
rf_deep = RandomForestClassifier(n_estimators=100, max_depth=2, random_state=42)
rf_deep.fit(X_train, y_train)
acc_rf_deep = accuracy_score(y_test, rf_deep.predict(X_test))

rf_full = RandomForestClassifier(n_estimators=200, max_depth=None, random_state=42)
rf_full.fit(X_train, y_train)
acc_rf_full = accuracy_score(y_test, rf_full.predict(X_test))

print(f"RF max_depth=2:    {acc_rf_deep:.4f}")
print(f"RF max_depth=None: {acc_rf_full:.4f}")
```

---

### ⚖️ Sobreajuste y Subajuste

Uno de los conceptos más importantes en ML. 

| | Subajuste (Underfitting) | Buen ajuste | Sobreajuste (Overfitting) |
|---|---|---|---|
| **Descripción** | El modelo es demasiado simple | El modelo generaliza bien | El modelo memoriza los datos de entrenamiento |
| **Error entrenamiento** | Alto | Bajo | Muy bajo |
| **Error prueba** | Alto | Bajo | Alto |
| **Analogía** | Estudiar solo los títulos del libro 📖 | Entender el tema a fondo 🧠 | Memorizar el libro de memoria 🤯 |

```python
# Detectar sobreajuste comparando accuracy en train vs test
rf_overfit = RandomForestClassifier(n_estimators=100, max_depth=None, random_state=42)
rf_overfit.fit(X_train, y_train)

train_acc = accuracy_score(y_train, rf_overfit.predict(X_train))
test_acc  = accuracy_score(y_test,  rf_overfit.predict(X_test))

print(f"Exactitud en entrenamiento: {train_acc:.4f}")
print(f"Exactitud en prueba:        {test_acc:.4f}")

if train_acc - test_acc > 0.05:
    print("⚠️ Posible sobreajuste detectado.")
else:
    print("✅ El modelo generaliza bien.")
```

---

### 📊 Comparación de modelos de clasificación

```python
import pandas as pd

resultados_clf = pd.DataFrame({
    'Modelo': ['Regresión Logística', 'Árbol de Decisión', 'Random Forest'],
    'Exactitud (Accuracy)': [acc_lr, acc_dt, acc_rf]
})

resultados_clf = resultados_clf.sort_values('Exactitud (Accuracy)', ascending=False)
print(resultados_clf.to_string(index=False))
```

> 🏆 El modelo con mayor exactitud es el mejor en clasificar tumores correctamente. Pero recuerda: la exactitud no siempre es la única métrica que importa, especialmente con clases desbalanceadas.

---

## 📈 Regresión con scikit-learn

### ¿Qué es una tarea de regresión?

En regresión, el modelo aprende a **predecir un valor numérico continuo**. La salida puede ser cualquier número real.

> 🎯 **Tarea:** Predecir el **precio de viviendas** en California usando el dataset *California Housing* de scikit-learn.

---

### 📦 Cargar y explorar los datos

```python
from sklearn.datasets import fetch_california_housing
import pandas as pd

# Cargar el dataset
data = fetch_california_housing()
df_reg = pd.DataFrame(data.data, columns=data.feature_names)
df_reg['target'] = data.target  # Precio mediano de casas (en $100,000)

print(f"Filas: {df_reg.shape[0]} | Columnas: {df_reg.shape[1]}")
df_reg.head()
```

```python
# Distribución del precio
df_reg['target'].describe()
```

---

### 🧹 Preparar y dividir los datos

```python
from sklearn.model_selection import train_test_split

X_reg = df_reg.drop('target', axis=1)
y_reg = df_reg['target']

X_train_r, X_test_r, y_train_r, y_test_r = train_test_split(
    X_reg, y_reg, test_size=0.2, random_state=42
)

print(f"Entrenamiento: {X_train_r.shape[0]} muestras")
print(f"Prueba:        {X_test_r.shape[0]} muestras")
```

---

### 🏋️ Entrenamiento: Regresión Lineal

La **Regresión Lineal** modela la relación entre las variables de entrada y la salida como una línea recta (o hiperplano en múltiples dimensiones).

$$\hat{y} = \beta_0 + \beta_1 x_1 + \beta_2 x_2 + \cdots + \beta_n x_n$$

> 🧠 **Intuición:** El modelo busca la línea que minimiza la suma de los errores al cuadrado entre las predicciones y los valores reales.

```python
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
import numpy as np

lr_reg = LinearRegression()
lr_reg.fit(X_train_r, y_train_r)

y_pred_lr_r = lr_reg.predict(X_test_r)
mse_lr = mean_squared_error(y_test_r, y_pred_lr_r)
print(f"📏 MSE - Regresión Lineal: {mse_lr:.4f}")
```

---

### 🌳 Entrenamiento: Árbol de Decisión (Regresión)

El árbol de decisión también se puede usar para regresión. En cada nodo hoja, predice el **promedio** de los valores del grupo.

```python
from sklearn.tree import DecisionTreeRegressor

dt_reg = DecisionTreeRegressor(random_state=42)
dt_reg.fit(X_train_r, y_train_r)

y_pred_dt_r = dt_reg.predict(X_test_r)
mse_dt = mean_squared_error(y_test_r, y_pred_dt_r)
print(f"📏 MSE - Árbol de Decisión: {mse_dt:.4f}")
```

---

### 🌲 Entrenamiento: Random Forest (Regresión)

```python
from sklearn.ensemble import RandomForestRegressor

rf_reg = RandomForestRegressor(n_estimators=100, random_state=42)
rf_reg.fit(X_train_r, y_train_r)

y_pred_rf_r = rf_reg.predict(X_test_r)
mse_rf = mean_squared_error(y_test_r, y_pred_rf_r)
print(f"📏 MSE - Random Forest: {mse_rf:.4f}")
```

---

### 📏 Métrica de evaluación: MSE

El **Error Cuadrático Medio (MSE)** mide qué tan lejos están las predicciones de los valores reales, en promedio.

$$MSE = \frac{1}{n} \sum_{i=1}^{n} (y_i - \hat{y}_i)^2$$

> 📉 **¡Menor MSE es mejor!** Un MSE de 0 significaría predicciones perfectas (algo que casi nunca ocurre en la realidad).

También puedes usar la raíz del MSE (RMSE) para interpretar el error en las mismas unidades que la variable objetivo:

$$RMSE = \sqrt{MSE}$$

```python
print(f"📏 RMSE - Regresión Lineal:  {np.sqrt(mse_lr):.4f}")
print(f"📏 RMSE - Árbol de Decisión: {np.sqrt(mse_dt):.4f}")
print(f"📏 RMSE - Random Forest:     {np.sqrt(mse_rf):.4f}")
```

---

### 📊 Comparación de modelos de regresión

```python
resultados_reg = pd.DataFrame({
    'Modelo': ['Regresión Lineal', 'Árbol de Decisión', 'Random Forest'],
    'MSE': [mse_lr, mse_dt, mse_rf],
    'RMSE': [np.sqrt(mse_lr), np.sqrt(mse_dt), np.sqrt(mse_rf)]
})

resultados_reg = resultados_reg.sort_values('MSE')
print(resultados_reg.to_string(index=False))
```

> 🏆 El modelo con **menor MSE/RMSE** es el mejor en predicción de precios. Observa cómo el Random Forest generalmente supera a los modelos más simples gracias a su naturaleza de ensemble.

---

## 🎓 Conclusiones

| Concepto | Resumen |
|---|---|
| 🤖 **Machine Learning** | Sistemas que aprenden patrones de los datos sin programación explícita |
| 🏷️ **Clasificación** | Predice categorías (maligno/benigno, spam/no spam) |
| 📈 **Regresión** | Predice valores numéricos continuos (precio, temperatura) |
| 🌲 **Random Forest** | Ensemble de árboles; robusto y preciso, con hiperparámetros clave |
| ⚖️ **Sobreajuste** | El modelo memoriza el training set pero falla en datos nuevos |
| 📏 **Métricas** | Accuracy para clasificación; MSE/RMSE para regresión |

> 🚀 **Próximos pasos:** Explora otras métricas como `F1-score`, `AUC-ROC` para clasificación y `R²` para regresión. También puedes investigar técnicas de búsqueda de hiperparámetros como `GridSearchCV`.

---

*Webinar preparado para TripleTen Bootcamp — Data Science & Analytics* 🎓
