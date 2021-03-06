from flask import current_app, Flask

def create_app():

    app = Flask(__name__)

    app.secret_key ='dev'

    from .auth import bp
    app.register_blueprint(bp)

    from .api import api_bp
    app.register_blueprint(api_bp)
    
    @app.route("/")
    def root():
        return "hello"
    
    def index():
        pass
    app.add_url_rule('/', 'index', index)

    return app
