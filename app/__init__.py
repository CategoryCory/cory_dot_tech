from flask import Flask
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

from app.main import bp as main_bp  # noqa: E402
app.register_blueprint(main_bp)

