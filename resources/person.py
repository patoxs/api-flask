from flask import Flask
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required

import datetime
from slugify import slugify
from resources.jsonEncoder import DateTimeEncoder

from modelos.person import PersonModel


posts = []

class PersonResource(Resource):

	parser = reqparse.RequestParser()
	parser.add_argument('login', help='Whoooo - This field cannot be left blank!')
	parser.add_argument('password',  help='Whoooo - This field cannot be left blank!')
	parser.add_argument('nicename',  help='Whoooo - This field cannot be left blank!')
	parser.add_argument('email',  help='Whoooo - This field cannot be left blank!')
	parser.add_argument('image',  help='Whoooo - This field cannot be left blank!')
	parser.add_argument('status',  type=int, help='Whoooo - This field cannot be left blank!')
	parser.add_argument('key_activate', help='Whoooo - This field cannot be left blank!')
	parser.add_argument('id_person_type', type=int, help='Whoooo - This field cannot be left blank!')
	parser.add_argument('description',  help='Whoooo - This field cannot be left blank!')
	parser.add_argument('facebook', help='Whoooo - This field cannot be left blank!')
	parser.add_argument('twitter', help='Whoooo - This field cannot be left blank!')

	#@jwt_required()
	def post(self):

		result = PersonResource.parser.parse_args()

		p = PersonModel(
			login = result['login'],
			password = result['password'],
			nicename = result['nicename'],
			email = result['email'],
			image = result['image'],
			status = result['status'],
			key_activate = result['key_activate'],
			id_person_type = result['id_person_type'],
			description = result['description'],
			facebook = result['facebook'],
			twitter = result['twitter']	
		)
		return p.save_to_db()

	def get(self, email_author):
		data = PersonModel.find_by_email(email_author)	
		if data:
			persons = data.json()
			return {"author": persons},200
		else:
			return {'message': 'Not found person'}, 404	
		

	




