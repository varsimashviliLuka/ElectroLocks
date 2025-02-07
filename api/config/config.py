import os
from decouple import config

class Config:
    SECRET_KEY=config('SECRET_KEY','secret')
    SQLALCHEMY_TRACK_MODIFICATIONS=False

    MYSQL_HOST = config('MYSQL_HOST', 'default_host')
    MYSQL_DATABASE = config('MYSQL_DATABASE', 'default_database')
    MYSQL_USER = config('MYSQL_USER', 'default_user')
    MYSQL_PASSWORD = config('MYSQL_PASSWORD', 'default_password')
    # MySQL connection URI
    # SQLALCHEMY_DATABASE_URI = f'mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}/{MYSQL_DATABASE}'

class DevConfig(Config):
    DEBUG=config('DEBUG',cast=bool)
    SQLALCHEMY_ECHO=True
    SQLALCHEMY_DATABASE_URI = f'mysql+pymysql://{Config.MYSQL_USER}:{Config.MYSQL_PASSWORD}@{Config.MYSQL_HOST}/{Config.MYSQL_DATABASE}'

class TestConfig(Config):
    pass

class ProdConfig(Config):
    pass

config_dict = {
    'dev': DevConfig,
    'prod': ProdConfig,
    'test': TestConfig
}