1. Hacer una copia del GSheet
1. Ajustar GS para usar punto decimal y formato de YYYYMMDD
    -Para fechas pasar primero a MX y convertir
    - Luego a formato US y convertir
1. Hacer recorrido de los datos pestaña a pestaña
1. Dar un formato adecuado a change_log
1. Revisar el diccionario de datos
1. Crear una copia de raw_songs nombrado a clear_songs
1. Enumerar en el chat columna por columna que cambios consideran necesarios para cada
1. Aplicar a cambios columna
    1. **Song* convertir UPPER LOWER PROPER + TRIM
    1. *Album* convertir UPPER LOWER PROPER + TRIM
    1. *Release Date* convertir YYYY-MM-DD 
        1. **Replace** para símbolos /, mostrar uso de replace y regexpreplace
        1. Ajustar las fechas usando los cambios entre US/MX
    1. *Duration* 
        1. Convertir a número
        1. Hacer split para lo que no tienen  número y hacer la operacion
            >> =IF(N2,D2, INDEX(SPLIT(D2,":"),1,1)*60 + INDEX(SPLIT(D2,":"),1,2))
    1. **Streams**
        1. Convertir a numero cambiando de región
    1. **Explicit**
        1. Formula 
            `=IF(ISNUMBER(MATCH(UPPER(TRIM(A2)), {"1","Y","YES","TRUE"}, 0)), TRUE,IF(ISNUMBER(MATCH(UPPER(TRIM(A2)), {"0","N","NO","FALSE"}, 0)), FALSE,NA()))`
    1. **Writer**
        1. `REGEXP_CONTAINS`
    
    1. Revisión de nulos y ausentes



     

