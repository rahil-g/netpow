#!/usr/bin/python
#Author: Rahil Gandotra

def change(nd,pwr,traff,delay,loss):
	fname = 'eopower'+str(nd)+'.snmprec'
	with open(fname, 'r') as file:
                data = file.readlines()
	newline1 = '1.3.6.1.2.1.229.1.2.1.1.1|4|'+str(pwr)+'\n'
	newline2 = '1.2.3.4.5.6.7.8.9|4|'+str(traff)+'\n'
	newline3 = '1.8.7.6.5.4.3.2.1|4|'+str(delay)+'\n'
	newline4 = '1.9.2.8.3.7.4.6.5|4|'+str(loss)+'\n'
	data[1] = newline1
	data[3] = newline2
	data[4] = newline3
	data[5] = newline4
	with open(fname,'w') as file:
                file.writelines(data)

if __name__ == "__main__":
        change(1,50,1000,1000,10)
        change(2,51,10000,100,1)
        change(3,100,100000,10,0)
        input("Press Enter to continue...")
        change(1,50,1000,100,1)
        change(2,90,9999,11,0.1)
        change(3,100,10000,10,0)
        input("Press Enter to continue...")
        change(1,50,1000,1000,10)
        change(2,75,10000,100,1)
        change(3,125,50000,10,0)
