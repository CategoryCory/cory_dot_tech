from flask import Flask
from app.extensions import db, migrate

def create_app(config_path: str) -> Flask:
    app = Flask(__name__)
    app.config.from_object(config_path)

    db.init_app(app)
    migrate.init_app(app, db)

    from app.main import bp as main_bp  # noqa: E402
    app.register_blueprint(main_bp)

    from app import models  # noqa: E402, F401

    return app
