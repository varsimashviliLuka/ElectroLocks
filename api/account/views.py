from flask_restx import Namespace, Resource, fields, marshal
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import request
from ..models.users import User
from werkzeug.security import generate_password_hash, check_password_hash

account_ns = Namespace('Account', description='account-თან დაკავშირებული API endpoint-ები')

user_model = account_ns.model(
    'CurrentUser', {
        'id': fields.Integer(required=False,description=''),
        'username': fields.String(required=True,description='01124096118'),
        'name': fields.String(required=True, description='Luka'),
        'last_name': fields.String(required=True, description='Varsimashvili'),
        'email': fields.String(required=False, description='varsimashvili.official@gmail.com'),
        'phone_number': fields.String(required=False, description='592159199'),
        'balance': fields.Integer(required=False, description='5.43'),
        'status': fields.Integer(required=True, description='2'),
        'is_admin': fields.Integer(required=False, description='0'),
        'services': fields.List(fields.Nested(
            {
                'id': fields.Integer(required=True,description='id'),
                'name': fields.String(required=True, description='სერვისის სახელი'),
                'location': fields.String(required=True, description=''),
                'description': fields.String(required=False, description=''),
                'status': fields.Integer(required=True, description=''),
                'created_at': fields.DateTime(required=False, description=''),
                'is_monthly_pay': fields.Boolean(required=True,description=''),
                'cost': fields.Float(required=True, description=''),
                'payed_at': fields.Date(required=False,description=''),
                'start_payment': fields.Date(required=True,description=''),
                'user_id': fields.Integer(required=True,description='')
            }
        ), description='list of services')
    }
)

password_chage_model = account_ns.model(
    'Password', {
        'old_password': fields.String(required=True, description='old password'),
        'new_password': fields.String(required=True, description='new password'),
        'retype_new_password': fields.String(required=True, description='retype new password')
    }
)

@account_ns.route('/account')
class Account(Resource):
    @jwt_required()
    def get(self):
        ''' საკუთარი მონაცემის ნახვა  '''
        
        username = get_jwt_identity()

        user = User.query.filter_by(username=username).first()
        if not user:
            return {'error': 'დაფიქსირდა შეცდომა მომხმარებლის ინფორმაციის წამოღებაზე'}, 404
        
        return marshal(user,user_model), 200
    
    @jwt_required()
    @account_ns.expect(password_chage_model)
    def put(self):
        ''' პაროლის შეცვლა '''

        data = request.get_json()
        username = get_jwt_identity()

        user = User.query.filter_by(username=username).first()

        if not user:
            return {'error': 'დაფიქსირდა შეცდომა მომხმარებლის ინფორმაციის წამოღებაზე'}, 404
        
        if not check_password_hash(user.password_hash, data.get('old_password')):
            return {'error': 'გთხოვთ შეიყვანოთ სწორი ახლანდელი პაროლი'}, 401
        
        if data.get('new_password') != data.get('retype_new_password'):
            return {'error': 'პაროლები არ ემთხვევა ერთმანეთს'}, 400
        
        if data.get('old_password') == data.get('new_password'):
            return {'error': 'ძველი პაროლი და ახალი პაროლი არ უნდა ემთხვეოდეს ერთმანეთს'}
        
        if len(data.get('new_password')) < 7:
            return {'error': 'პაროლი უნდა შეიცავდეს მინიმუმ 8 სიმბოლოს'}
        
        user.password_hash = generate_password_hash(data.get('new_password'))
        user.save()
        return {'message': 'პაროლი წარმატებით შეიცვალა'}, 200
