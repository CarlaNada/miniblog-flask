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

## Estructura del proyecto
miniblog/
│── app.py # Punto de entrada de la aplicación
│── models.py # Modelos de la base de datos
│── requirements.txt # Dependencias del proyecto
│── migrations/ # Migraciones de la base de datos
│── templates/ # Archivos HTML
│── environment/ # (ignorado por Git, entorno virtual local)
│── pycache/ # (ignorado por Git, archivos temporales)

## Instalación y configuración
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


## Funcionalidades
- Registro y gestión de usuarios.
- Creación, edición y eliminación de posts.
- Plantillas HTML con Jinja2.
- Migraciones de base de datos con Flask-Migrate.
