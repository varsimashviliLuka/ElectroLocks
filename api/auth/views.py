from flask_restx import Namespace, Resource, fields
from flask import request
from ..models.users import User
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token,create_refresh_token, jwt_required, get_jwt_identity


auth_ns = Namespace('Authentication', description='authentication სთან დაკავშირებული API endpoint-ები')


signup_model=auth_ns.model(
    'User', {
        'username': fields.String(required=True,description='01124096118'),
        'name': fields.String(required=True, description='Luka'),
        'last_name': fields.String(required=True, description='Varsimashvili'),
        'email': fields.String(required=False, description='varsimashvili.official@gmail.com'),
        'phone_number': fields.String(required=False, description='592159199'),
        'password': fields.String(required=True, description='LUKAluka123'),
        'balance': fields.Integer(required=False, description='5.43'),
        'is_admin': fields.Integer(required=False, description='1')
    }
)

login_model = auth_ns.model(
    'Login', {
        'username': fields.String(required=True, description='Username'),
        'password': fields.String(required=True, description='Password')
    }
)


@auth_ns.route('/registration')
class Registration(Resource):

    @auth_ns.doc(security='JsonWebToken')
    @jwt_required()
    @auth_ns.expect(signup_model)
    def post(self):
        ''' მომხმარებლის დარეგისტრირება '''

        username = get_jwt_identity()

        user = User.query.filter_by(username=username).first()

        if not user.check_permission():
            return {'error': 'თქვენ არ გაქვთ მომხმარებლის რეგისტრაციის უფლება'}, 403

        data = request.get_json()
        new_user = User.query.filter_by(username=data.get('username')).first()

        if new_user:
            return {'error': 'მომხმარებელი უკვე რეგისტრირებულია'}, 409

        new_user = User(
            username=data.get('username'),
            name=data.get('name'),
            last_name=data.get('last_name'),
            email=data.get('email'),
            phone_number=data.get('phone_number'),
            password_hash=generate_password_hash(data.get('password')),
            balance = data.get('balance'),
            is_admin = data.get('is_admin')
        )

        new_user.create()

        return {'message': 'მომხმარებელი წარმატებით დარეგისტრირდა'}, 200
    


@auth_ns.route('/login')
class Login(Resource):

    @auth_ns.expect(login_model)
    def post(self):
        ''' სისტემაში შესვლა '''

        data = request.get_json()

        username=data.get('username')
        
        user=User.query.filter_by(username=username).first()

        if (user is not None) and check_password_hash(user.password_hash,data.get('password')):
            access_token = create_access_token(identity=user.username)
            refresh_token = create_refresh_token(identity=user.username)

            response = {'access_token': access_token,
                        'refresh_token': refresh_token}
            
            return response, 200
        
        return {'error': 'არასწორი მომხმარებელი/პაროლი'}, 401
    

    
@auth_ns.route('/refresh')
class Refresh(Resource):
    
    @auth_ns.doc(security='JsonWebToken')
    @jwt_required(refresh=True)
    def post(self):
        ''' JWT ტოკენის დარეფრეშება '''

        username = get_jwt_identity()

        access_token = create_access_token(identity=username)

        return {'access_token': access_token}, 200