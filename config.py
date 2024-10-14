import os

class Config:     
    TESTING = False
    SQLALCHEMY_DATABASE_URI = 'postgresql://flask_api_db_t8sf_user:CdqXu3VHlzpmLR6mbeIM2RPjdXq0GqbZ@dpg-cs5uj1lumphs73b2t840-a.oregon-postgres.render.com/flask_api_db_t8sf'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'your-secret-key'
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or 'supersecret'

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'postgresql://flask_api_db_t8sf_user:CdqXu3VHlzpmLR6mbeIM2RPjdXq0GqbZ@dpg-cs5uj1lumphs73b2t840-a.oregon-postgres.render.com/flask_api_db_t8sf'
