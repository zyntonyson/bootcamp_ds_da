# Solución Propuesta: Proyecto de Recuperación de Oro
**Sprint 13 - Proyecto Integrado | TripleTen Data Science**

---

## Objetivo del Proyecto

Desarrollar un modelo de Machine Learning capaz de **predecir el coeficiente de recuperación de oro** en dos etapas del proceso de purificación:

1. **`rougher.output.recovery`** — Recuperación del concentrado rougher (flotación)
2. **`final.output.recovery`** — Recuperación del concentrado final

La métrica de evaluación final utiliza **sMAPE** (Error Medio Absoluto Porcentual Simétrico), combinando ambos objetivos:

```
sMAPE_final = 0.25 * sMAPE(rougher) + 0.75 * sMAPE(final)
```

---

## Entendimiento del Proceso Tecnológico

El mineral extraído pasa por las siguientes etapas:

1. **Flotación (Rougher process):** Se introduce la alimentación rougher en las plantas de flotación → se obtiene concentrado rougher + colas rougher.
2. **Purificación primaria (Primary cleaner):** El concentrado rougher se somete a purificación.
3. **Purificación secundaria (Secondary cleaner):** Segunda etapa de purificación → produce concentrado final + nuevas colas.

### Denominación de características

```
[stage].[parameter_type].[parameter_name]
```

| Prefijo `[stage]`     | Significado              |
|-----------------------|--------------------------|
| `rougher`             | Flotación                |
| `primary_cleaner`     | Purificación primaria    |
| `secondary_cleaner`   | Purificación secundaria  |
| `final`               | Producto final           |

| Prefijo `[parameter_type]` | Significado                        |
|----------------------------|------------------------------------|
| `input`                    | Parámetros de la materia prima     |
| `output`                   | Parámetros del producto            |
| `state`                    | Estado actual de la etapa          |
| `calculation`              | Características calculadas         |

---

## Datos Disponibles

| Archivo                     | Descripción                                   |
|-----------------------------|-----------------------------------------------|
| `gold_recovery_train.csv`   | Dataset de entrenamiento (con targets)        |
| `gold_recovery_test.csv`    | Dataset de prueba (sin targets)               |
| `gold_recovery_full.csv`    | Dataset completo (entrenamiento + prueba)     |

> **Nota:** Algunos parámetros no están disponibles en el conjunto de prueba porque fueron medidos o calculados mucho más tarde. El conjunto de prueba **no contiene los targets**.

---

## Plan de Solución

---

## Paso 1: Preparación de los Datos

### 1.1 Carga y exploración inicial

```python
import pandas as pd
import numpy as np
from sklearn.metrics import mean_absolute_error

# URLs de los archivos
url_train = "https://practicum-content.s3.us-west-1.amazonaws.com/datasets/gold_recovery_train.csv?etag=68f7294d2022296464fd4d705519843c"
url_test  = "https://practicum-content.s3.us-west-1.amazonaws.com/datasets/gold_recovery_test.csv?etag=1e251eb453e155475fca8d03d8b66ae2"
url_full  = "https://practicum-content.s3.us-west-1.amazonaws.com/datasets/gold_recovery_full.csv?etag=b2fba00139bca2b8c4c9af43667e0656"

# Cargar datasets con el índice de fecha
df_train = pd.read_csv(url_train, parse_dates=['date']).sort_values('date').set_index('date')
df_test  = pd.read_csv(url_test,  parse_dates=['date']).sort_values('date').set_index('date')
df_full  = pd.read_csv(url_full,  parse_dates=['date']).sort_values('date').set_index('date')

print("Forma train:", df_train.shape)
print("Forma test:", df_test.shape)
print("Forma full:", df_full.shape)

# Exploración básica
df_train.head()
df_train.info()
df_train.describe()
```

---

### 1.2 Verificar el cálculo de recuperación rougher

La fórmula de recuperación es:

```
recovery = C * (F - T) / (F * (C - T)) * 100
```

Donde:
- **C** = proporción de oro en el concentrado (`rougher.output.concentrate_au`)
- **F** = proporción de oro en la alimentación (`rougher.input.feed_au`)
- **T** = proporción de oro en las colas (`rougher.output.tail_au`)

```python
# Variables de la fórmula
C = df_train['rougher.output.concentrate_au']
F = df_train['rougher.input.feed_au']
T = df_train['rougher.output.tail_au']

# Denominador
denominator = F * (C - T)

# Serie vacía para el cálculo
calculated_recovery = pd.Series(index=df_train.index, dtype='float64')

# Filas con denominador válido
valid = denominator.notna() & (denominator != 0)

# Calcular recuperación solo en filas válidas
calculated_recovery.loc[valid] = (
    C.loc[valid] * (F.loc[valid] - T.loc[valid])
    / denominator.loc[valid]
) * 100

# Comparar con el valor registrado
comparison = pd.DataFrame({
    'actual': df_train['rougher.output.recovery'],
    'calculated': calculated_recovery
}).replace([np.inf, -np.inf], np.nan).dropna()

mae = mean_absolute_error(comparison['actual'], comparison['calculated'])
print(f"Filas evaluadas: {len(comparison)}")
print(f"EAM (MAE): {mae}")
```

**Resultado obtenido:** EAM ≈ 9.3e-15 (prácticamente cero).
Esto confirma que `rougher.output.recovery` fue calculado correctamente.

---

### 1.3 Análisis de características ausentes en el conjunto de prueba

```python
# Columnas en train pero NO en test
cols_only_in_train = set(df_train.columns) - set(df_test.columns)
print(f"Columnas en train pero NO en test: {len(cols_only_in_train)}")

for col in sorted(cols_only_in_train):
    parts = col.split('.')
    param_type = parts[1] if len(parts) > 1 else 'unknown'
    print(f"  [{param_type}] {col}")
```

**Resultado:** Las columnas ausentes en el test son de tipo `output` y `calculation` —
calculadas o medidas a posteriori en el proceso real. Esto es esperado por diseño del problema
y no afecta al modelo si se usan solo las features disponibles en test.

---

### 1.4 Preprocesamiento de datos

```python
from sklearn.impute import SimpleImputer

# Identificar columnas de features disponibles en ambos conjuntos
target_cols = ['rougher.output.recovery', 'final.output.recovery']
feature_cols = [c for c in df_train.columns
                if c in df_test.columns and c not in target_cols]

# Imputar valores faltantes con la mediana (robusta a outliers)
imputer = SimpleImputer(strategy='median')

X_train_full = pd.DataFrame(
    imputer.fit_transform(df_train[feature_cols]),
    columns=feature_cols,
    index=df_train.index
)
X_test = pd.DataFrame(
    imputer.transform(df_test[feature_cols]),
    columns=feature_cols,
    index=df_test.index
)

# Targets de entrenamiento
y_rougher = df_train['rougher.output.recovery']
y_final   = df_train['final.output.recovery']

# Conservar solo filas donde ambos targets están disponibles
valid_idx = y_rougher.notna() & y_final.notna()
X_train   = X_train_full.loc[valid_idx]
y_rougher = y_rougher.loc[valid_idx]
y_final   = y_final.loc[valid_idx]

print(f"Filas de entrenamiento válidas: {len(X_train)}")
print(f"Features disponibles: {len(feature_cols)}")
```

---

## Paso 2: Análisis Exploratorio de Datos (EDA)

### 2.1 Concentración de metales por etapa de purificación

```python
import matplotlib.pyplot as plt

metals = ['au', 'ag', 'pb']
stages = {
    'Alimentación\n(Rougher input)': 'rougher.input.feed_{}',
    'Concentrado\nRougher':          'rougher.output.concentrate_{}',
    'Concentrado\nFinal':            'final.output.concentrate_{}'
}
metal_names = {'au': 'Oro (Au)', 'ag': 'Plata (Ag)', 'pb': 'Plomo (Pb)'}
colors = ['#FFD700', '#C0C0C0', '#B5651D']

fig, axes = plt.subplots(1, 3, figsize=(15, 5))

for ax, metal, color in zip(axes, metals, colors):
    means, labels = [], []
    for stage_label, col_template in stages.items():
        col = col_template.format(metal)
        if col in df_train.columns:
            means.append(df_train[col].mean())
            labels.append(stage_label)
    ax.bar(labels, means, color=color, edgecolor='black', alpha=0.85)
    ax.set_title(metal_names[metal], fontsize=13)
    ax.set_ylabel('Concentración media (%)')
    ax.set_ylim(0, max(means) * 1.3)

plt.suptitle('Concentración de metales por etapa de purificación', fontsize=15, fontweight='bold')
plt.tight_layout()
plt.show()
```

**Interpretación esperada:**
- La concentración de **oro** debe aumentar progresivamente de la alimentación al concentrado final (el proceso es eficiente).
- La **plata y el plomo** también pueden aumentar, pero en menor proporción.
- Si algún metal no muestra incremento, puede indicar ineficiencia en etapas específicas.

---

### 2.2 Distribución del tamaño de partículas: train vs test

```python
fig, ax = plt.subplots(figsize=(10, 5))
col = 'rougher.input.feed_size'
df_train[col].plot.hist(bins=60, alpha=0.6, label='Train', color='steelblue', ax=ax)
df_test[col].plot.hist(bins=60, alpha=0.6, label='Test', color='tomato', ax=ax)
ax.set_xlabel('Tamaño de partícula (feed_size)')
ax.set_ylabel('Frecuencia')
ax.set_title('Distribución del tamaño de partículas: Train vs Test')
ax.legend()
plt.tight_layout()
plt.show()
```

**Criterio:** Si las distribuciones de train y test son similares (visualmente), la evaluación del
modelo será representativa y válida.

---

### 2.3 Concentración total y eliminación de anomalías

```python
# Columnas de concentración de la alimentación
feed_cols = [c for c in df_train.columns
             if 'rougher.input.feed_' in c and c.endswith(('_au', '_ag', '_pb', '_sol'))]

total_feed = df_train[feed_cols].sum(axis=1)

# Visualizar distribución de concentración total
total_feed.hist(bins=50, color='teal', edgecolor='white', alpha=0.8)
plt.title('Distribución de concentración total en la alimentación')
plt.xlabel('Suma de concentraciones')
plt.ylabel('Frecuencia')
plt.show()

# Umbral: percentil 1 como indicador de anomalías
threshold = total_feed.quantile(0.01)
anomalous = total_feed < threshold
print(f"Umbral: {threshold:.4f}")
print(f"Filas anómalas detectadas (concentración total casi 0): {anomalous.sum()}")

# Eliminar anomalías y realinear datasets
X_train   = X_train[~anomalous.loc[X_train.index]]
y_rougher = y_rougher[~anomalous.loc[y_rougher.index]]
y_final   = y_final[~anomalous.loc[y_final.index]]

print(f"Filas de entrenamiento después de limpiar: {len(X_train)}")
```

---

## Paso 3: Construcción del Modelo

### 3.1 Función sMAPE

```python
def smape(y_true, y_pred):
    """
    Error Medio Absoluto Porcentual Simétrico (sMAPE).

    sMAPE = (1/N) * sum( |yi - yi_hat| / ((|yi| + |yi_hat|) / 2) ) * 100
    """
    y_true = np.array(y_true)
    y_pred = np.array(y_pred)

    denominator = (np.abs(y_true) + np.abs(y_pred)) / 2
    mask = denominator != 0

    result = np.zeros(len(y_true))
    result[mask] = np.abs(y_true[mask] - y_pred[mask]) / denominator[mask] * 100

    return result.mean()


def final_smape(y_true_rougher, y_pred_rougher, y_true_final, y_pred_final):
    """
    Métrica final: combinación ponderada de sMAPE rougher y final.

    sMAPE_final = 0.25 * sMAPE(rougher) + 0.75 * sMAPE(final)
    """
    smape_rougher = smape(y_true_rougher, y_pred_rougher)
    smape_fin     = smape(y_true_final, y_pred_final)
    return 0.25 * smape_rougher + 0.75 * smape_fin


# Verificación: sMAPE perfecto debe ser 0
y_t = np.array([10, 20, 30])
y_p = np.array([10, 20, 30])
print("sMAPE perfecto (debe ser 0):", smape(y_t, y_p))
```

---

### 3.2 Entrenamiento y validación cruzada de modelos

```python
from sklearn.model_selection import cross_val_score, KFold
from sklearn.linear_model import LinearRegression, Ridge
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.tree import DecisionTreeRegressor
from sklearn.metrics import make_scorer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
import warnings
warnings.filterwarnings('ignore')


def smape_scorer_fn(y_true, y_pred):
    # Retorna valor negativo para que sklearn (que maximiza) minimice el sMAPE
    return -smape(y_true, y_pred)


# greater_is_better=True (default): make_scorer NO niega el resultado,
# así cross_val_score devuelve valores negativos y -cv.mean() da el sMAPE positivo.
smape_score = make_scorer(smape_scorer_fn)
kf = KFold(n_splits=5, shuffle=False)  # Sin shuffle para respetar el orden temporal

# Modelos candidatos
models = {
    'Regresión Lineal': Pipeline([
        ('scaler', StandardScaler()),
        ('model', LinearRegression())
    ]),
    'Ridge': Pipeline([
        ('scaler', StandardScaler()),
        ('model', Ridge(alpha=1.0))
    ]),
    'Árbol Decisión': DecisionTreeRegressor(max_depth=6, random_state=42),
    'Random Forest':  RandomForestRegressor(
        n_estimators=100, max_depth=8, random_state=42, n_jobs=-1
    ),
    'Gradient Boosting': GradientBoostingRegressor(
        n_estimators=100, max_depth=4, learning_rate=0.05, random_state=42
    ),
}

results = {}
header = f"{'Modelo':<22} | {'sMAPE Rougher':>14} | {'sMAPE Final':>12} | {'sMAPE Total':>12}"
print(header)
print("-" * len(header))

for name, model in models.items():
    cv_r = cross_val_score(model, X_train, y_rougher, cv=kf, scoring=smape_score)
    cv_f = cross_val_score(model, X_train, y_final,   cv=kf, scoring=smape_score)
    sr = -cv_r.mean()
    sf = -cv_f.mean()
    st = 0.25 * sr + 0.75 * sf
    results[name] = {'smape_rougher': sr, 'smape_final': sf, 'smape_total': st}
    print(f"{name:<22} | {sr:>13.4f}% | {sf:>11.4f}% | {st:>11.4f}%")

# Modelo baseline: predecir siempre la media
baseline_r = smape(y_rougher, np.full(len(y_rougher), y_rougher.mean()))
baseline_f = smape(y_final,   np.full(len(y_final),   y_final.mean()))
baseline_t = 0.25 * baseline_r + 0.75 * baseline_f
print(f"{'BASELINE (media)':<22} | {baseline_r:>13.4f}% | {baseline_f:>11.4f}% | {baseline_t:>11.4f}%")
```

---

### 3.3 Evaluación final en el conjunto de prueba

```python
# Seleccionar el mejor modelo según sMAPE total de validación cruzada
best_name = min(results, key=lambda k: results[k]['smape_total'])
print(f"Mejor modelo seleccionado: {best_name}")
print(f"  sMAPE Rougher: {results[best_name]['smape_rougher']:.4f}%")
print(f"  sMAPE Final:   {results[best_name]['smape_final']:.4f}%")
print(f"  sMAPE Total:   {results[best_name]['smape_total']:.4f}%")

best_model = models[best_name]

# Entrenar y predecir para target rougher
best_model.fit(X_train, y_rougher)
pred_rougher = best_model.predict(X_test)

# Entrenar y predecir para target final
best_model.fit(X_train, y_final)
pred_final = best_model.predict(X_test)

# Guardar predicciones
predictions_df = pd.DataFrame({
    'rougher.output.recovery': pred_rougher,
    'final.output.recovery':   pred_final
}, index=df_test.index)

predictions_df.to_csv('predictions.csv')
print("\nPredicciones guardadas en predictions.csv")
print(f"  rougher.output.recovery — min: {pred_rougher.min():.2f}, max: {pred_rougher.max():.2f}, media: {pred_rougher.mean():.2f}")
print(f"  final.output.recovery   — min: {pred_final.min():.2f}, max: {pred_final.max():.2f}, media: {pred_final.mean():.2f}")
```

---

## Resumen de Resultados Esperados

### Tabla comparativa de modelos

| Modelo               | sMAPE Rougher | sMAPE Final | sMAPE Total |
|----------------------|:-------------:|:-----------:|:-----------:|
| Baseline (media)     | ~10–15%       | ~8–12%      | ~9–13%      |
| Regresión Lineal     | ~8–12%        | ~6–10%      | ~7–11%      |
| Ridge                | ~8–12%        | ~6–10%      | ~7–11%      |
| Árbol de Decisión    | ~7–10%        | ~5–9%       | ~6–9%       |
| **Random Forest**    | **~5–8%**     | **~4–7%**   | **~5–7%**   |
| Gradient Boosting    | ~5–8%         | ~4–7%       | ~5–7%       |

> **Modelo recomendado:** Random Forest o Gradient Boosting, gracias a su capacidad de capturar
> relaciones no lineales entre los parámetros del proceso.

---

## Conclusiones

1. **Verificación de datos:** El EAM ≈ 9.3e-15 confirma que `rougher.output.recovery`
   fue calculado correctamente.

2. **Características faltantes en test:** Corresponden a columnas de tipo `output` y `calculation`
   calculadas a posteriori. Esto es esperado por el diseño del problema y no afecta
   al modelo siempre que se usen solo las features disponibles en test.

3. **Distribuciones train/test:** Se verifica visualmente que las distribuciones del tamaño
   de partículas sean similares en ambos conjuntos, garantizando una evaluación representativa.

4. **Anomalías:** Se detectan y eliminan observaciones con concentración total ≈ 0
   (mediciones inválidas o erróneas del proceso).

5. **Métrica sMAPE:** La fórmula ponderada da mayor peso (75%) al sMAPE del concentrado final,
   enfatizando la importancia de predecir correctamente la recuperación al final del proceso.

6. **Mejor modelo:** Se selecciona mediante validación cruzada temporal (KFold sin shuffle),
   respetando el orden cronológico de los datos del proceso industrial.

---

## Estructura del Notebook

```
notebook.ipynb
├── 0. Importaciones y carga de datos
├── 1. Preparación de datos
│   ├── 1.1 Exploración inicial (shape, info, describe)
│   ├── 1.2 Verificación del cálculo de recuperación rougher (EAM ≈ 0)
│   ├── 1.3 Análisis de características ausentes en test
│   └── 1.4 Preprocesamiento (imputación con mediana, limpieza de anomalías)
├── 2. Análisis exploratorio (EDA)
│   ├── 2.1 Concentración de metales (Au, Ag, Pb) por etapa
│   ├── 2.2 Distribución de tamaño de partículas: train vs test
│   └── 2.3 Concentración total y eliminación de anomalías
├── 3. Construcción del modelo
│   ├── 3.1 Función sMAPE y métrica final ponderada
│   ├── 3.2 Validación cruzada de 5 modelos candidatos
│   ├── 3.3 Comparación con baseline (predicción de la media)
│   └── 3.4 Evaluación final y generación de predicciones en test
└── 4. Conclusiones
```

---

*Solución propuesta para el Sprint 13 - Proyecto Integrado 2 | TripleTen Data Science & Analytics Bootcamp*
