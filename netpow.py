#!/usr/bin/python3
#Author: Rahil Gandotra

import subprocess
import csv
import threading
import time
import datetime
import sqlite3
from prettytable import PrettyTable

def discover(fname):
	with open(fname) as csv_file:
		reader = csv.reader(csv_file, delimiter=',')
		for row in reader:
			devices.append({'ip':str(row[0]), 'port':str(row[1]), 'snmpver':str(row[2]), 'seclev':str(row[3]), 'authprot':str(row[4]), 'authpass':str(row[5]), 'secname':str(row[6]), 'privprot':str(row[7]), 'privpass':str(row[8])})
	print (len(devices),'device(s) discovered from SNMP-NSOT file.')
	return devices

def snmp(device,nd):
	device_endpoint = device['ip']+":"+device['port']
	values = []
	values.append(device_endpoint)
	Table = PrettyTable()
	Table.field_names = ["Key", "Value"]
	Table.align["Key"] = "l"
	Table.align["Value"] = "l"
	Table.add_row(['2 Device Endpoint',device_endpoint])
	contextl = {'entity': ['1.3.6.1.2.1.47.1.1.1.1.2.1'], 'eopower':['1.3.6.1.2.1.229.1.1.1.1.1', '1.3.6.1.2.1.229.1.2.1.1.1', '1.3.6.1.2.1.229.1.2.1.3.1', '1.2.3.4.5.6.7.8.9','1.8.7.6.5.4.3.2.1','1.9.2.8.3.7.4.6.5']}
	for i in contextl:
		if i == 'entity':
			cntxt = i+str(nd)
			oids = contextl[i]
			for o in oids:
				cmd = ['snmpget', '-v', device['snmpver'], '-l', device['seclev'], '-a', device['authprot'], '-A', device['authpass'], '-n', cntxt, '-u',device['secname'], '-x', device['privprot'], '-X', device['privpass'], device_endpoint,o]
				returned_output = subprocess.check_output(cmd).decode("utf8")
				returned_output = returned_output.split(':')[1]
				returned_output = returned_output.replace(' ','')
				returned_output = returned_output.replace('\"','')
				returned_output = returned_output.replace('\n','')
				dname = returned_output
				if o == '1.3.6.1.2.1.47.1.1.1.1.2.1':
					TKey = '1 Device Name'
				Table.add_row([TKey,returned_output])
		elif i =='eopower':
			oids = contextl[i]
			cntxt = i+str(nd)
			for o in oids:
				cmd = ['snmpget', '-v', device['snmpver'], '-l', device['seclev'], '-a', device['authprot'], '-A', device['authpass'], '-n', cntxt, '-u',device['secname'], '-x', device['privprot'], '-X', device['privpass'], device_endpoint,o]
				returned_output = subprocess.check_output(cmd).decode("utf8")
				returned_output = returned_output.split(':')[1]
				returned_output = returned_output.replace(' ','')
				returned_output = returned_output.replace('\"','')
				returned_output = returned_output.replace('\n','')
				if o == '1.3.6.1.2.1.229.1.1.1.1.1':
					TKey = '3 Power monitoring capability'
					if int(returned_output) >= 4:
						TVal = True
					else:
						TVal = False
					Table.add_row([TKey,TVal])
				elif o == '1.3.6.1.2.1.229.1.2.1.1.1':
					TKey = '4 Power in Watts'
					Table.add_row([TKey,returned_output])
					dpower = returned_output
					if float(returned_output) > 0:
						Table.add_row(['6 Direction of power','Consumer of power'])
						ddire = 'consumer'
					else:
						Table.add_row(['6 Direction of power','Producer of power'])
						ddire = 'producer'
				elif o == '1.3.6.1.2.1.229.1.2.1.3.1':
					TKey = '5 Power Unit Multiplier'
					dum = returned_output
					Table.add_row([TKey,returned_output])
				elif o == '1.2.3.4.5.6.7.8.9':
					TKey = '6 Traffic in Mbps'
					dtraf = returned_output
					Table.add_row([TKey,returned_output])

				elif o == '1.8.7.6.5.4.3.2.1':
					TKey = '7 Delay in ms'
					ddelay = returned_output
					Table.add_row([TKey,returned_output])

				elif o == '1.9.2.8.3.7.4.6.5':
                                        TKey = '7 Loss in %'
                                        dloss = returned_output
                                        Table.add_row([TKey,returned_output])
	
	Table.sortby = "Key"
	print (Table)
	
	values.append(dname)
	values.append(dpower)
	values.append(dum)
	values.append(ddire)
	values.append(dtraf)
	values.append(ddelay)
	values.append(dloss)
	db = 'powerinfo.sql3'
	con = sqlite3.connect(db)
	cursorObj = con.cursor()
	cursorObj.execute("SELECT rowid FROM devices WHERE endpoint = ?", (values[0],))
	data=cursorObj.fetchone()
	if data is None:
		cursorObj.execute('''INSERT INTO devices(endpoint, name, power, unitmultiplier, direction, traffic, delay, loss) VALUES(?, ?, ?, ?, ?, ?, ?, ?)''', values)
	else:
		newvalues = (dpower, dtraf, ddelay, dloss, device_endpoint)
		cursorObj.execute("""Update devices set power = ?, traffic = ?, delay = ?, loss = ? where endpoint = ?""",newvalues)
	con.commit()
	cursorObj.close()
	con.close()

if __name__ == "__main__":
	
	#Discover device from SNMP-NSOT file.
	devices = []
	devices = discover('SNMP-NSOT.csv')
	
	#Create database and table to store and retrieve power information.
	db = 'powerinfo.sql3'
	con = sqlite3.connect(db)
	cursorObj = con.cursor()
	cursorObj.execute(''' SELECT count(name) FROM sqlite_master WHERE type='table' AND name='devices' ''')
	if cursorObj.fetchone()[0]==1 : 
   		pass
	else:
		cursorObj.execute("CREATE TABLE devices(endpoint text PRIMARY KEY, name text, power text, unitmultiplier real, direction text, traffic text, delay text, loss text)")
		con.commit()
	cursorObj.close()
	con.close()
	
	#Start realtime monitoring of devices.
	while True:
		nd = 1
		print ('\n'+str(datetime.datetime.now()))
		for i in devices:
			x = threading.Thread(target=snmp, args=(i,nd))
			x.start()
			nd+=1
		time.sleep(6)
