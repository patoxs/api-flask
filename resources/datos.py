from flask import Flask, jsonify
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required, current_identity

import json
import datetime

from modelos.db import ConectarDB

datos = []

class DatosResource(Resource):
	parser = reqparse.RequestParser()
	parser.add_argument('rut', type=int, help='Whoooo - This field cannot be left blank!')

	@jwt_required()
	def get(self, rut):
		if rut:
			database = ConectarDB('sistema_integrado')
			sql = "EXEC [barra].[p_datos_generales_usuario_get] @rut = %d" % (rut)
			result = database.return_mssql_dict(sql)
			return json.dumps(result), 200

		return {"message":"Person not found"}, 404