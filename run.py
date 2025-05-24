import os
from typing import Any
import sqlalchemy as sa
import sqlalchemy.orm as so
from dotenv import load_dotenv
from app import create_app
from app.extensions import db
from app.models import WorkExperience, Project, ContactSubmission

env = os.getenv('APP_ENV', 'development')
load_dotenv(f'.env.{env}')

config_name: str

match env:
    case ['production']:
        config_name = 'config.ProductionConfig'
    case _:
        config_name = 'config.DevelopmentConfig'

app = create_app(config_name)

@app.shell_context_processor
def make_shell_context() -> dict[str, Any]:
    return {
        'sa': sa,
        'so': so,
        'db': db,
        'WorkExperience': WorkExperience,
        'Project': Project,
        'ContactSubmission': ContactSubmission,
    }
