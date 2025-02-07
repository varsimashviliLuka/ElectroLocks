from flask_restx import Namespace, Resource

user_ns = Namespace('user', description='მომხმარებლებთან დაკავშირებული API endpoint-ები')

@user_ns.route('/user/<int:user_id>')
class SpecificUser(Resource):
    def put(self):
        ''' მომხმარებლის ინფორმაციის განახლება '''

        pass
    def get(self):
        ''' კონკრეტული მომხმარებლის ინფორმაციის წამოღება '''

        pass

    def delete(self):
        ''' კონკრეტული მომხმარებლის წაშლა '''

        pass

@user_ns.route('/user')
class User(Resource):
    def get(self):
        ''' ყველა მომხმარებლის ინფორმაციის წამოღება '''

        pass