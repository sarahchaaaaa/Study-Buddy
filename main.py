#!/usr/bin/env python3

import tornado.ioloop
import tornado.options
import tornado.web
import sys
import sqlite3

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

	# get column info of user_table
	def get_user_info(self, netid='', name='', major=''):
		columns_l = ['NETID', 'NAME', 'MAJOR']
		column_str = columns.join(',')

		# assemble where str
		'''
		where_l = []
		part_str = ''
		if(netid):
			part_str = ''
			where_l.append('NETID')

		if(name):
			part_str = ''
			where_l.append()
		
		if(major):
			part_str = ''
			where_l.append('NAME')
		where_str = where_l.join(' and ')
		'''

		# assemble query
		query = ''
		table_str = 'user_table'
		query += ['SELECT', column_str, 'FROM', table_str].join(' ') + ';'

		# connect and execute query
		connection, cursor = self._connect()
		rows = []

		try:
			cursor.execute(query)
			rows = cursor.fetchall()
			connection.commit()
		except Exception:
			raise

		connection.close()
		print(rows)
 
		
	#def get_group_info(gid, creator, crn, location, gsize):


class HelloHandler(tornado.web.RequestHandler):
	def get(self):
		self.write("Hello, World")

class userHandler(tornado.web.RequestHandler):
	def get(self):
		netid = self.get_arguments('NETID')
		response = {'NETID': netid}
                print(getting database info)
		Database.get_user_info()
		self.write(response)
	def post(self, _): #method to add
		netids.append(json.loads(self.request.body))
		self.write({'message': 'new item added'})
	def delete(self, id):
		global netids
		new_netids = [netid for netid in netids if netid['id'] is not id]
		netids = new_netids
		self.write({'message': 'Item with id %s was deleted' % id})

class netidHandler(tornado.web.RequestHandler):
	def get(self):
		name = self.get_arguments('NAME')
		major = self.get_arguments('MAJOR')
		response = {'NAME': name, 'NETID': netid, 'MAJOR': major}
		self.write(response)
#	def put(self):

class locationsHandler(tornado.web.RequestHandler):
	def get(self):
		locations = self.get_arguments('NAME')
		response = {'NAME': locations}
		self.write(response)

class locationNameHandler(tornado.web.RequestHandler):
	def get(self):
		name = self.get_arguments('NAME')
		capacity = self.get_arguments('CAPACITY')
		xCoord = self.get_arguments('XCOORDINATE')
		yCoord = self.get_arguments('YCOORDINATE')
		response = {'NAME': name, 'CAPACITY': capacity, 'XCOORDINATE': xCoord, 'YCOORDINATE': yCoord}
		self.write(response)

class groupsHandler(tornado.web.RequestHandler):
	def get(self):
		gName = self.get_arguments('GID')
		response = {'GID': gName}
		self.write(response) 

# def put(self):
class groupNameHandler(tornado.web.RequestHandler):
	def get(self):
		gName = self.get_arguments('NAME')
		creator = self.get_arguments('CREATOR')
		crn = self.get_arguments('CRN')
		size = self.get_arguments('SIZE')
		about = self.get_arguments('ABOUT')
		response = {'NAME': gName, 'CREATOR':creator, 'CRN':crn, 'SIZE':size, 'ABOUT': about}
		self.write(response)

class classHandler(tornado.web.RequestHandler):
	def get(self):
		classes = self.get_arguments('CLASS')
		response = {'CLASS':classes}
		self.write(response)

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
	(r'/users/netid', netidHandler),
	(r'/locations', locationsHandler),
	(r'/locations/name', locationNameHandler),
	(r'/groups', groupsHandler),
	(r'/groups/gid', groupNameHandler),
])

# set port based on cmd arg
if len(sys.argv) > 1:
	PORT = sys.argv[1]

# bind socket
Application.listen(PORT)

# Main Execution
# start server
tornado.options.parse_command_line()
tornado.ioloop.IOLoop.current().start()
