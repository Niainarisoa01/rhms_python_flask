from os import environ, path
from dotenv import load_dotenv

basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, '..', '.env'))

class Config:
    SECRET_KEY = environ.get('SECRET_KEY') or 'dev-key-à-changer-en-production'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + path.join(basedir, '..', 'hrms.db')
    
class ProductionConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = environ.get('DATABASE_URL')

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
} 