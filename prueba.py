from flask import Flask
from modelos.db import ConectarDB


app = Flask(__name__)
app.debug = True

@app.route("/<int:rut>")
def prueba(rut):
	database = ConectarDB('sistema_integrado')
	database.execute_query('select * from bdi.usuario where rut = %d' % (rut))
	return database.to_json()


if __name__ == '__main__':
	app.run(port=5000)
