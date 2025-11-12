# MiniBlog con Flask
Este proyecto implementa una API RESTful para un Miniblog utilizando el framework Flask en Python, SQLAlchemy como ORM, y Flask-JWT-Extended para la autenticación y autorización basada en roles (user, moderator, admin).

# Estructura del proyecto
miniblog/
│── app.py
│── decorators/
│── environment/
│── migrations/
│── models/
│── requirements.txt
│── schemas/
│── templates/
│── views/
│── pycache/

# Instalación y configuración
1. Clonar el repositorio
    git clone git@github.com:CarlaNada/miniblog-flask.git
    cd miniblog-flask

2. Crear y activar entorno virtual
    python3 -m venv environment
    source environment/bin/activate (Linux/masOS)

3. Instalar dependencias
    pip install -r requirements.txt

4. Configurar la base de datos
    flask db init
    flask db migrate -m "Inicial"
    flask db upgrade

5. Ejecutar la app
    python app.py
    flask run
    Servidor disponible: http://127.0.0.1:5000

# Documentación de Endpoints (API REST)
Los endpoints de la API están prefijados con /api/. 
Todas las peticiones deben usar Content-Type: application/json.

1. Autenticación
    Metodo POST --- URL: /api/register --- Registra un nuevo usuario (user por defecto). (Permisos: publico)
    Metodo POST --- URL: /api/login --- Inicia sesión y devuelve un access_token JWT. (Permisos: publico)

2. Posts
    Metodo GET --- URL: /api/posts --- Lista todos los posts. (Permisos: publico)
    Metodo POST --- URL: /api/posts --- Crea un nuevo post. (Permisos: Autenticacion (user, moderator, admin))
    Metodo GET --- URL: /api/posts/<int:post_id> --- Muestra un post específico. (Permisos: publico)
    Metodo PUT --- /api/posts/<int:post_id> --- Edita un post. (Permisos: autor o admin)
    Metodo DELETE --- URL: /api/posts/<int:post_id> --- /api/posts/<int:post_id> (Permisos: autor o admin)

3. Comentarios
    Metodo GET --- URL: /api/posts/<int:post_id>/comments --- Lista los comentarios visibles para un post. (Permisos: publico)
    Metodo POST --- URL: /api/posts/<int:post_id>/comments --- Crea un nuevo comentario para un post. (Permisos: Autenticacion (user, moderator, admin))
    Metodo DELETE --- URL: /api/comments/<int:comentario_id> --- Elimina un comentario. (Permisos: autor, moredator o admin)

4. Usuarios
    Metodo GET --- URL: /api/users --- Lista todas los usuarios. (Permisos: admin)
    Metodo GET --- URL: /api/users/<int:user_id> --- Muestra detalles de un usuario. (Permisos: propio useuario o admin)
    Metodo PATCH --- URL: /api/users/<int:user_id> --- Cambia el rol de un usuario. (Permisos: admin)
    Metodo DELETE --- URL: /api/users/<int:user_id> --- Activa/desactiva un usuario. (Permisos: admin)

5. Categorias
    Metodo GET --- URL: /api/categories --- Lista todas las categorías. (Permisos: publico)
    Metodo POST --- URL: /api/categories --- Crea una nueva categoría. (Permisos: admin)
    Metodo PUT --- URL: /api/categories --- Edita una categoría. (Permisos: moderator o admin)
    Metodo DELETE --- URL: /api/categories --- Elimina una categoría. (Permisos: admin)

6. Estadisticas
    Metodo GET --- URL: /api/stats --- Muestra estadísticas generales de la plataforma. (Permisos: moderator o admin)

# Credenciales de prueba para cada rol
