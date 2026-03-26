# 🛠️ Solución: Push bloqueado por secreto en commit anterior (GitHub Push Protection)

## 📌 Problema

GitHub bloquea el `push` porque detecta un secreto (por ejemplo, un token) dentro del historial del repositorio.

Incluso si el archivo ya fue eliminado en un commit reciente, el error persiste porque el secreto sigue presente en un **commit anterior**.

---

## 🎯 Objetivo

Editar un commit anterior para eliminar el archivo sensible del historial y poder hacer `push` correctamente.

---

## 🧭 Pasos

### 1. Revisar commits recientes

```
git log --oneline -n 5
```

Identificar:
- el commit que contiene el secreto
- su posición en el historial

---

### 2. Iniciar rebase interactivo

```
git rebase -i HEAD~2
```

En el editor, cambiar `pick` por `edit` en el commit con el problema:

```
edit 78eeab8 Updates for Project
pick 8fa3dec Remove token file and ignore secrets
```

---

### 3. Eliminar el archivo sensible del commit

```
git rm --cached v7/07-herramientas-desarrollo/token.txt
```

> `--cached` elimina el archivo del commit sin borrarlo necesariamente del sistema local.

---

### 4. Agregar el archivo al `.gitignore`

```
echo v7/07-herramientas-desarrollo/token.txt >> .gitignore
git add .gitignore
```

---

### 5. Reescribir el commit

```
git commit --amend --no-edit
```

---

### 6. Continuar el rebase

```
git rebase --continue
```

---

### 7. Saltar commit vacío (si aparece)

Si Git muestra:

> "The previous cherry-pick is now empty"

Ejecutar:

```
git rebase --skip
```

Esto ocurre cuando el commit siguiente ya no tiene cambios nuevos.

---

### 8. Subir cambios al remoto (reescribiendo historial)

```
git push origin main --force
```

---

## 📦 Comandos utilizados

```
git log --oneline -n 5
git rebase -i HEAD~2
git rm --cached v7/07-herramientas-desarrollo/token.txt
git add .gitignore
git commit --amend --no-edit
git rebase --continue
git rebase --skip
git push origin main --force
```

---

## 🧠 Explicación

GitHub bloquea el `push` porque el secreto sigue existiendo en el historial.

Eliminar el archivo en un commit nuevo **no es suficiente**.

Es necesario:
- editar el commit donde se introdujo el secreto
- reescribir el historial
- volver a subir los cambios

---

## ⚠️ Recomendaciones

- Revocar inmediatamente cualquier token expuesto
- No guardar credenciales en archivos versionados
- Usar variables de entorno (`.env`)
- Agregar archivos sensibles al `.gitignore`

Ejemplo:

```
.env
token.txt
```

---

## 📝 Resumen corto

Se corrigió un `push` bloqueado editando un commit anterior con `git rebase -i`, eliminando el archivo sensible con `git rm --cached`, agregándolo al `.gitignore`, reescribiendo el commit con `--amend`, continuando el rebase y forzando el `push` con `--force`.