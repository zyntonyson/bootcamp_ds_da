
# 🛡️ Git Push Protection: Eliminación de token comprometido con `git rebase -i`

> **Incidencia:** GitHub bloquea el push por contener un token expuesto  
> **Objetivo:** Eliminar commits comprometidos y limpiar el historial

---

## 📍 1. Contexto del error

Al intentar hacer push:

```bash
error: GH013: Repository rule violations found for refs/heads/main.
Push cannot contain secrets
```

GitHub detectó un **token expuesto** en el commit `5464b21`.

---

## 🕵️‍♂️ 2. Identificar los commits sospechosos

```bash
git log --oneline
```

Ubicamos commits como:

- `5464b21` (token)
- `c610825` y `295f30f` (relacionados al archivo afectado)

---

## 🔧 3. Ejecutar rebase interactivo

```bash
git rebase -i 8bf2703
```

🔹 `8bf2703` es el commit anterior a los que queremos modificar

---

## 📝 4. Cambiar `pick` por `edit`

```bash
edit 5464b21 Updates...
edit c610825 Updates...
edit 295f30f Updates...
```

💡 Se hace para detenernos en esos commits y corregir el contenido

---

## 🛠️ 5. Limpiar archivos y continuar

En cada parada:

1. **Abrir el archivo**
   ```bash
   nano archivo.ipynb
   ```

2. **Eliminar el token y las marcas de conflicto**
   ```text
   <<<<<<<, =======, >>>>>>>
   ```

3. **Guardar cambios y seguir**
   ```bash
   git add archivo.ipynb
   git commit --amend --no-edit
   git rebase --continue
   ```

---

## 🧼 6. Si hay errores durante el rebase

- Cancelar:
  ```bash
  git rebase --abort
  ```

- Continuar:
  ```bash
  git rebase --continue
  ```

- Forzar limpieza:
  ```bash
  rm -rf .git/rebase-merge
  ```

---

## 🔍 7. Verificar que ya no hay secretos

```bash
git grep 'ghp_' $(git rev-list --all)
```

---

## 🚀 8. Push limpio

```bash
git push origin main --force
```

⚠️ *¡OJO!* Esto sobrescribe el historial remoto. Avisa a tu equipo si estás en colaboración.

---

## 🧠 9. Buenas prácticas

- Nunca subas notebooks con tokens hardcodeados
- Usa `.env` y `.gitignore`
- Configura escaneo local con `pre-commit` o `git-secrets`

---

## ✅ 10. Aprendido

> Esta fue una excelente práctica para entender:
> - Reescritura de historial con `rebase -i`
> - Resolución de conflictos
> - Políticas de seguridad de GitHub
