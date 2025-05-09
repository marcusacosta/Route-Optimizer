from flask import Flask

def create_app():
    app = Flask(__name__)

    from .routes import optimizer_bp  # ✅ This line ensures your routes are included
    app.register_blueprint(optimizer_bp)  # ✅ This line registers your /optimize route

    return app
