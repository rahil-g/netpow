#!/usr/bin/python3
#Author: Rahil Gandotra
#Python script to dynamically modify power/network performance parameters in the simulated SNMP agents.

import random
import threading
import time

pwr_cons1 = ['102.85','103.02','103.19','102.90','103.03','103.21','102.91','103.03','103.09','102.95','103.08','103.14']
pwr_cons2 = ['40.53','40.58','40.65','40.58','40.63','40.69']
pwr_cons3 = ['93.52','93.62','93.55','93.63','93.52','93.63','93.55','93.66','93.11','93.25','93.29','93.37','93.23','93.35','93.39','93.43','93.41','93.42','93.15','93.28','93.33','93.41','93.26','93.37','93.43','93.47','93.44','93.46']
bw = ['1000','10000','100000','9999','50000']
delay = ['1000', '100', '10', '11']
loss = ['10','1','0','0.1']

def modify(nd):
	fname = 'eopower'+str(nd)+'.snmprec'
	if nd == 1:
		pwr_cons = pwr_cons1
	elif nd == 2:
		pwr_cons = pwr_cons2
	elif nd == 3:
		pwr_cons = pwr_cons3
	with open(fname, 'r') as file:
		data = file.readlines()
	newline1 = '1.3.6.1.2.1.229.1.2.1.1.1|4|' + random.choice(pwr_cons)+'\n'
	data[1] = newline1
	newline3 = '1.2.3.4.5.6.7.8.9|4|' + random.choice(bw) + '\n'
	data[3] = newline3
	newline4 = '1.8.7.6.5.4.3.2.1|4|' + random.choice(delay) + '\n'
	data[4] = newline4
	newline5 = '1.9.2.8.3.7.4.6.5|4|' + random.choice(loss)
	data[5] = newline5
	print (data)
	with open(fname,'w') as file:
		file.writelines(data)

if __name__ == "__main__":
	while True:
		nd = 1
		while (nd <= 3):
			x = threading.Thread(target=modify, args=(nd,))
			x.start()
			nd += 1
		time.sleep(5)
