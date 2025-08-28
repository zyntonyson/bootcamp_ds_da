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
        # top-k (no ordenados); luego ordenamos esos k si queremos estabilidad
        neigh_idx_part = np.argpartition(D, kth=k-1, axis=1)[:, :k]

        # Votación mayoritaria
        y_pred = np.empty(X.shape[0], dtype=self._y.dtype)
        for i in range(X.shape[0]):
            idx_k = neigh_idx_part[i]
            # ordenar esos k por distancia real para desempates consistentes
            local_order = np.argsort(D[i, idx_k], kind="stable")
            idx_k = idx_k[local_order]
            neigh_labels = self._y[idx_k]

            # mapear a 0..C-1 para usar bincount de forma robusta
            # (self.classes_ está ordenado)
            inv_map = {c: j for j, c in enumerate(self.classes_)}
            neigh_idx_labels = np.fromiter((inv_map[c] for c in neigh_labels), dtype=int, count=len(neigh_labels))

            counts = np.bincount(neigh_idx_labels, minlength=self.classes_.size)
            # argmax estable -> clase con mayor conteo; si hay empate, la de menor índice (determinista)
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
        - Usar: np.abs(A[:, None, :] - B[None, :, :]).sum(axis=2)
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
