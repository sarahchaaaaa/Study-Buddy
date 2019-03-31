#!/usr/bin/env python3

import tornado.ioloop
import tornado.options
import tornado.web
import sys
import sqlite3
import json

# Constants

PORT = 9000

# Handlers

netids = []

class Database():
	def __init__(self):
		self.db_path = './database'

	# create connection to database
	def _connect(self):
		connection = sqlite3.connect(self.db_path)
		cursor = connection.cursor()
		return connection, cursor

	def get_user_info(self):
		table = 'user_table'
		columns = ['NETID', 'NAME', 'MAJOR']

		return self.get_db_info(table, columns)
	
	def get_group_info(self):
		table = 'group_table'
		columns = ['GID', 'CREATOR', 'CRN', 'LOCATION', 'GSIZE', 'ABOUT']

		return self.get_db_info(table, columns)

	def get_class_info(self):
		table = 'class_table'
		columns = ['CRN', 'NAME']

		return self.get_db_info(table, columns)

	def get_location_info(self):
		table = 'location_table'
		columns = ['NAME', 'CAPACITY', 'XCOORDINATE', 'YCOORDINATE']

		return self.get_db_info(table, columns)

	def set_user_info(self, netid, columns, values):
		table_info = self.get_user_info()
		table = 'user_table'

		self.set_info(table, table_info, 'NETID', netid, columns, values)

	def set_group_info(self, gid, columns, values):
		table_info = self.get_group_info()
		table = 'group_table'

		self.set_info(table, table_info, 'GID', gid, columns, values)

	def set_info(self, table, table_info, key, key_value, columns, values):
		isNew = key_value not in table_info[key]

		if isNew:
		    print(isNew)
		    print(key)
		    print(key_value)
		    self.set_db_info(table, [key] + columns, [key_value] + values)
		else:
		    self.update_db_info(table, key, key_value, columns, values)
		
	#def get_group_info(gid, creator, crn, location, gsize):

	def get_db_info(self, table, columns):

		# assemble column str
		column_str = ','.join(columns)

		# assemble query
		query = ''
		query += ' '.join(['SELECT', column_str, 'FROM', table]) + ';'

		return self._execute_query(query, columns)

	def set_db_info(self, table, columns, values):
		# correct values
		new_values = []
		for value in values:
			if  value.isdigit():
				new_values.append(value)
			else:
				new_values.append('\"' + value + '\"')

		# assemble column str and value str
		column_str = '(' + ','.join(list(columns)) + ')'
		value_str = '(' + ','.join(list(new_values)) + ')'

		# assemble query
		query = ''
		query += ' '.join(['insert into', table, column_str, \
				    'values', value_str]) + ';'

		return self._execute_query(query, columns)

	def update_db_info(self, table, key, key_value, columns, values):
		# correct values
		new_values = []
		for value in values:
			if  value.isdigit():
				new_values.append(value)
			else:
				new_values.append('\"' + value + '\"')

		# correct key_value
		if not key_value.isdigit():
		    key_value = '\"' + key_value + '\"'

		# assemble column str and value str
		column_str = '(' + ','.join(list(columns)) + ')'
		value_str = '(' + ','.join(list(new_values)) + ')'

		update_str = ','.join([col + ' = ' + val for col, val in zip(columns, new_values)])
		equal_str = key + ' = ' + key_value

		# assemble query
		query = ''
		query += ' '.join(['update', table, 'set', update_str, \
				    'where', equal_str]) + ';'

		print(query) 
		return self._execute_query(query, columns)


	def _execute_query(self, query, columns):

		# connect and execute query
		connection, cursor = self._connect()
		rows = []

		try:
			print(query)
			cursor.execute(query)
			rows = cursor.fetchall()
			connection.commit()
		except Exception:
                        pass

		connection.close()

		# construct JSON result dict
		result = {}

		for column in columns:
			result[column] = []

		for row in rows:
			for i, column in enumerate(columns):
				result[column].append(row[i])

		return result

class HelloHandler(tornado.web.RequestHandler):
	def get(self):
		self.write("Hello, World")

class userHandler(tornado.web.RequestHandler):
	def get(self):
		response = db.get_user_info()
		print(json.dumps(response))
		self.write(json.dumps(response))

		'''
	def post(self, _): #method to add
		netids.append(json.loads(self.request.body))
		self.write({'message': 'new item added'})
	def delete(self, id):
		global netids
		new_netids = [netid for netid in netids if netid['id'] is not id]
		netids = new_netids
		self.write({'message': 'Item with id %s was deleted' % id})
		'''

class netidHandler(tornado.web.RequestHandler):
	'''
	def get(self):
		name = self.get_arguments('NAME')
		major = self.get_arguments('MAJOR')
		response = {'NAME': name, 'NETID': netid, 'MAJOR': major}
		self.write(response)
	'''
	# insert or update a student
	def put(self, netid = None):
		if not netid:
			raise

		payload = self.request.body
		columns = []
		values = []

		if(payload):
		    data = json.loads(self.request.body)
		    columns = list(data.keys()) if data else None
		    values = [data[column] for column in columns] if columns else None

		response = db.set_user_info(netid, columns, values)
		self.write(json.dumps(response))

class locationsHandler(tornado.web.RequestHandler):
	# get all locations
	def get(self):
		response = db.get_location_info()
		print(json.dumps(response))
		self.write(json.dumps(response))

class locationNameHandler(tornado.web.RequestHandler):
	def get(self):
		name = self.get_arguments('NAME')
		capacity = self.get_arguments('CAPACITY')
		xCoord = self.get_arguments('XCOORDINATE')
		yCoord = self.get_arguments('YCOORDINATE')
		response = {'NAME': name, 'CAPACITY': capacity, 'XCOORDINATE': xCoord, 'YCOORDINATE': yCoord}
		self.write(response)

class groupsHandler(tornado.web.RequestHandler):
	# get all groups
	def get(self):
		response = db.get_group_info()
		print(json.dumps(response))
		self.write(json.dumps(response))

# def put(self):
class groupIDHandler(tornado.web.RequestHandler):
	def put(self, gid = None):
		if not gid:
			raise

		payload = self.request.body
		columns = []
		values = []

		if(payload):
		    data = json.loads(self.request.body)
		    columns = list(data.keys()) if data else None
		    values = [data[column] for column in columns] if columns else None

		response = db.set_group_info(netid, columns, values)
		self.write(json.dumps(response))
		

class classHandler(tornado.web.RequestHandler):
	# get all classes
	def get(self):
		response = db.get_class_info()
		print(json.dumps(response))
		self.write(json.dumps(response))

class crnHandler(tornado.web.RequestHandler):
	def get(self):
		classes = self.get_arguments('CLASS')
		crn = self.get_arguments('CRN')
		response = {'CLASS':classes, 'CRN': crn}
		self.write(response)

#Application		

Application = tornado.web.Application([
	(r'/', HelloHandler),
	(r'/users', userHandler),
	(r'/users/?(.*)', netidHandler),
	(r'/locations', locationsHandler),
	(r'/locations/name', locationNameHandler),
	(r'/groups', groupsHandler),
	(r'/groups/gid', groupIDHandler),
	(r'/classes', classHandler)
])

# set port based on cmd arg
if len(sys.argv) > 1:
	PORT = sys.argv[1]

db = Database()

# bind socket
Application.listen(PORT)

# Main Execution
# start server
tornado.options.parse_command_line()
tornado.ioloop.IOLoop.current().start()
