from modelos.db import ConectarDB

class User(object):
	def __init__(self, _id, username, password):
		self.id = _id
		self.username = username
		self.password = password

	def __str__(self):
		return "User(id='%s')" % self.id

class Login():

	@classmethod
	def find_by_rut(self, rut):
		database = ConectarDB('sistema_integrado')
		sql = "select * from bdi.usuario where rut = %d" % (rut)
		respuesta = database.return_mssql_dict(sql)
		users = [
			User(respuesta[0]['id_usuario'], respuesta[0]['rut'], respuesta[0]['clave']),
		]
		username_table = {u.username: u for u in users}
		return username_table

	@classmethod
	def find_by_id(self, id):
		database = ConectarDB('sistema_integrado')
		sql = "select * from bdi.usuario where id_usuario = %d" % (id)
		respuesta = database.return_mssql_dict(sql)
		users = [
			User(respuesta[0]['id_usuario'], respuesta[0]['rut'], respuesta[0]['clave']),
		]
		userid_table = {u.id: u for u in users}
		return userid_table

