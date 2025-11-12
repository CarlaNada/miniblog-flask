from app import db
from datetime import datetime

class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre_usuario = db.Column(db.String(50), nullable=False, unique=True)
    email = db.Column(db.String(120), nullable=False, unique=True)
    #password = db.Column(db.String(200), nullable=False, unique=True)
    role = db.Column(db.String(20), default='user', nullable=False) #'user', 'moderator' o 'admin'
    is_active = db.Column(db.Boolean, default=True) #para activar/desactivar usuarios
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    credentials = db.relationship("UserCredentials", backref="user", uselist=False)
    posts = db.relationship("Post", backref="autor", lazy=True)
    comentarios = db.relationship("Comentario", backref="autor", lazy=True)

class Categoria(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False, unique=True)
    posts = db.relationship("Post", backref="categoria", lazy=True)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(150), nullable=False)
    contenido = db.Column(db.Text, nullable=False)
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    usuario_id = db.Column(db.Integer, db.ForeignKey("usuario.id"), nullable=False)
    categoria_id = db.Column(db.Integer, db.ForeignKey("categoria.id"), nullable=False)
    comentarios = db.relationship("Comentario", backref="post", lazy=True)

    is_published = db.Column(db.Boolean, default=True) #para activar/desactivar posts
    update_at = db.Column(db.DateTime, default=datetime.utcnow)

class Comentario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    texto = db.Column(db.Text, nullable=False)
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    usuario_id = db.Column(db.Integer, db.ForeignKey("usuario.id"), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey("post.id"), nullable=False)

    is_visible = db.Column(db.Boolean, default=True) # para l moderacion

class UserCredentials(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    role = db.Column(db.String(20), default='user', nullable=False)
    password_hash = db.Column(db.String(255), nullable=False) # genera hash largos
    usuario_id = db.Column(db.Integer, db.ForeignKey("usuario.id"), nullable=False)