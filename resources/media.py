from flask import Flask
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required,current_identity
import werkzeug

from helpers.images import ImageProcessing

from modelos.media import MediaModel


class MediaResource(Resource):

	parser = reqparse.RequestParser()
	parser.add_argument('media', help='Whoooo - This field cannot be left blank!')
	parser.add_argument('description',  help='Whoooo - This field cannot be left blank!')
	parser.add_argument('file',  help='Whoooo - This field cannot be left blank!', type=werkzeug.datastructures.FileStorage, location='files')

	@jwt_required()
	def post(self):

		result = MediaResource.parser.parse_args()
		imagen = result['file']
		photo = ImageProcessing()
		img = photo.upload_file(imagen)
		url = photo.create_images('crop',img)
		
		user = current_identity.id

		p = MediaModel(
			media = result['media'],
			url = url,
			description = result['description'],
			owner = user,
			ping = 0
		)
		p.save_to_db()
		return {"message":"Image create", "name": url}, 201

	


class GetOnePersonResource(Resource):

	def get(self,year,month,title):
		year = str(year)
		month = str(month)
		title = str(title)
		url = "/{0}/{1}/{2}".format(year, month, title)
		
		data = MediaResource.find_by_url(url)
		if data:
			return { 
				'title': data.title , 
				'excerpt': data.excerpt, 
				'content': data.content, 
				'url': data.url, 
				'datetime':  data.datetime
				}, 200
		
				#return PersonModel.response_json(p), 200
				#data = json.dumps( DateTimeEncoder().encode(query) )

		return {"message":"Person not found"}, 404
			
		






