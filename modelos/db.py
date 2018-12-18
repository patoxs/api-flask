import pymssql
import ConfigParser, os
import json
import datetime

from resources.jsonEncoder import DateTimeEncoder


class ConectarDB():
	def __init__(self, database):
		config = ConfigParser.RawConfigParser()   
		configPath = r'config/.config.cfg'
		config.readfp(open(configPath))
		
		self.server = config.get('BD','servidor')
		self.port = config.get('BD','puerto')
		self.user = config.get('BD','usuario')
		self.password = config.get('BD','password')
		self.database = database

	def connect(self):
		try:
			conn = pymssql.connect(server=self.server, port=self.port, user=self.user, password=self.password, database=self.database)
			return conn.cursor()
		except Exception as e:
			print('Error, al conectarse a la base de datos - %s' %(e))
		
	def close(self, cursor):
		cursor.close()

	def return_mssql_dict(self, sql):
		try:

			cur = self.connect()
			cur.execute(sql)

			def return_dict_pair(row_item):
				return_dict = {}
				for column_name, row in zip(cur.description, row_item):
					if isinstance(row, datetime.datetime):
						row = DateTimeEncoder().encode(row.strftime("%d/%m/%Y"))

					return_dict[column_name[0]] = row
				return return_dict

			return_list = []
			for row in cur:
				row_item = return_dict_pair(row)
				return_list.append(row_item)

			self.close(cur)

			return return_list

		except Exception, e:
			print '%s' % (e)


	def execute_query(self, query):
		try:
			cursor = self.connect()
			cursor.execute(query)
			self.response = cursor.fetchall()
			self.close(cursor)
			return self.response
		except Exception as e:
			print('Error, al tratar de ejecutar la query - %s' %(e))

	def get_one_query(self, query):
		try:
			cursor = self.connect()
			cursor.execute(query)
			self.response = cursor.fetchone()
			self.close(cursor)
			return self.response
		except Exception as e:
			print('Error, al tratar de ejecutar la query - %s' %(e))
			
	def to_json(self):
		return json.dumps(self.response)


