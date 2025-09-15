from flask import Flask, render_template, request
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

@app.route("/comentarios", methods=['POST', 'GET'])
def comentarios():
    if request.method == "POST":
        name =request.form["usuario"]
    return render_template(
        "comentarios.html"
    )

@app.route("/usuario_nuevo", methods=['POST', 'GET'])
def usuario_nuevo():
    return render_template(
        "usuario_nuevo.html"
    )

@app.route("/post_nuevo", methods=['POST', 'GET'])
def post_nuevo():
    return render_template(
        "post_nuevo.html"
    )

app.route('/post/<int:post_id>')
def post_detail(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post_details.html', post=post)

if __name__ == "__main__":
    app.run(debug=True)



