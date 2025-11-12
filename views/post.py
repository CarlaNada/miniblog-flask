from flask.views import MethodView
from flask import jsonify, request
from flask_jwt_extended import jwt_required, get_jwt
from datetime import datetime
from marshmallow import ValidationError
from app import db
from models.models import Post, db
from decorators.decoradores import check_ownership, owner_or_roles
from schemas.schemas import post_schema 

# Función auxiliar para el decorador owner_or_roles
def get_post_owner_id(post_id):
    #Retorna el ID del usuario dueño del post
    post = Post.query.get_or_404(post_id) 
    return post.usuario_id

#Clase POST y POSTDETAIL
#Mostrar todos los posts (get) y crear un post nuevo (post)

class PostAPI(MethodView):
    def get(self):
        posts = Post.query.filter_by(is_published=True).order_by(Post.fecha_creacion.desc()).all()
        data = [
            {
                "id": post.id,
                "titulo": post.titulo,              
                "contenido": post.contenido,         
                "usuario_id": post.usuario_id,       
                "categoria_id": post.categoria_id,   
                "fecha_creacion": post.fecha_creacion.isoformat(),
                "publicado": post.is_published, 
                "fecha_actualizacion": post.update_at.isoformat() if post.update_at else None 
            }
            for post in posts
        ]
        return jsonify(data), 200

    #Nuevo post (requiere token)
    @jwt_required()
    def post(self):
        #Validamos datos con Marshmallow
        try:
            data = post_schema.load(request.get_json())
        except ValidationError as err:
            return jsonify({"errors": err.messages}), 400
        
        claims = get_jwt()
        usuario_id = claims["user_id"]

        #Nuevo post
        nuevo_post = Post(
            titulo=data['titulo'],
            contenido=data['contenido'],
            categoria_id=data['categoria_id'],
            usuario_id=usuario_id,
            is_published=False
        )   
        
        db.session.add(nuevo_post)
        db.session.commit()
        return jsonify({"message": "Post creado", "id": nuevo_post.id}), 201

#Mostrar - get (user) / actualizar y eliminar - put y delete (moderador y admin)
class PostDetailAPI(MethodView):
    def get(self, post_id):
        post = Post.query.get_or_404(post_id)

        is_owner = False
        is_admin = False
        try:
            claims = get_jwt()
            uid = claims.get("user_id")
            role = claims.get("role")
            is_owner = post.usuario_id == uid
            is_admin = role in ("admin", "moderator")
        except Exception:
            pass

        if not post.is_published and not is_owner and not is_admin:
            # Si no está publicado y no eres ni dueño ni admin/mod
            return jsonify({"message": "Post no encontrado o no publicado"}), 404 
            
        return jsonify({
            "id": post.id,
            "titulo": post.titulo,
            "contenido": post.contenido,
            "autor_id": post.usuario_id,
            "categoria_id": post.categoria_id,
            "fecha_creacion": post.fecha_creacion.isoformat(),
            "publicado": post.is_published,
            "fecha_actualizacion": post.update_at.isoformat() if post.update_at else None
        }), 200

    #Editar posts (autor o admin)
    @owner_or_roles(get_post_owner_id, ["admin"])
    def put(self, post_id):
        try:
            data = post_schema.load(request.get_json(), partial=True)
        except ValidationError as err:
            return jsonify({"errors": err.messages}), 400

        post = Post.query.get_or_404(post_id)

        if "titulo" in data: 
            post.titulo = data["titulo"]
        if "contenido" in data: 
            post.contenido = data["contenido"]
        if "categoria_id" in data:
            post.categoria_id = data["categoria_id"]

        if "is_published" in request.get_json():
            post.is_published = request.get_json()["is_published"]


        post.update_at = datetime.utcnow()
        db.session.commit()
        return jsonify({"message": "Post actualizado"}), 200

    # Eliminar posts (autor o admin)
    @owner_or_roles(get_post_owner_id, ["admin"]) # solo dueño o admin pueden eliminar
    def delete(self, post_id):
        post = Post.query.get_or_404(post_id)
        
        db.session.delete(post)
        db.session.commit()
        return jsonify({"message": "Post eliminado"}), 200
        if not check_ownership(post.usuario_id):
            return {"message": "No autorizado"}, 403