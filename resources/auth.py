from modelos.login import Login

class ResourceAuth:
	
	@classmethod
	def find_by_username(self, rut):
		return Login.find_by_rut(rut)

	@classmethod
	def find_by_id(self, id):
		return Login.find_by_id(id)
		
