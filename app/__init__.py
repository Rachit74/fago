from flask import Flask, blueprints, Blueprint

API_URL = "http://localhost:8080"

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = "abc123"


    from .views import views


    app.register_blueprint(views, url_path="/")

    return app