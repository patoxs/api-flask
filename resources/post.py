from flask import Flask, jsonify
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required, current_identity

import json
import datetime
from slugify import slugify

from modelos.post import PostModel, TaxonomyModel
from modelos.person import PersonModel


posts = []

class DateTimeEncoder(json.JSONEncoder):
	def default(self, obj):
		if isinstance(obj, datetime.datetime):
			return obj.isoformat()
		elif isinstance(obj, datetime.date):
			return obj.isoformat()
		elif isinstance(obj, datetime.timedelta):
			return (datetime.datetime.min + obj).time().isoformat()
		else:
			return super(DateTimeEncoder, self).default(obj)

class PostResource(Resource):

	parser = reqparse.RequestParser()
	parser.add_argument('title', help='Whoooo - This field cannot be left blank!')
	parser.add_argument('excerpt',  help='Whoooo - This field cannot be left blank!')
	parser.add_argument('content',  help='Whoooo - This field cannot be left blank!')
	parser.add_argument('password',  help='Whoooo - This field cannot be left blank!')
	parser.add_argument('parent', type=int, help='Whoooo - This field cannot be left blank!')
	parser.add_argument('post_order', type=int, help='Whoooo - This field cannot be left blank!')
	parser.add_argument('taxonomy', help='Whoooo - This field cannot be left blank!')
	parser.add_argument('image', help='Whoooo - This field cannot be left blank!')

	@jwt_required()
	def post(self):

		result = PostResource.parser.parse_args()

		today = datetime.datetime.now()
		year = str(today.year)
		month = str(today.month)

		slug_post = slugify(result['title'])
		url = "/{0}/{1}/{2}".format(year, month, slug_post)

		#obtener el usuario que esta creando el post print(current_identity)
		user = current_identity.id

		if self.taxonomy_exist(result['taxonomy']):
			#status 1:publish; 2:waiting; 3:delete
			news = PostModel(
				title = result['title'],
				excerpt = result['excerpt'],
				content = result['content'],
				datetime = str(today),
				status = 1,
				ping = 0,
				password = result['password'],
				url = url,
				modified = str(today),
				parent = result['parent'],
				post_order = result['post_order'],
				id_person = user,
				image = result['image']
			)

			

			if news.find_by_title(result['title']):
				return {"message":"Post already exist"}, 200

			taxonomys = result['taxonomy'].split(",")
			news_exist = 0
			
			for tax in taxonomys:

				t = TaxonomyModel.find_by_taxonomy(tax.strip())

				if news_exist == 0:
					id_post = news.save_to_db()
					p = news.find_by_title(result['title'])
					news_exist = 1

				news.create_relacion_taxonomy(p,t)
			
			return {"message":"Post created"}, 201

		else:

			return {"message":"Taxonomys not exist"}, 404

	def taxonomy_exist(self, taxs):
		taxonomys = taxs.split(",")

		for tax in taxonomys:
			print(tax)
			t = TaxonomyModel.find_by_taxonomy(tax.strip())
			if t is None:
				return False
		return True

	@classmethod
	def return_taxonomy(cls, data):
		taxonomys = dict()
		for t in TaxonomyModel.return_taxonomy(data):
			taxonomys[t.id] = t.taxonomy
		return taxonomys

	@classmethod
	def return_person(cls, data):
		taxonomys = dict()
		for t in TaxonomyModel.return_taxonomy(data):
			taxonomys[t.id] = t.taxonomy
		return taxonomys

	@classmethod
	def return_post(cls, data):
		news = dict()
		for d in reversed(data):
			taxonomys = PostResource.return_taxonomy(d[0])
			news[d[1]] = PostResource.to_json(
				title = d[2],
				excerpt = d[3],
				content = d[4],
				datetime = d[5],
				url = d[6], 
				image = d[7],
				taxonomy = taxonomys)
		return news

	@classmethod
	def to_json(cls, **kwargs):
		return {
			'title': kwargs['title'],
			'excerpt': kwargs['excerpt'],
			'content': kwargs['content'],
			'datetime': DateTimeEncoder().encode(kwargs['datetime'].strftime("%d/%m/%Y")),
			'url': kwargs['url'],
			'image': kwargs['image'],
			'taxonomy': kwargs['taxonomy']
		}



class GetOnePostResource(Resource):

	def get(self,year,month,title):
		year = str(year)
		month = str(month)
		title = str(title)
		url = "/{0}/{1}/{2}".format(year, month, title)
		
		data = PostModel.find_by_url(url)
		
		post_id = data.id

		if data:
			news = data.json()
			person = PersonModel.find_by_id(news['id_person'])
			news['author'] = person.json()
			news['taxonomy'] = PostResource.return_taxonomy(data)
			news['prev'] = GetOnePostResource.return_post_prev(post_id)
			news['next'] = GetOnePostResource.return_post_next(post_id)

			return {"post": news},200

		return {"message":"Post not found"}, 404

	@classmethod
	def return_post_prev(cls, post_id):
		id = post_id - 1

		if id < 1:
			return {'No post'}

		data = PostModel.find_by_id(id)
		if data:
			return {
				'title': data.title,
				'image': data.image,
				'url': data.url
			}
		else:
			return {'No post'}

	@classmethod
	def return_post_next(cls, post_id):
		id = post_id + 1

		data = PostModel.find_by_id(id)
		if data:
			return {
				'title': data.title,
				'image': data.image,
				'url': data.url
			}
		else:
			return {'No post'}


class GetListPostResource(Resource):

	#@jwt_required()
	def get(self, taxonomy, quantity):

		if taxonomy == "all":
			data = PostModel.return_all_post(quantity)
		else:
			data = PostModel.return_post_by_taxonomy(taxonomy, quantity)
			
		if data:
			return PostResource.return_post(data), 200
		else:
			return {'message': 'Not found post'}, 404	
		


class GetSearchPostResource(Resource):
	def get(self, word):
		data = PostModel.search_in_content(word)
		if data:
			return PostResource.return_post(data), 200
		else:
			return {'message': 'Not found post'}, 404	


