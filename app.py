from flask import Flask, render_template, request, url_for, redirect
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = (
    "mysql+pymysql://root:@localhost:3306/miniblog_db"
)

db = SQLAlchemy(app)
migrate = Migrate(app, db)

from models import Usuario, Categoria, Comentario, Post

@app.route("/")
def index():
    #renderizar los post por el orden que desee
    return render_template(
        "index.html"
    )

@app.route("/usuario_nuevo", methods=['POST', 'GET'])
def usuario_nuevo():
    if request.method == "POST":
        usuario = request.form["usuario"]
        password = request.form["password"]
        email = request.form["email"]

        nuevo_usuario = Usuario(usuario=usuario, email=email, password=password)
        db.session.add(nuevo_usuario)
        db.session.commit()
        return redirect(url_for("index"))
    
    return render_template(
        "usuario_nuevo.html"
    )

@app.route("/post_nuevo", methods=['POST', 'GET'])
def post_nuevo():
    usuarios = Usuario.query.all()
    categorias = Categoria.query.all()

    if request.method == "POST":
        usuario_id = request.form["usuario_id"]
        titulo = request.form["titulo"]
        categoria_id = request.form["categoria_id"]
        contenido = request.form["contenido"]
        fecha = request.form["fecha"]
        
        nuevo_post = Post(titulo=titulo, contenido=contenido, fecha=fecha, usuario_id=int(usuario_id), categoria_id=int(categoria_id))
        db.session.add(nuevo_post)
        db.session.commit()
        return redirect(url_for("index"))
    return render_template(
        "post_nuevo.html", usuarios=usuarios, categorias=categorias
    )

app.route('/post/<int:post_id>', methods=['POST', 'GET'])
def post_detail(post_id):
    post = Post.query.get_or_404(post_id)
    


    return render_template('post_details.html', post=post)

if __name__ == "__main__":
    app.run(debug=True)



