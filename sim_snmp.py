#!/usr/bin/python3
#Author:Rahil Gandotra
#Python script to simulate SNMP agents using custom data files.

import argparse
import os
import sys

def conf_snmp(num,ddir):
    i = 1
    cmd = 'snmpsimd.py '
    while (i <= num):
        cmd += '--agent-udpv4-endpoint=127.0.0.1:'+str(1023+i)+' '
        i += 1
    cmd += '--data-dir='+ddir
    os.system(cmd)
    
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("num", help="number of SNMP agents to be simulated", type=int)
    parser.add_argument("--dir", help="location of data directory with SNMP agents config files [default: ./data]", type=str, default=os.path.join(os.getcwd(),'data'))
    args = parser.parse_args()
    num_agents = args.num
    if (num_agents < 1):
        print('Invalid number of agents. Terminating...')
        sys.exit()
    data_dir = args.dir
    i = 1
    while (i <= num_agents):
        entity_fname = "entity"+str(i)+".snmprec"
        eopower_fname = "eopower"+str(i)+".snmprec"
        if (not os.path.exists(os.path.join(data_dir,entity_fname))) or (not os.path.exists(os.path.join(data_dir,eopower_fname))):
            print('Required entity/eopower file does not exist. Terminating...')
            sys.exit()
        i += 1
    conf_snmp(num_agents, data_dir)

