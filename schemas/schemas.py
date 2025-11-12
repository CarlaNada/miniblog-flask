from marshmallow import Schema, fields, validate, ValidationError

class RegisterSchema(Schema):
    nombre_usuario = fields.Str(required=True, validate=validate.Length(min=3, max=50))
    email = fields.Email(required=True)
    password = fields.Str(required=True, validate=validate.Length(min=4))

class LoginSchema(Schema):
    email = fields.Email(required=True)
    password = fields.Str(required=True)

class PostSchema(Schema):
    titulo = fields.Str(required=True, validate=validate.Length(min=3))
    contenido = fields.Str(required=True, validate=validate.Length(min=3))
    categoria_id = fields.Int(load_default=None)

class CategoriaSchema(Schema):
    nombre = fields.Str(required=True, validate=validate.Length(min=3, max=50))

class ComentarioSchema(Schema):
    texto = fields.Str(required=True, validate=validate.Length(min=1, max=500))

class UserRolePatchSchema(Schema):
    role = fields.Str(required=True, validate=validate.OneOf(["user", "moderator", "admin"]))

register_schema = RegisterSchema()
login_schema = LoginSchema()
post_schema = PostSchema()
categoria_schema = CategoriaSchema()
comentario_schema = ComentarioSchema()
user_role_patch_schema = UserRolePatchSchema()