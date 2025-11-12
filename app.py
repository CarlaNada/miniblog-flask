from flask import Flask, render_template, request, url_for, redirect
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = (
    "mysql+pymysql://root:@localhost:3306/miniblog_db"
)
app.config["JWT_SECRET_KEY"] = "clave-secreta-larga" 
app.config["JWT_TOKEN_LOCATION"] = ["headers"] #define dónde buscar el token
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = 60 * 60 * 24  #24 hs (en segundos)

db = SQLAlchemy(app)
migrate = Migrate(app, db)
jwt = JWTManager(app)

from models.models import Usuario, Categoria, Comentario, Post, UserCredentials

#Vistas API (registrarlas)
from views.user import UserAPI, UserDetailAPI
from views.autenticacion import RegistroAPI, LoginAPI
from views.post import PostAPI, PostDetailAPI
from views.comentario import ComentarioAPI, ComentarioDetailAPI
from views.categoria import CategoriaAPI, CategoriaDetailAPI
from views.stats import StatsAPI


# HTML
@app.route("/")
def index():
    posts = Post.query.order_by(Post.fecha_creacion.desc()).all()
    return render_template(
        "index.html", posts=posts
    )

@app.route("/usuario_nuevo", methods=['POST', 'GET'])
def usuario_nuevo():
    if request.method == "POST":
        usuario = request.form["usuario"]
        password = request.form["password"]
        email = request.form["email"]

        hashed_pw = generate_password_hash(password)
        nuevo_usuario = Usuario(nombre_usuario=usuario, email=email, password=hashed_pw)        
        db.session.add(nuevo_usuario)
        db.session.commit()
        return redirect(url_for("index"))
    
    return render_template(
        "usuario_nuevo.html"
    )

@app.route("/post_nuevo", methods=['POST', 'GET'])
def post_nuevo():
    usuarios = Usuario.query.all()

    if request.method == "POST":
        usuario_id = request.form["usuario_id"]
        titulo = request.form["titulo"]
        categoria_id = request.form["categoria_id"]
        contenido = request.form["contenido"]
        
        nuevo_post = Post(titulo=titulo, contenido=contenido, usuario_id=int(usuario_id), categoria_id=int(categoria_id))
        db.session.add(nuevo_post)
        db.session.commit()
        return redirect(url_for("index"))
    
    return render_template(
        "post_nuevo.html", usuarios=usuarios
    )

@app.context_processor
def inject_categories():
    categorias = Categoria.query.all()
    return dict(categorias=categorias)

@app.route('/post/<int:post_id>', methods=['POST', 'GET'])
def post_detail(post_id):
    post = Post.query.get_or_404(post_id)
    if request.method == "POST":
        texto = request.form["texto"]
        usuario_id = request.form["usuario_id"]
        
        nuevo_comentario = Comentario(texto=texto, usuario_id=int(usuario_id), post_id=post.id)
        db.session.add(nuevo_comentario)
        db.session.commit()
        return redirect(url_for("post_detail", post_id=post.id))
    
    usuarios = Usuario.query.all()
    return render_template('post_details.html', post=post, usuarios=usuarios)

#===== ENPOINTS =====

# ------ Registro/Login -------
register_view = RegistroAPI.as_view('api_register')
app.add_url_rule(
    '/api/register', 
    view_func=register_view, 
    methods=['POST']
    )

login_view = LoginAPI.as_view('api_login')
app.add_url_rule(
    '/api/login', 
    view_func=login_view, 
    methods=['POST']
    )

# ------ Post/PostDetail -------
post_view = PostAPI.as_view('posts_api')
app.add_url_rule(
    '/api/posts', 
    view_func=post_view, 
    methods=['GET', 'POST']
    )

post_detail_view = PostDetailAPI.as_view('post_detail_api')
app.add_url_rule(
    '/api/posts/<int:post_id>', 
    view_func=post_detail_view, 
    methods=['GET', 'PUT', 'DELETE']
    )

# ------ Comentario/ComentarioDetail -------
comment_view = ComentarioAPI.as_view('comentario_api')
app.add_url_rule(
    '/api/posts/<int:post_id>/comments', 
    view_func=comment_view, 
    methods=['GET', 'POST']
    )

comment_detail_view = ComentarioDetailAPI.as_view('comentario_detail_api')
app.add_url_rule(
    '/api/comments/<int:comentario_id>', 
    view_func=comment_detail_view, 
    methods=['DELETE']
    )

# ------ Categoria/CategoriaDetail -------
categories_view = CategoriaAPI.as_view('categoria_api')
app.add_url_rule(
    '/api/categories',
    view_func=categories_view,
    methods=['POST', 'GET']
)

categories_detail_view = CategoriaDetailAPI.as_view('categoria_detail_api')
app.add_url_rule(
    '/api/categories/<int:categoria_id>',
    view_func=categories_detail_view,
    methods=['PUT', 'DELETE']
)

# ------ Stats -------
stats_view = StatsAPI.as_view('stats_api')
app.add_url_rule(
    '/api/stats',
    view_func=stats_view,
    methods=['GET']
)

# ------ User -------
user_view = UserAPI.as_view('user_api')
app.add_url_rule(
    '/api/users',
    view_func=user_view,
    methods = ['GET']    
)

user_detail_view = UserDetailAPI.as_view('user_detail_api')
app.add_url_rule(
    '/api/users/<int:user_id>',
    view_func=user_detail_view,
    methods = ['GET', 'PATCH', 'DELETE']    
)

if __name__ == "__main__":
    app.run(debug=True)
