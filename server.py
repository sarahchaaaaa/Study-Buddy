#!/usr/bin/env python3

import tornado.ioloop
import tornado.options
import tornado.web
import sys
import sqlite3

# Constants

PORT = 9800

# Handlers

netids = []

class HelloHandler(tornado.web.RequestHandler):
	def get(self):
		self.write("Hello, World")

class userHandler(tornado.web.RequestHandler):
	def get(self):
		netid = self.get_arguments('NETID')
		response = {'NETID': netids}
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

Application.listen(PORT)

# Main Execution
#PORT = sys.argv[1]
tornado.options.parse_command_line()
tornado.ioloop.IOLoop.current().start()
