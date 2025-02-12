from flask import Flask, render_template
from .user.views import user_ns
from .auth.views import auth_ns
from .account.views import account_ns
from .services.views import services_ns
from flask_restx import Api
from .config.config import config_dict
from .utils import db
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from .commands  import init_db, populate_db

COMMANDS = [init_db,populate_db]

def create_app(config=config_dict['dev']):

    app=Flask(__name__)
    CORS(app)
    app.config.from_object(config)

    @app.route('/')
    def index():
        return render_template('index.html')


    db.init_app(app)

    jwt=JWTManager(app)

    migrate = Migrate(app,db)

    api=Api(app=app,title='Electric Locks',version='1.0', 
            description='ElectricLocks API',doc='/api',
            authorizations=config.AUTHORIZATION, prefix='/api')
    
    api.add_namespace(user_ns,path='/user')
    api.add_namespace(auth_ns, path='/auth')
    api.add_namespace(account_ns, path='/account')
    api.add_namespace(services_ns, path='/services')


    register_commands(app)


    return app


def register_commands(app):
    for command in COMMANDS:
        app.cli.add_command(command)