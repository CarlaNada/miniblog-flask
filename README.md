# MiniBlog con Flask
Un pequeño proyecto de blog desarrollado en Python usando Flask.  
El objetivo es crear una aplicación web simple que permita manejar publicaciones y usuarios.

# Tecnologías utilizadas
- Python 3
- Flask
- SQLAlchemy
- Jinja2
- Flask-Migrate
- MySQL

# Estructura del proyecto
miniblog/
│── app.py
│── models.py
│── requirements.txt
│── migrations/
│── templates/
│── environment/
│── pycache/

# Instalación y configuración
1. Clonar el repositorio
    git clone git@github.com:CarlaNada/miniblog-flask.git
    cd miniblog-flask

2. Crear y activar entorno virtual (opcional pero recomendado)
    python3 -m venv venv
    source venv/bin/activate

3. Instalar dependencias
    pip install -r requirements.txt

4. Configurar la base de datos
    flask db init
    flask db migrate -m "Inicial"
    flask db upgrade

5. Ejecutar la app
    flask run
    Navegador: http://127.0.0.1:5000


# Funcionalidades
- Registro y gestión de usuarios.
- Creación de posts y comentarios.
- Plantillas HTML con Jinja2.
- Migraciones de base de datos con Flask-Migrate.
