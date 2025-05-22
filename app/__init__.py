from flask import Flask
# from config import Config

def create_app(config_path: str) -> Flask:
    app = Flask(__name__)
    app.config.from_object(config_path)

    from app.main import bp as main_bp  # noqa: E402
    app.register_blueprint(main_bp)

    return app
