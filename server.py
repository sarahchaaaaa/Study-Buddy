#!/usr/bin/env python3

import tornado.ioloop
import tornado.options
import tornado.web
import sys

# Constants

PORT = 9991

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
		name = self.get_arguments('NAME', None)
		major = self.get_arguments('MAJOR', None)
		response = {'NAME': name, 'NETID': netid, 'MAJOR': major}
		self.write(response)
#	def put(self):

class locationsHandler(tornado.web.RequestHandler):
	def get(self):
		locations = self.get_arguments('NAME', None)
		response = {'NAME': locations}
		self.write(response)

class locationNameHandler(tornado.web.RequestHandler):
	def get(self):
		name = self.get_arguments('NAME', None)
		capacity = self.get_arguments('CAPACITY', None)
		xCoord = self.get_arguments('XCOORDINATE', None)
		yCoord = self.get_arguments('YCOORDINATE', None)
		response = {'NAME': name, 'CAPACITY': capacity, 'XCOORDINATE': xCoord, 'YCOORDINATE': yCoord}
		self.write(response)
class groupsHandler(tornado.web.RequestHandler):
	def get(self):
		gName = self.get_arguments('GID', None)
		response = {'GID': gName}
		self.write(response) 
# def put(self):
class groupNameHandler(tornado.web.RequestHandler):
	def get(self):
		gName = self.get_arguments('NAME', None)
#		creator = self.get_arguments('
#		CREATOR CRN SIZE ABOUT'

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
PORT = sys.argv[1]
tornado.options.parse_command_line()
tornado.ioloop.IOLoop.current().start()
