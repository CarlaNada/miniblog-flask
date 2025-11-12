from flask.views import MethodView
from flask import jsonify, request
from flask_jwt_extended import jwt_required, get_jwt
from marshmallow import ValidationError
from models.models import Comentario, Post, db
from decorators.decoradores import owner_or_roles
from schemas.schemas import comentario_schema

def get_comment_owner_id(comentario_id):
    comentario = Comentario.query.get_or_404(comentario_id) 
    return comentario.usuario_id

#Clase COMENTARIO
#Mostrar/crear comentarios (publico y users)
class ComentarioAPI(MethodView):
    def get(self, post_id):
        Post.query.get_or_404(post_id)
        comentarios = Comentario.query.filter_by(post_id=post_id, is_visible=True).all()
        return jsonify([
            {"id": comentario.id,
            "text": comentario.texto, 
            "user_id": comentario.usuario_id,
            "created_at": comentario.fecha_creacion.isoformat()}
            for comentario in comentarios
        ]), 200

    #Crear comentario
    @jwt_required()
    def post(self, post_id):
        Post.query.get_or_404(post_id)
        try:
            data = comentario_schema.load(request.get_json())
        except ValidationError as err:
            return jsonify({"errors": err.messages}), 400

        claims = get_jwt()
        uid = claims["user_id"] # ID de usuario del token
        texto = data.get("texto")

        comentario_nuevo = Comentario(texto=texto, usuario_id=uid, post_id=post_id)

        db.session.add(comentario_nuevo)
        db.session.commit()
        return jsonify({"message": "Comentario creado", "id": comentario_nuevo.id}), 201

#Borrar comentario (autor, moderador, admin)
class ComentarioDetailAPI(MethodView):
    @owner_or_roles(get_comment_owner_id, ["moderator", "admin"])
    def delete(self, comentario_id):
        comentario = Comentario.query.get_or_404(comentario_id)

        db.session.delete(comentario)
        db.session.commit()
        return jsonify({"message": "Comentario eliminado"}), 200