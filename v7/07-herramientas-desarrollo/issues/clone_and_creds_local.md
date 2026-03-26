# 📘 Tutorial: Clonar un repositorio privado de GitHub y configurar credenciales locales (Windows)

Este tutorial te guía paso a paso para:

- Aceptar una invitación a un repositorio privado
- Clonar el repositorio en tu máquina
- Configurar las credenciales **solo para ese repositorio** (sin afectar otros)

---

## ✅ Paso 1: Aceptar la invitación al repositorio

1. Ve a tu correo o entra directamente a GitHub.
2. Abre el link del repositorio que te compartieron.
3. Si es privado, verás un botón **"Aceptar invitación"**.
4. Haz clic y asegúrate de poder ver el repo en tu lista:  
   👉 https://github.com/YOUR-USERNAME?tab=repositories

---

## ✅ Paso 2: Clonar el repositorio

1. En GitHub, ve al botón verde **"Code"** → selecciona **HTTPS**.
2. Copia la URL del repositorio:

    ```
    https://github.com/organizacion/repositorio-invitado.git
    ```

3. En tu terminal de Git Bash:

    ```bash
    git clone https://github.com/organizacion/repositorio-invitado.git
    cd repositorio-invitado
    ```

---

## ✅ Paso 3: Configurar credenciales solo para este repositorio

Dentro del repositorio clonado:

```bash
git config credential.helper manager-core
```

Esto guarda la configuración solo en `.git/config`.

Puedes verificarlo con:

```bash
git config --local credential.helper
```

---

## ✅ Paso 4: Autenticarse con GitHub (token)

Haz un `git pull` o `git push` para que GitHub te pida autenticarte:

```bash
git pull
```

### 🔐 Cuando Git te pida usuario y contraseña:

- **Usuario**: Tu nombre de usuario GitHub
- **Contraseña**: Un **token personal de GitHub (PAT)**

🔗 [Genera un token aquí](https://github.com/settings/tokens) → "Generate new token (classic)"  
✔ Marca el permiso `repo`

Una vez ingresado, el token se guarda solo para este proyecto.

---

## ✅ Paso 5 (opcional): Verifica tu `.git/config`

Debe contener algo como esto:

```
[credential]
    helper = manager-core

[remote "origin"]
    url = https://github.com/organizacion/repositorio-invitado.git
```

---

## ❌ ¿Cómo eliminar las credenciales solo de este repo?

Puedes hacerlo con:

```bash
git credential-manager reject https://github.com/organizacion/repositorio-invitado.git
```

O manualmente en:

- Abrir `Administrador de credenciales de Windows`
- Eliminar entrada de GitHub relacionada

---

## 📝 Notas

- Esta configuración **no afecta a tus otros proyectos Git**.
- Puedes tener múltiples repos con diferentes usuarios sin conflicto.
