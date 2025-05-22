import os
from dotenv import load_dotenv
from app import create_app

env = os.getenv('APP_ENV', 'development')
load_dotenv(f'.env.{env}')

config_name: str

match env:
    case ['production']:
        config_name = 'config.ProductionConfig'
    case _:
        config_name = 'config.DevelopmentConfig'

app = create_app(config_name)
