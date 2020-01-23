from src.blueprints.core.bp import bp

@bp.route("/")
def hello_world():
    return "Hello World"