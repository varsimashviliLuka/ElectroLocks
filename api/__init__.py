from flask import Flask
from .user.views import user_ns
from .auth.views import auth_ns
from flask_restx import Api
from .config.config import config_dict
from .utils import db
from .models.services import Services
from .models.users import User
from flask_migrate import Migrate


def create_app(config=config_dict['dev']):
    app=Flask(__name__)

    app.config.from_object(config)

    db.init_app(app)

    migrate = Migrate(app,db)

    api=Api(app)

    api.add_namespace(user_ns,path='/user')
    api.add_namespace(auth_ns, path='/auth')


    @app.shell_context_processor
    def make_shell_context():
        return {
            'db':db,
            'User': User,
            'Services': Services,
        }



    return app