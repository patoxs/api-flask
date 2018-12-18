from flask import Flask
from flask_restful import Api
from flask_jwt import JWT, jwt_required

from security import authenticate, identity
from resources.datos import DatosResource



app = Flask(__name__)
app.debug = True
app.config['SECRET_KEY'] = 'super-secret'
api = Api(app)

jwt = JWT(app, authenticate, identity) # /auth

api.add_resource(DatosResource, '/datos/<int:rut>')
#api.add_resource(GetOnePostResource, '/post/<int:year>/<int:month>/<string:title>')
#api.add_resource(GetListPostResource, '/post_list/<string:taxonomy>/<int:quantity>')
#api.add_resource(GetSearchPostResource, '/search/<string:word>')
#api.add_resource(MediaResource, '/media')
#api.add_resource(PersonResource, '/person/<string:email_author>')


if __name__ == '__main__':
	app.run(host='10.20.3.186',port=5000)
