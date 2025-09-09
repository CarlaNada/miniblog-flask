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

if __name__ == "__main__":
    app.run(debug=True)



