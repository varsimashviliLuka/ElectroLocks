from flask_restx import Namespace, Resource, fields
from flask import request
from ..models.users import User
from werkzeug.security import generate_password_hash, check_password_hash


auth_ns = Namespace('authentication', description='authentication სთან დაკავშირებული API endpoint-ები')


signup_model=auth_ns.model(
    'User', {
        'username': fields.String(required=True,description='01124096118'),
        'name': fields.String(required=True, description='Luka'),
        'last_name': fields.String(required=True, description='Varsimashvili'),
        'email': fields.String(required=False, description='varsimashvili.official@gmail.com'),
        'phone_number': fields.String(required=False, description='592159199'),
        'password': fields.String(required=True, description='LUKAluka123'),
        'balance': fields.Integer(required=False, description='5.43')
    }
)


@auth_ns.route('/registration')
class Registration(Resource):

    @auth_ns.expect(signup_model)
    @auth_ns.marshal_with(signup_model)
    def post(self):
        ''' მომხმარებლის დარეგისტრირება '''

        data = request.get_json()
        
        new_user = User(
            username=data.get('username'),
            name=data.get('name'),
            last_name=data.get('last_name'),
            email=data.get('email'),
            phone_number=data.get('phone_number'),
            password_hash=generate_password_hash(data.get('password'))
        )

        new_user.save()

        return new_user, 200

@auth_ns.route('/login')
class Login(Resource):
    def post(self):
        ''' სისტემაში შესვლა '''
        pass