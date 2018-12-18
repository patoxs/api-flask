from werkzeug.security import safe_str_cmp
from resources.auth import ResourceAuth

def authenticate(username,password):
	usuario = ResourceAuth.find_by_username(username)
	user = usuario.get(username)
	if user and safe_str_cmp(user.password, password):
		return user

def identity(payload):
	id_usuario = payload['identity']
	usuario = ResourceAuth.find_by_id(id_usuario)
	return usuario.get(id_usuario)