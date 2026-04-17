
quizz:
    question:
        body:
            ¿Qué hace el siguiente codigo?

            ```python
            import pandas as pd
    import numpy as np
    # Calcular métricas por grupo
    metrics = df.groupby('group')['conversion'].agg(['count', 'mean']).reset_index()
    print(metrics)
            ```
        items:
            option:
                "Agrupa los datos por la columna 'group' y calcula el conteo y la media de la columna 'conversion'."
            option:
                "Crea un nuevo DataFrame con las métricas calculadas."
            option:
                "Imprime el DataFrame con las métricas."
            option:
                "Agrupa los datos por la columna 'group' y calcula el conteo y la media de la columna 'conversion'."
        feedback: 
            "Crea un nuevo DataFrame con las métricas calculadas."
    question:
        body:
            ¿Qué hace el siguiente codigo 2?

            ```python
            import pandas as pd
    import numpy as np
    # Calcular métricas por grupo
    metrics = df.groupby('group')['conversion'].agg(['count', 'mean']).reset_index()
    print(metrics)
            ```
        items:
            option:
                "Agrupa los datos por la columna 'group' y calcula el conteo y la media de la columna 'conversion'."
            option:
                "Crea un nuevo DataFrame con las métricas calculadas."
            option:
                "Imprime el DataFrame con las métricas."
            option:
                "Agrupa los datos por la columna 'group' y calcula el conteo y la media de la columna 'conversion'."
        feedback: 
            "Crea un nuevo DataFrame con las métricas calculadas."
