#!/usr/bin/python3
#Author:Rahil Gandotra
#Python script to initialize REST endpoints to provide the power information in an abstracted manner.

from flask import Flask
from flask_restful import Resource, Api
import sqlite3

db = 'powerinfo.sql3'

app = Flask(__name__)
api = Api(app)

class Root(Resource):
	def get(self):
		cmd = 'REST endpoints present at: EMS-IP:5002/devices, and EMS-IP:5002/devices/<endpoint>'
		return (cmd)

class Devices(Resource):
    def get(self):
        con = sqlite3.connect(db)
        cursorObj = con.cursor()
        cursorObj.execute('SELECT * FROM devices')
        rows = cursorObj.fetchall()
        for row in rows:
            print(row)
        cursorObj.close()
        con.close()
        return (rows)

class Devices_Individual(Resource):
    def get(self, endpoint):
        con = sqlite3.connect(db)
        cursorObj = con.cursor()        
        cursorObj.execute("select * from devices where endpoint = ?", (str(endpoint),))
        rows = cursorObj.fetchall()
        return (rows)

class Test(Resource):
    def get(self):
        cmd = 'Test'
        return (cmd)

api.add_resource(Root, '/') # Root Route
api.add_resource(Devices, '/devices') # Route_1
api.add_resource(Devices_Individual, '/devices/<endpoint>') # Route_2
api.add_resource(Test, '/test')


if __name__ == '__main__':
     app.run(host='0.0.0.0',port='5002')
