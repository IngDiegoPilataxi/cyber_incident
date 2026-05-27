# SECURITY.md - Laboratorio 4: Autenticación y Seguridad
**Estudiante:** Diego Ricardo Pilataxi Pita
**Curso:** Ethical Hacking

---

### Q0: ¿Por qué un rastreador de incidentes no autenticado es un problema de seguridad?
Un sistema de gestión de vulnerabilidades expuesto públicamente permite que cualquier persona en internet (incluyendo atacantes) pueda leer información crítica sobre las brechas de seguridad de una organización, o peor aún, eliminar registros de incidentes para ocultar sus rastros. Es una fuga de información crítica y una falta total de control de acceso.

### Q1: Modelo User vs UserProfile - ¿Por qué usar OneToOneField?
Usamos `UserProfile` vinculado con un `OneToOneField` porque modificar el modelo `User` nativo de Django es complejo y puede romper módulos integrados. El `OneToOneField` garantiza que la relación sea estricta (un usuario solo puede tener un perfil, y un perfil pertenece a un solo usuario). De esta forma, extendemos los datos (agregando el rol de Analista o Admin) manteniendo limpio el núcleo de autenticación de Django.

### Q2: Propósito del parámetro `?next=` y el riesgo de redirección abierta (Open Redirect)
El parámetro `?next=` sirve para mejorar la experiencia del usuario: si alguien intenta entrar a `/incidents/` sin estar logueado, Django lo manda al login pero recuerda en el parámetro `?next=` a dónde quería ir originalmente, para redirigirlo allí tras iniciar sesión con éxito. 
El riesgo de seguridad ("Open Redirect") ocurre si Django no valida ese parámetro. Un atacante podría enviar un enlace engañoso como `http://tusitio.com/login/?next=http://sitio-malicioso.com`. El usuario inicia sesión confiando en tu sitio, y es redirigido automáticamente a la página del atacante, donde le pueden robar la sesión.

### Q3: Autenticación vs Autorización (Ejemplos concretos del laboratorio)
* **Autenticación (AuthN):** Verifica *quién* eres. En el lab, esto es la pantalla de Login y el decorador `@login_required`.
* **Autorización (AuthZ):** Verifica *qué puedes hacer*. En el lab, esto es la función `if not profile.is_admin():` que bloquea las vistas.
* **Consecuencia de omitir la autorización:** Si implementas autenticación pero saltas la autorización, un usuario con rol de "Analista" podría iniciar sesión (Autenticarse) y luego acceder libremente a la URL para eliminar incidentes, porque el sistema no restringe sus permisos.

### Q4: Riesgo de asignación masiva (Mass Assignment) y `commit=False`
Usamos `commit=False` en el formulario para pausar el guardado en la base de datos y permitirnos inyectar de forma segura el usuario actual (`request.user`) desde el servidor. Si permitiéramos que el campo `reported_by` se enviara a través del formulario HTML (incluso oculto), un atacante podría interceptar la petición POST y cambiar el ID para hacerse pasar por otro usuario (ej. un administrador). Este ataque se relaciona con la **Manipulación de Parámetros** y vulnerabilidades tipo IDOR (Insecure Direct Object Reference).

### Q5: Por qué ocultar botones en la plantilla NO es suficiente seguridad
Ocultar los botones de "Editar" y "Eliminar" en el HTML usando `{% if %}` solo oculta la interfaz visual (Seguridad por oscuridad). Sin embargo, un atacante o usuario curioso que conozca la estructura de las rutas puede evadir esto simplemente escribiendo la URL manualmente en el navegador (ej. `/incidents/1/edit/`). Este ataque se conoce como **Forced Browsing** (Navegación Forzada) o Acceso a Nivel de URL. Por eso la seguridad real debe estar en el backend (en el archivo `views.py`).

### Q6 (Bonus): Ataques de Fuerza Bruta y mitigación con `django-axes`
* **Fuerza Bruta:** Es un ataque automatizado donde se prueban miles de combinaciones de contraseñas por segundo en un formulario de login hasta adivinar la correcta.
* **Mitigación:** `django-axes` mitiga esto bloqueando la dirección IP o la cuenta de usuario tras un número definido de intentos fallidos.
* **Trade-off de un límite bajo:** Si el `AXES_FAILURE_LIMIT` es muy bajo (ej. 2 intentos), se corre el riesgo de causar un ataque de **Denegación de Servicio (DoS)** accidental, donde los usuarios legítimos quedan bloqueados constantemente al equivocarse tipeando su contraseña.
* **Otra protección:** Además del límite de intentos, un endpoint de login se puede proteger implementando Autenticación Multifactor (MFA/2FA) o añadiendo un CAPTCHA.