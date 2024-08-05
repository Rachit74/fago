from flask import Flask, blueprints, Blueprint

API_URL = "http://localhost:8080"

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = "abc123"


    from .views import views
    from .auth import auth


    app.register_blueprint(views, url_path="/")
    app.register_blueprint(auth, url_path="/auth")

    return app