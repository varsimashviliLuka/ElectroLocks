from flask_restx import Namespace, Resource, fields, marshal
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import request
from ..models.users import User
from ..account.views import user_model as show_user_model


user_ns = Namespace('User', description='მომხმარებლებთან დაკავშირებული API endpoint-ები')

user_model=user_ns.model(
    'User', {
        'id': fields.Integer(required=False,description='2'),
        'username': fields.String(required=True,description='01124096118'),
        'name': fields.String(required=True, description='Luka'),
        'last_name': fields.String(required=True, description='Varsimashvili'),
        'email': fields.String(required=False, description='varsimashvili.official@gmail.com'),
        'phone_number': fields.String(required=False, description='592159199'),
        'balance': fields.Integer(required=False, description='5.43'),
        'status': fields.Integer(required=True, description='2'),
        'registered_at': fields.DateTime(required=False, description=''),
        'is_admin': fields.Integer(required=False, description='1')
    }
)


@user_ns.route('/user/<int:user_id>')
class SpecificUser(Resource):
    @user_ns.expect(user_model)
    @jwt_required()
    def put(self,user_id):
        ''' მომხმარებლის ინფორმაციის განახლება '''
    
        # მოწმდება რამდენად აქვს მომხმარებელს უფლება, რომ ნახოს ყველა მომხმარებლის ინფორმაცია. check_permission() ფუნქცია
        # დამატებულის User მოდელზე /api/models/users.py
        if not User.query.filter_by(username=get_jwt_identity()).first().check_permission():
            return {'error': 'თქვენ არ გაქვთ მომხმარებლების ნახვის უფლება'}, 403
        
        user = User.query.filter_by(id=user_id).first()

        if not user:
            return {'error': 'მითითებული ID-ით მომხმარებელი ვერ მოიძებნა'}, 404
        
        data = request.get_json()
        try:
            balance = float(data.get('balance'))
        except (ValueError, TypeError):
            return {'error': 'გთხოვთ სწორი ფორმატით შეიყვანეთ ბალანსი'}, 400
        
        try:
            status = int(data.get('status'))
        except (ValueError, TypeError):
            return {'error': 'გთხოვთ სწორი ფორმატით შეიყვანეთ სტატუსი'}, 400
        
        try:
            is_admin = bool(data.get('is_admin'))
        except (ValueError, TypeError):
            return {'error': 'გთხოვთ სწორი ფორმატით შეიყვანეთ ბალანსი'}, 400
        
        try:
            user.username = data.get('username')
            user.name = data.get('name')
            user.last_name = data.get('last_name')
            user.email = data.get('email')
            user.phone_number = data.get('phone_number')
            user.balance = balance
            user.status = status
            user.is_admin = is_admin
            user.save()
            return {'message': 'მონაცემი წარმატებით განახლდა'}, 200
        except:
            return {'error': 'მონაცემის შენახვის დროს დაფიქსირდა შეცდომა'}, 500

        



    @jwt_required()
    def get(self, user_id):
        ''' კონკრეტული მომხმარებლის ინფორმაციის წამოღება '''

        # მოწმდება რამდენად აქვს მომხმარებელს უფლება, რომ ნახოს ყველა მომხმარებლის ინფორმაცია. check_permission() ფუნქცია
        # დამატებულის User მოდელზე /api/models/users.py
        if not User.query.filter_by(username=get_jwt_identity()).first().check_permission():
            return {'error': 'თქვენ არ გაქვთ მომხმარებლების ნახვის უფლება'}, 403
        
        user = User.query.filter_by(id=user_id).first()

        if not user:
            return {'error': 'მითითებული ID-ით მომხმარებელი ვერ მოიძებნა'}, 404
        
        return marshal(user,show_user_model), 200
        
        
    
    @jwt_required()
    def delete(self,user_id):
        ''' კონკრეტული მომხმარებლის წაშლა '''

        # მოწმდება რამდენად აქვს მომხმარებელს უფლება, რომ ნახოს ყველა მომხმარებლის ინფორმაცია. check_permission() ფუნქცია
        # დამატებულის User მოდელზე /api/models/users.py
        if not User.query.filter_by(username=get_jwt_identity()).first().check_permission():
            return {'error': 'თქვენ არ გაქვთ მომხმარებლების ნახვის უფლება'}, 403
        
        user = User.query.filter_by(id=user_id).first()

        if not user:
            return {'error': 'მითითებული ID-ით მომხმარებელი ვერ მოიძებნა'}, 404
        
        user.delete()
        return {'message': 'მომხმარებელი წარმატებით წაიშალა'}, 200



@user_ns.route('/user')
class Users(Resource):

    @jwt_required()
    def get(self):
        ''' ყველა მომხმარებლის ინფორმაციის წამოღება '''

        # მოწმდება რამდენად აქვს მომხმარებელს უფლება, რომ ნახოს ყველა მომხმარებლის ინფორმაცია. check_permission() ფუნქცია
        # დამატებულის User მოდელზე /api/models/users.py
        if not User.query.filter_by(username=get_jwt_identity()).first().check_permission():
            return {'error': 'თქვენ არ გაქვთ მომხმარებლების ნახვის უფლება'}, 403


        users = User.query.all()

        if not users:
            return {'error', 'მომხმარებლები ვერ მოიძებნა'}, 404
        
        # marshal ფუნქციით ვაბრუნებ მომხმარებლების სიას user_model ფორმატით
        return marshal(users,show_user_model),200
    