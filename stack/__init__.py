from flask import current_app, Flask

def create_app():
    app = Flask(__name__)
    app.secret_key ='dev'
    from .auth import bp
    app.register_blueprint(bp)

    @app.route("/")
    def index():
        return "hello"

    return app
