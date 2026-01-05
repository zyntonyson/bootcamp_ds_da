import os

def limpiar_ruta(ruta):
    return ruta.replace(os.sep, "/")

def construir_arbol_notebooks(ruta_base):
    arbol = {}

    for carpeta_actual, _, archivos in os.walk(ruta_base):
        if ".venv" in carpeta_actual:
            continue
        notebooks = [f for f in archivos if f.endswith(".ipynb")]
        if notebooks:
            ruta_relativa = os.path.relpath(carpeta_actual, ruta_base)
            partes = ruta_relativa.split(os.sep) if ruta_relativa != "." else []
            nodo = arbol
            for parte in partes:
                nodo = nodo.setdefault(parte, {})
            for notebook in notebooks:
                ruta_notebook = os.path.join(carpeta_actual, notebook)
                ruta_relativa = os.path.relpath(ruta_notebook, ruta_base)
                nodo[notebook] = limpiar_ruta(ruta_relativa)  # hoja: ruta_colab

    return arbol

def escribir_arbol_colab(arbol, archivo_md, ruta_repo, nivel=1,user="zyntonyson"):
    for clave, valor in sorted(arbol.items()):
        if isinstance(valor, dict):
            archivo_md.write("   " * nivel + f"- {clave}\n")
            escribir_arbol_colab(valor, archivo_md, ruta_repo, nivel + 1)
        else:
            titulo = os.path.splitext(clave)[0]
            url = f"https://colab.research.google.com/github/{user}/{ruta_repo}/blob/main/{valor}"
            archivo_md.write("   " * nivel + f"- [{titulo}]({url})\n")

def generar_markdown_notebooks(ruta_repo_local, nombre_repo="main-folder", archivo_salida="notebooks.md"):
    arbol = construir_arbol_notebooks(ruta_repo_local)
    with open(archivo_salida, "w", encoding="utf-8") as f:
        f.write("*Notebooks*\n\n")
        escribir_arbol_colab(arbol, f, nombre_repo)



if __name__ == "__main__":
    ruta_repo_local=r"C:\Users\roman\Documents\proyectos\tripleten\bootcamp_ds_da"
    nombre_repo='bootcamp_ds_da'
    archivo_salida=r"C:\Users\roman\Documents\proyectos\tripleten\bootcamp_ds_da\Index-notebooks.md"
    generar_markdown_notebooks(ruta_repo_local=ruta_repo_local, nombre_repo=nombre_repo,archivo_salida=archivo_salida)

