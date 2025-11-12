from flask.views import MethodView
from flask import jsonify, request
from marshmallow import ValidationError
from models.models import Categoria,db
from decorators.decoradores import roles_required
from schemas.schemas import categoria_schema

#Clase CATEGORIA y CATEGORIADETAIL
#Mostrar categorias (publico) y crear categorias (mod/admin)
class CategoriaAPI(MethodView):
    def get(self):
        categorias = Categoria.query.all()
        return jsonify([
            {"id": categoria.id,
            "nombre": categoria.nombre} 
            for categoria in categorias
        ])
    
    #Crear categorias (solo admin)
    @roles_required(["admin"])
    def post(self):
        try:
            data = categoria_schema.load(request.get_json())
        except ValidationError as err:
            return jsonify({"errors": err.messages}), 400
            
        nombre = data.get("nombre")
        
        if Categoria.query.filter_by(nombre=nombre).first():
            return jsonify({"message": "La categoría ya existe"}), 409
        
        categoria_nueva = Categoria(nombre=nombre)
        db.session.add(categoria_nueva)
        db.session.commit()

        return jsonify({"message": "Creada", "id": categoria_nueva.id}), 201

#Editar categorias (mod/admin), eliminar categorias (admin)
class CategoriaDetailAPI(MethodView):
    #Editar (moderator/admin)
    @roles_required(["moderator", "admin"])
    def put(self, categoria_id):
        categoria = Categoria.query.get_or_404(categoria_id)
        
        try:
            data = categoria_schema.load(request.get_json())
        except ValidationError as err:
            return jsonify({"errors": err.messages}), 400
            
        nombre = data.get("nombre")
        
        categoria.nombre = nombre
        db.session.commit()
        return jsonify({"message": "Actualizada"}), 200

    # Eliminar (admin) 
    @roles_required(["admin"])
    def delete(self, categoria_id):
        categoria = Categoria.query.get_or_404(categoria_id)
        
        db.session.delete(categoria)
        db.session.commit()
        return jsonify({"message": "Eliminada"}), 200