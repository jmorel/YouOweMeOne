import cherrypy
from mako.template import Template
#import sqlite3 as sqlite
from pysqlite2 import dbapi2 as sqlite
from math import sqrt

def isNumber(source):
	res = False
	try:
		n = str(float(source)) # if that doesn't do an error, then we're ok
		res = True
	except:
		# not an integere
		res = False
	return res

def isCreditor(con, creditorID):
	cursor = con.cursor()
	query = "SELECT count(*) FROM Creditor WHERE id=?"
	res = cursor.execute(query, (creditorID, ))
	n = int(res.fetchone()[0])
	if n > 0:
		return True
	else:
		return False

def doesCreditorExists(con, creditorName):
	cursor = con.cursor()
	query = "SELECT count(*) FROM Creditor WHERE name=?"
	res = cursor.execute(query, (creditorName, ))
	n = int(res.fetchone()[0])
	if n > 0:
		return True
	else:
		return False

def isDebitor(con, debitorID):
	cursor = con.cursor()
	query = "SELECT count(*) FROM Debitor WHERE id=?"
	res = cursor.execute(query, (debitorID, ))
	n = int(res.fetchone()[0])
	if n > 0:
		return True
	else:
		return False

def isValidString(source):
	res = True
	validChars = "abcdefghijklmnopqrstuvwxyz0123456789.-_ !"
	for c in source.lower():
		if c not in validChars:
			res = False
			break
	return res

class Beer:
	
	@cherrypy.expose
	def default(self, creditor=None):
		if creditor:
			con = sqlite.connect('beer.db')
			if not con:
				return "no connexion to DB"
			cursor = con.cursor()
			# check that user does exist
			query = "SELECT count(*) FROM creditor WHERE name=?"
			res = cursor.execute(query, (creditor, ))
			n = int(cursor.fetchone()[0])
			if n == 1:
				# get creditor
				query = "SELECT id, name FROM creditor WHERE name=?"
				res = cursor.execute(query, (creditor,) )
				row = res.fetchone()
				creditorID = int(row[0])
				creditorName = row[1]
				# get debitors
				query = "SELECT id, name, amount FROM debitor WHERE creditor=? ORDER BY id ASC"
				res = cursor.execute(query, (creditorID, ))
				debitors = []
				for row in res.fetchall():
					debitors.append({'id': int(row[0]), 'name': row[1], 'amount': row[2]})
				# close connexion
				con.close()
				# generate page
				template = Template(filename='perso.html', output_encoding='utf-8', encoding_errors='replace')
				page = template.render(
					creditorID = creditorID,
					creditorName = creditorName,
					debitors = debitors )
				# display page
				return page

		# default page, with the formular to create a new user
		# generate page
		template = Template(filename='index.html', output_encoding='utf-8', encoding_errors='replace')
		page = template.render()
		# display page
		return page
	
	@cherrypy.expose
	def deleteDebitor(self, debitorID, creditorID):
		# open connexion to DB
		con = sqlite.connect('beer.db')
		if not con:
			return "no connexion to DB"
		if isDebitor(con, debitorID) and isCreditor(con, creditorID):
			cursor = con.cursor()
			query = "DELETE FROM debitor WHERE id=? AND creditor=?"
			cursor.execute(query, (debitorID, creditorID))
			con.commit()
			con.close()
			return 'ok'
		else:
			con.close()
			return 'no'
	
	@cherrypy.expose
	def editDebitor(self, debitorID, creditorID, amount):
		# open connexion to DB
		con = sqlite.connect('beer.db')
		if not con:
			return "no connexion to DB"
		cursor = con.cursor()
		# check data
		if isNumber(amount) and isDebitor(con, debitorID) and isCreditor(con, creditorID):
			query = "UPDATE debitor SET amount=? WHERE id=? AND creditor=?"
			cursor.execute(query, (amount, debitorID, creditorID))
			con.commit()	
			con.close()
			return 'ok'
		else:
			con.close()
			return 'no'
	
	@cherrypy.expose
	def addDebitor(self, creditorID, debitorName, amount):
		# open connexion to DB
		con = sqlite.connect('beer.db')
		if not con:
			return "no connexion to DB"
		# convert data to standard
		debitorName = debitorName.decode('utf-8')
		amount = amount.decode('utf-8')
		# check data
		if isNumber(amount) and isCreditor(con, creditorID) and isValidString(debitorName):
			cursor = con.cursor()
			# insert data
			query = "INSERT INTO debitor(creditor, name, amount) VALUES (?,?,?)"
			cursor.execute(query, (creditorID, debitorName, amount))
			query = "SELECT last_insert_rowid()"
			res = cursor.execute(query)
			id = int(res.fetchone()[0])
			con.commit()
			con.close()
			return str(id)
		else:
			con.close()
			return 'no'
	
	@cherrypy.expose
	def addCreditor(self, creditorName):
		# error codes:
		# 1: name already taken
		# 2: invalid chars
		
		# open connexion to DB
		con = sqlite.connect('beer.db')
		if not con:
			return "no connexion to DB"
		# check chars
		creditorName = creditorName.decode('utf-8')
		if not isValidString(creditorName):
			con.close()
			return '2'
		cursor = con.cursor()
		# check that that user does not already exists
		#query = "SELECT count(*) FROM creditor WHERE name=?"
		#res = cursor.execute(query, (creditorName, ))
		#n = int(res.fetchone()[0])
		#if n!=0:
		#	con.close()
		#	return '1'
		if doesCreditorExists(con, creditorName):
			con.close()
			return '1'		
		# the user can now be created
		query = "INSERT INTO creditor(name) VALUES(?)"
		cursor.execute(query, (creditorName, ))
		con.commit()
		con.close()
		return '0'

	@cherrypy.expose
	def stats(self):
		# open connexion to DB
		con = sqlite.connect('beer.db')
		if not con:
			return "no connexion to DB"
		cursor = con.cursor()
		
		query = "SELECT count(*) FROM creditor"
		res = cursor.execute(query)
		people = res.fetchone()[0]
		
		query = "SELECT sum(amount) FROM debitor"
		res = cursor.execute(query)
		total = res.fetchone()[0]
		
		mean = total / people
		
		query = "SELECT sum(amount) FROM debitor GROUP BY creditor"
		res = cursor.execute(query)
		sd = 0
		for row in res.fetchall():
			sd += (row[0]-mean)**2
		sd = sd / people
		sd = sqrt(sd)
		
		template = Template(filename='stats.html', output_encoding='utf-8', encoding_errors='replace')
		page = template.render(
			people = people,
			total = total,
			mean = mean,
			sd = sd)
		# display page
		return page

cherrypy.config.update({
    'environment': 'production',
    #'log.screen': True,
    'server.socket_host': '127.0.0.1',
    'server.socket_port': 14902,
})

local_conf ={ '/beer.css': {
			'tools.staticfile.on' : True,
			'tools.staticfile.filename' : '/local/path/beer.css'},
		'/beer.js': {
			'tools.staticfile.on' : True,
			'tools.staticfile.filename' : '/local/path/beer.js'},
		'/jquery.js': {
			'tools.staticfile.on' : True,
			'tools.staticfile.filename' : '/local/path/jquery.js'},
		'/beer.png': {
			'tools.staticfile.on' : True,
			'tools.staticfile.filename' : '/local/path/beer.png'},
		'/title.png': {
			'tools.staticfile.on' : True,
			'tools.staticfile.filename' : '/local/path/title.png'},
		'/buzz.png': {
			'tools.staticfile.on' : True,
			'tools.staticfile.filename' : '/local/path/buzz.png'},
		'/favicon.png': {
			'tools.staticfile.on' : True,
			'tools.staticfile.filename' : '/local/path/favicon.png'}}
			

conf ={ '/beer.css': {
			'tools.staticfile.on' : True,
			'tools.staticfile.filename' : '/server/path/youowemeone/beer.css'},
		'/beer.js': {
			'tools.staticfile.on' : True,
			'tools.staticfile.filename' : '/server/path/youowemeone/beer.js'},
		'/jquery.js': {
			'tools.staticfile.on' : True,
			'tools.staticfile.filename' : '/server/path/youowemeone/jquery.js'},
		'/beer.png': {
			'tools.staticfile.on' : True,
			'tools.staticfile.filename' : '/server/path/youowemeone/beer.png'},
		'/title.png': {
			'tools.staticfile.on' : True,
			'tools.staticfile.filename' : '/server/path/youowemeone/title.png'},
		'/buzz.png': {
			'tools.staticfile.on' : True,
			'tools.staticfile.filename' : '/server/path/youowemeone/buzz.png'},
		'/favicon.png': {
			'tools.staticfile.on' : True,
			'tools.staticfile.filename' : '/server/path/youowemeone/favicon.png'}}

cherrypy.quickstart(Beer(), config=conf)
