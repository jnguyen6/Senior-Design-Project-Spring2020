from flask import Flask

def create_app():
    app = Flask(__name__)
    from src.blueprints.core import bp as bp_core
    bp_core.config(app)

    return app