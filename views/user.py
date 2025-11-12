from flask.views import MethodView
from flask import jsonify, request
from flask_jwt_extended import jwt_required, get_jwt
from marshmallow import ValidationError
from models.models import Usuario, UserCredentials, db
from decorators.decoradores import roles_required
from schemas.schemas import user_role_patch_schema 

#Mostrar usuarios / activar-desactivar (solo admin)
#Mostrar lista usuarios completa
class UserAPI(MethodView):
    @roles_required(["admin"])
    def get(self):
        usuarios = Usuario.query.order_by(Usuario.id.asc()).all()
        return jsonify([
            {"id": usuario.id, 
            "username": usuario.nombre_usuario, 
            "email": usuario.email, 
            "role": usuario.role, 
            "is_active": usuario.is_active}
            for usuario in usuarios
        ]), 200
    
#Mostrar usuario especfico, cambiar rol, desactivar usuario
class UserDetailAPI(MethodView):
    @jwt_required()
    def get(self, user_id):
        claims = get_jwt()
        uid = claims['user_id']
        role = claims['role']
        
        #Validar autorizacion
        if role != 'admin' and uid != user_id:
            return jsonify({"message": "Permiso denegado. No autorizado."}), 403
            
        usuario = Usuario.query.get_or_404(user_id)
        
        return jsonify({
            "id": usuario.id, 
            "nombre_usuario": usuario.nombre_usuario, 
            "email": usuario.email, 
            "role": usuario.role, 
            "is_active": usuario.is_active
        }), 200

    #Cambio de rol
    @roles_required(["admin"])
    def patch(self, user_id):
        try:
            data = user_role_patch_schema.load(request.get_json())
        except ValidationError as err:
            return jsonify({"errors": err.messages}), 400
            
        usuario = Usuario.query.get_or_404(user_id)
        nuevo_role = data.get("role")
        
        usuario.role = nuevo_role
        db.session.commit()
        return jsonify({"message": "Rol actualizado"}), 200

    #Desactivar usuarios
    @roles_required("admin")
    def delete(self, user_id):
        usuario = Usuario.query.get_or_404(user_id)
        usuario.is_active = False
        db.session.commit()
        return jsonify({"message": "Usuario desactivado"}), 200