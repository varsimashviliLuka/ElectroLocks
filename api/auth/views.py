from flask_restx import Namespace, Resource

auth_ns = Namespace('authentication', description='authentication სთან დაკავშირებული API endpoint-ები')

@auth_ns.route('/registration')
class Registration(Resource):
    def post(self):
        ''' მომხმარებლის დარეგისტრირება '''
        pass

@auth_ns.route('/login')
class Login(Resource):
    def post(self):
        ''' სისტემაში შესვლა '''
        pass