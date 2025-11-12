from functools import wraps
from flask import jsonify
from flask_jwt_extended import jwt_required, get_jwt

#Permite sólo si el rol del token está en 'roles'
def roles_required(*roles):
    """Permite solo si el usuario tiene alguno de los roles dados."""
    def outer(fn):
        @wraps(fn)
        @jwt_required()
        def wrapper(*args, **kwargs):
            claims = get_jwt()
            role = claims.get("role")
            if role not in roles:
                return jsonify({"message": "No autorizado: rol insuficiente"}), 403
            return fn(*args, **kwargs)
        return wrapper
    return outer

def owner_or_roles(get_owner_id_func, *roles):
    """
    Permite si el usuario es dueño del recurso o tiene uno de los roles dados.
    Ejemplo:
    @owner_or_roles(lambda post_id: Post.query.get(post_id).usuario_id, 'admin')
    """
    def outer(fn):
        @wraps(fn)
        @jwt_required()
        def wrapper(*args, **kwargs):
            claims = get_jwt()
            uid = claims.get("user_id")
            role = claims.get("role")

            if role in roles:
                return fn(*args, **kwargs)

            owner_id = get_owner_id_func(**kwargs)
            if uid == owner_id:
                return fn(*args, **kwargs)
            return jsonify({"message": "No autorizado: no sos el dueño"}), 403
        return wrapper
    return outer

def check_ownership(resource_owner_id):
    """Verifica si el usuario autenticado es dueño del recurso o admin."""
    claims = get_jwt()
    if claims["role"] == "admin":
        return True
    return claims["user_id"] == resource_owner_id
