from flask_restx import Namespace,Resource

services_ns = Namespace('services', description='სერვისებთან დაკავშირებული API endpoint-ები')

@services_ns.route('/services')
class Services(Resource):
    def post(self):
        ''' სერვისის შექმნა '''
        pass
    def get(self):
        ''' ყველა სერვისის ინფორმაციის წამოღება '''
        pass
    
@services_ns.route('/services/<int:service_id>')
class SpecificServices(Resource):
    def get(self):
        ''' კონკრეტული სერვისის ინფორმაციის წამოღება '''
        pass
    def put(self):
        ''' კონკრეტული სერვისის რედაქტირება '''
        pass
    def delete(self):
        ''' კონკრეტული სერვისის წაშლა '''
        pass
    