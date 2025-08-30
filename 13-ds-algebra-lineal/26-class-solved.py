import numpy as np
from sklearn.base import BaseEstimator, ClassifierMixin


class KNNClassifier(BaseEstimator, ClassifierMixin):

    """
    K-Nearest Neighbors.
    Parámetros
    ----------
    k : int
        Número de vecinos a considerar (k >= 1).
    metric : {"euclidean", "manhattan"}
        Métrica de distancia a utilizar.
    """

    def __init__(self, k=3, metric="euclidean"):
        # Validaciones básicas del init
        if not isinstance(k, int) or k < 1:
            raise ValueError("k debe ser un entero positivo (k >= 1).")
        metric = str(metric).lower()
        if metric not in {"euclidean", "manhattan"}:
            raise ValueError('metric debe ser "euclidean" o "manhattan".')
        self.k = k
        self.metric = metric
        # atributos que se setearán en fit
        self._X = None  # matriz de entrenamiento (n_samples, n_features)
        self._y = None  # etiquetas de entrenamiento (n_samples,)
        self.classes_ = None  # clases únicas en el orden interno
        self.inv_map = None # Etiquetas para el clasificador (0,1,2,...)

    def fit(self, X, y):
        """
        Guarda los datos de entrenamiento.
        - X: np.ndarray de forma (n_samples, n_features)
        - y: np.ndarray de forma (n_samples,)
        - Puede incluir validaciones de tipos/dimensiones.
        - Debe devolver self para cumplir el API de sklearn.
        """
        X, y = self._validate_inputs(X, y)
        if self.k > X.shape[0]:
            raise ValueError(f"k={self.k} no puede ser mayor que el número de muestras ({X.shape[0]}).")
        self._X = X
        self._y = y
        self.classes_ = np.unique(y)
        self.inv_map = {c: j for j, c in enumerate(self.classes_)}
        return self

    def predict(self, X):
        """
        Predice la clase para cada muestra en X.
        - Calcula distancias entre X y _X.
        - Identifica índices de los k vecinos más cercanos con np.argsort/argpartition.
        - Hace votación mayoritaria (resolver empates si ocurren).
        - Devuelve np.ndarray (n_samples_pred,) con etiquetas predichas.
        """
        self._check_is_fitted()
        X = self._validate_inputs(X, y=None)

        # Matriz de distancias (n_pred, n_train)
        D = self._pairwise_distances(X, self._X)

        # Índices de los k vecinos más cercanos por fila (argpartition para eficiencia)
        k = self.k

        # top-k (no ordenados)
        neigh_idx_part = np.argpartition(D, kth=k-1, axis=1)[:, :k]

        # Votación mayoritaria
        y_pred = np.empty(X.shape[0], dtype=self._y.dtype)
        for i in range(X.shape[0]):
            idx_k = neigh_idx_part[i]
            neigh_labels = self._y[idx_k]
            neigh_idx_labels = np.fromiter((self.inv_map[c] for c in neigh_labels), dtype=int, count=len(neigh_labels))
            counts = np.bincount(neigh_idx_labels, minlength=self.classes_.size)
            winner_local = int(np.argmax(counts))
            y_pred[i] = self.classes_[winner_local]
        return y_pred


    def _pairwise_distances(self, A, B):
        """
        Calcula distancias pairwise entre A (m, d) y B (n, d) según self.metric.
        Devuelve una matriz (m, n) con las distancias.
        """
        if self.metric == "euclidean":
            return self._euclidean(A, B)
        elif self.metric == "manhattan":
            return self._manhattan(A, B)
        else:
            # Esta rama no debería alcanzarse por la validación en __init__
            raise ValueError('metric debe ser "euclidean" o "manhattan".')

    def _euclidean(self, A, B):
        """
        Distancia Euclídea.
        Implementación vectorizada:
        - Para cada fila a en A y b en B, d(a,b) = ||a - b||_2
        - Usar broadcasting: np.linalg.norm(A[:, None, :] - B[None, :, :], axis=2)
        """
        diff = A[:, None, :] - B[None, :, :]
        return np.linalg.norm(diff, axis=2)

    def _manhattan(self, A, B):
        """
        Distancia Manhattan L1 pairwise.
        Implementación vectorizada:
        - d(a,b) = sum(|a_i - b_i|)
        """
        return np.abs(A[:, None, :] - B[None, :, :]).sum(axis=2)

    # ----------------------
    # Métodos auxiliares (opcionales)
    # ----------------------

    def _check_is_fitted(self):
        """
        Verifica que fit() haya sido llamado (conforme a sklearn.utils.validation).
        """
        if self._X is None or self._y is None or self.classes_ is None:
            raise ValueError("Este KNNClassifier no está ajustado aún. Llama primero a fit(X, y).")

    def _validate_inputs(self, X, y=None):
        """
        Normaliza tipos y valida dimensiones/NaNs.
        - Si y no es None: validar longitud y tipos (clasificación).
        """
        X = np.asarray(X, dtype=float)
        if X.ndim != 2:
            raise ValueError("X debe ser un arreglo 2D de forma (n_samples, n_features).")
        if y is None:
            return X
        y = np.asarray(y)
        if y.ndim != 1:
            raise ValueError("y debe ser un arreglo 1D de longitud n_samples.")
        if X.shape[0] != y.shape[0]:
            raise ValueError(f"Incompatibilidad de muestras: X tiene {X.shape[0]} filas y y tiene {y.shape[0]} elementos.")
        # (opcional) Chequeo de NaNs
        if np.isnan(X).any():
            raise ValueError("X contiene NaNs; limpia o imputa antes de usar KNN.")
        if np.isnan(y.astype(float, copy=False), where=False).any() if np.issubdtype(y.dtype, np.floating) else False:
            # Solo intentamos NaN-check si y es flotante; si es object/str, omitimos NaN check estricto
            raise ValueError("y contiene NaNs; limpia antes de usar KNN.")

        return X, y





import numpy as np
from sklearn.base import BaseEstimator, RegressorMixin

class LinearRegressionCustom(BaseEstimator, RegressorMixin):
    """
    Implementación básica de Regresión Lineal compatible con scikit-learn.
    Parámetros
    ----------
    fit_intercept : bool
        Si True, añade una columna de unos para el intercepto.
    """

    def __init__(self, fit_intercept=True):
        self.fit_intercept = fit_intercept
        self.coef_ = None      # vector de coeficientes (sin intercepto si aplica)
        self.intercept_ = None # valor escalar del intercepto si fit_intercept=True

    def fit(self, X, y):
        """
        Ajusta el modelo a los datos (X, y) resolviendo la ecuación normal:
        β = (X^T X)^(-1) X^T y
        - Si fit_intercept=True: añadir columna de unos a X.
        - Guardar coef_ y intercept_ según corresponda.
        - Devolver self.
        """
        # --- Validaciones y casting ---
        X = np.asarray(X, dtype=float)
        y = np.asarray(y, dtype=float)
        if X.ndim != 2:
            raise ValueError("X debe ser 2D (n_samples, n_features).")
        if y.ndim != 1:
            raise ValueError("y debe ser 1D (n_samples,).")
        if X.shape[0] != y.shape[0]:
            raise ValueError(f"Incompatibilidad: X tiene {X.shape[0]} filas y y tiene {y.shape[0]} elementos.")
        if np.isnan(X).any() or np.isnan(y).any():
            raise ValueError("X o y contienen NaNs. Limpia o imputa antes de ajustar.")

        # --- Construir X_aug con o sin intercepto ---
        X_aug = self._add_intercept(X) if self.fit_intercept else X

        # --- Resolver betas (pinv para robustez numérica) ---
        # beta_star incluye intercepto si fit_intercept=True
        beta_star = np.linalg.pinv(X_aug) @ y  # equivalente a (X_aug^T X_aug)^-1 X_aug^T y con mayor estabilidad

        if self.fit_intercept:
            self.intercept_ = float(beta_star[0])
            self.coef_ = beta_star[1:].copy()
        else:
            self.intercept_ = 0.0
            self.coef_ = beta_star.copy()

        return self

    def predict(self, X):
        """
        Predice valores para nuevas muestras.
        - Añadir columna de unos si fit_intercept=True.
        - Calcular y = X @ beta.
        - Devuelve vector (n_samples,).
        """
        self._check_is_fitted()
        X = np.asarray(X, dtype=float)
        if X.ndim != 2:
            raise ValueError("X debe ser 2D (n_samples, n_features).")
        if np.isnan(X).any():
            raise ValueError("X contiene NaNs. Limpia o imputa antes de predecir.")



        return X@self.coef_ + self.intercept_


    # ----------------------
    # Métodos auxiliares
    # ----------------------

    def _add_intercept(self, X):
        """
        Añade columna de unos a X si fit_intercept=True.
        """
        if not self.fit_intercept:
            return X
        n = X.shape[0]
        return np.c_[np.ones(n, dtype=float), X]

    def _check_is_fitted(self):
        """
        Verifica que fit() haya sido llamado (coef_ no None).
        """
        if self.coef_ is None or self.intercept_ is None:
            raise ValueError("Este LinearRegressionCustom no está ajustado. Llama primero a fit(X, y).")


from sklearn.base import BaseEstimator, TransformerMixin

class FeatureObfuscator(BaseEstimator, TransformerMixin):
    """
    Ofuscador lineal reversible: X' = X @ P
    - Si P es invertible, se recupera X = X' @ P^{-1}.
    
    Parámetros
    ----------
    P : np.ndarray | None
        Matriz de ofuscación (dxd) proporcionada por el usuario (debe ser invertible).
        Si None, se generará en fit() .
    seed : int | None
        Semilla para reproducibilidad cuando se genere P.
    """

    def __init__(self,  P=None,  seed=None):
        self.P = P
        self.seed = seed
        # Atributos aprendidos en fit()
        self.P_ = None       # Matriz de ofuscación final (validada/generada)
        self.P_inv_ = None   # Inversa para inverse_transform

    # ----------------------
    # API sklearn
    # ----------------------

    def fit(self, X, y=None):
        """
        Valida/infere n_features y define P_ y P_inv_.
        - Si P es proporcionada: validar forma (dxd), invertibilidad y asignar.
        - Si no: generar P_  y calcular P_inv_.
        - Debe devolver self.
        """
        X = self._validate_2d(X)
        d = X.shape[1]
        rng = np.random.default_rng(self.seed)

        if self.P is not None:
            P = np.asarray(self.P, dtype=float)
            if P.shape != (d, d):
                raise ValueError(f"P debe tener forma {(d, d)}; recibida {P.shape}.")
            # Revisa si la matriz es invertible 
            if np.linalg.matrix_rank(P) < d:  # puede usarse  igual al determinante np.linalg.det(A)
                raise ValueError("La matriz P proporcionada no es invertible.")
            self.P_ = P.copy()
        else:
            self.P_ = self._generate_P(d, rng)

        # calcular inversa  de P 
            self.P_inv_ = np.linalg.inv(self.P_)

        return self

    def transform(self, X):
        """
        Aplica la ofuscación: X' = X @ P_
        - Validar que fit() fue llamado (P_ no None).
        - Validar dimensionalidad: X.shape[1] == P_.shape[0]
        - Devolver X ofuscada.
        """
        self._check_is_fitted()
        X = self._validate_2d(X)
        if X.shape[1] != self.P_.shape[0]:
            raise ValueError(f"Incompatibilidad: X tiene {X.shape[1]} columnas y P tiene {self.P_.shape[0]}.")
        return X @ self.P_

    def inverse_transform(self, X_obf):
        """
        Revierte la ofuscación: X = X_obf @ P_inv_
        - Validar que fit() fue llamado y que P_inv_ existe.
        - Devolver datos originales.
        """
        self._check_is_fitted()
        X_obf = self._validate_2d(X_obf)
        if X_obf.shape[1] != self.P_inv_.shape[0]:
            raise ValueError(f"Incompatibilidad: X_obf tiene {X_obf.shape[1]} columnas y P_inv tiene {self.P_inv_.shape[0]}.")
        return X_obf @ self.P_inv_

    # ----------------------
    # Utilidades internas
    # ----------------------

    def _generate_P(self, d, rng):
        """
        Genera una matriz P (dxd) invertible det!=0 .
        """        
        while True:
            A = rng.integers(low=0, high=d**2,size=(d, d))
            if np.linalg.det(A) > 1:
                break
        return A


    def _check_is_fitted(self):
        """
        Verifica que fit() haya sido llamado (P_ y P_inv_ no None).
        """
        if self.P_ is None or self.P_inv_ is None:
            raise ValueError("Este FeatureObfuscator no está ajustado. Llama primero a fit(X).")

    def _validate_2d(self, X):
        """
        Convierte a np.array float y valida que sea 2D (n_samples, n_features).
        """
        X = np.asarray(X, dtype=float)
        if X.ndim != 2:
            raise ValueError("Se espera una matriz 2D (n_samples, n_features).")
        if np.isnan(X).any():
            raise ValueError("X contiene NaNs; limpia o imputa antes de transformar.")
        return X