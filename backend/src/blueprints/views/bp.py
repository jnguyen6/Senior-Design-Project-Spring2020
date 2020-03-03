from flask import Blueprint, Flask

bp = Blueprint('views', __name__)

def config(app: Flask):
    from src.blueprints.views import routes
    app.register_blueprint(bp)
