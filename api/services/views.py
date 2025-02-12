from flask_restx import Namespace,Resource, fields, marshal
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import request
from ..models.users import User
from ..models.services import Services

services_ns = Namespace('Services', description='სერვისებთან დაკავშირებული API endpoint-ები')

service_create_model = services_ns.model('ServiceCreateModel',{
    'name': fields.String(required=True, description='სერვისის სახელი'),
    'location': fields.String(required=True, description=''),
    'description': fields.String(required=False, description=''),
    'status': fields.Integer(required=True, description=''),
    'is_monthly_pay': fields.Boolean(required=True,description=''),
    'cost': fields.Float(required=True, description=''),
    'payed_at': fields.Date(required=False,description=''),
    'start_payment': fields.Date(required=True,description=''),
    'user_id': fields.Integer(required=True,description='')
})

service_model = services_ns.model('ServiceModel',{
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
})


@services_ns.route('/services')
class ServicesApi(Resource):

    @services_ns.expect(service_create_model)
    @jwt_required()
    def post(self):
        ''' სერვისის შექმნა '''
        
        user = User.query.filter_by(username=get_jwt_identity()).first()

        if not user.check_permission():
            return {'error': 'თქვენ არ გაქვთ სერვისის დამატების უფლება'}, 403
        
        data = request.get_json()
        try:
            service = Services(name=data.get('name'),
                            location=data.get('location'),
                            description=data.get('description',''),
                            status=data.get('status',0),
                            is_monthly_pay=data.get('is_monthly_pay'),
                            cost=data.get('cost'),
                            payed_at=data.get('payed_at'),
                            start_payment=data.get('start_payment'),
                            user_id=data.get('user_id'))
            service.create()
            return {'message': 'სერვისი წარმატებით შეიქმნა'}
        except:
            return {'error': 'სერვისის შექმნისას დაფიქსირდა შეცდომა'}, 400


    @jwt_required()
    def get(self):
        ''' ყველა სერვისის ინფორმაციის წამოღება '''

        user = User.query.filter_by(username=get_jwt_identity()).first()

        if not user.check_permission():
            return {'error': 'თქვენ არ გაქვთ სერვისის დამატების უფლება'}, 403

        services = Services.query.all()

        if not services:
            return {'error': 'სერვისები ვერ მოიძებნა'}, 404
        

        return marshal(services,service_model), 200
        

    
@services_ns.route('/services/<int:service_id>')
class SpecificServices(Resource):
    @jwt_required()
    def get(self,service_id):
        ''' კონკრეტული სერვისის ინფორმაციის წამოღება '''
        
        user = User.query.filter_by(username=get_jwt_identity()).first()

        if not user.check_permission():
            return {'error': 'თქვენ არ გაქვთ სერვისის ნახვის უფლება'}, 403
        
        service = Services.query.filter_by(id=service_id).first()

        if not service:
            return {'error': 'სერვისი ვერ მოიძებნა'}, 404
        
        return marshal(service,service_model), 200

    @services_ns.expect(service_create_model)
    @jwt_required()
    def put(self, service_id):
        ''' კონკრეტული სერვისის რედაქტირება '''

        user = User.query.filter_by(username=get_jwt_identity()).first()

        if not user.check_permission():
            return {'error': 'თქვენ არ გაქვთ სერვისის ნახვის უფლება'}, 403
        
        service = Services.query.filter_by(id=service_id).first()

        if not service:
            return {'error': 'სერვისი ვერ მოიძებნა'}, 404
        
        data = request.get_json()

        service.name = data.get('name')
        service.location = data.get('location')
        service.description = data.get('description')
        service.status = data.get('status')
        service.is_monthly_pay = data.get('is_monthly_pay')
        service.cost = data.get('cost')
        service.payed_at = data.get('payed_at')
        service.start_payment = data.get('start_payment')
        service.save()

        return {'message': 'სერვისი წარმატებით დარედაქტირდა'}, 200
    

    @jwt_required()
    def delete(self,service_id):
        ''' კონკრეტული სერვისის წაშლა '''

        user = User.query.filter_by(username=get_jwt_identity()).first()

        if not user.check_permission():
            return {'error': 'თქვენ არ გაქვთ სერვისის ნახვის უფლება'}, 403
        
        service = Services.query.filter_by(id=service_id).first()

        if not service:
            return {'error': 'სერვისი ვერ მოიძებნა'}, 404
        
        service.delete()
        return {'message':'სერვისი წარმატებით წაიშალა'}, 200
    