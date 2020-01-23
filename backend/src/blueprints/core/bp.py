from flask import Blueprint, Flask

bp = Blueprint('core', __name__)

def config(app: Flask):
    from src.blueprints.core import routes
    app.register_blueprint(bp)