from flask.views import MethodView
from flask import jsonify
from flask_jwt_extended import get_jwt
from datetime import datetime, timedelta
from models.models import Usuario, Post, Comentario
from decorators.decoradores import roles_required

# Clase STATS 
# Mostrar estadisticas (mod/admin (admin ve extra))
class StatsAPI(MethodView):
    @roles_required(["moderador", "admin"])
    def get(self):
        total_posts = Post.query.count()
        total_comments = Comentario.query.count()
        total_users = Usuario.query.count()
        data = {
            "total_posts": total_posts,
            "total_comments": total_comments,
            "total_users": total_users
        }

        claims = get_jwt()
        #(admin ve extra)
        if claims.get("role") == "admin":
            last_week = datetime.utcnow() - timedelta(days=7)
            recent_posts = Post.query.filter(Post.fecha_creacion >= last_week).count()
            data["posts_last_week"] = recent_posts

        return jsonify(data), 200