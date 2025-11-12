from flask.views import MethodView
from flask import jsonify, request
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token
from marshmallow import ValidationError

from models.models import Usuario, UserCredentials, db
from schemas.schemas import register_schema, login_schema

# Clase REGISTRO
class RegistroAPI(MethodView):
    def post(self):
        # Validacion con Marshmallow
        try:
            data = register_schema.load(request.get_json())
        except ValidationError as err:
            return jsonify({"errors": err.messages}), 400

        nombre_usuario = data.get('nombre_usuario')
        email = data.get('email')
        password = data.get('password')

        # Validacion existencia
        if Usuario.query.filter((Usuario.email == email) | (Usuario.nombre_usuario == nombre_usuario)).first():
            return jsonify({"message": "El usuario o email ya existen"}), 409
        
        # Crear hash
        hashed_pw = generate_password_hash(password)
        
        nuevo_usuario = Usuario(
            nombre_usuario=nombre_usuario, 
            email=email, 
            role="user" 
        )
        db.session.add(nuevo_usuario)
        db.session.flush()

        nueva_credencial = UserCredentials(
            password_hash=hashed_pw,
            user=nuevo_usuario
        )

        db.session.add(nueva_credencial)
        db.session.commit()
        return jsonify({"message": "Usuario creado"}), 201
    
# Clase LOGIN 
class LoginAPI(MethodView):
    def post(self):
        #Validacon con Marshmallow
        try:
            data = login_schema.load(request.get_json())
        except ValidationError as err:
            return jsonify({"errors": err.messages}), 400
            
        email = data.get('email')
        password = data.get('password')

        # Validacion credenciales
        usuario = Usuario.query.filter_by(email=email).first()

        if not usuario:
            return jsonify({"message": "Credenciales inválidas"}), 401

        credenciales = UserCredentials.query.filter_by(usuario_id=usuario.id).first()
        
        if not credenciales or not check_password_hash(credenciales.password_hash, password):
            return jsonify({"message": "Credenciales inválidas"}), 401

        if not usuario.is_active:
            return jsonify({"message": "Usuario desactivado"}), 403

        # datos del token
        claims = {"role": usuario.role, "user_id": usuario.id, "email": usuario.email}
        token = create_access_token(identity=str(usuario.id), additional_claims=claims) 
        
        return jsonify({"access_token": token, "role": usuario.role}), 200

