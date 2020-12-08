## Real-time Network Power monitoring (NetPow)
A framework for non-intrusive collection of real-time power consumption information from the next generation of networking hardware by employing information models.

### Quick Start

Tested on OS: Ubuntu 16.04.07 LTS

Required packages:
Python3, 
Pip3
```
$ sudo apt-get update; sudo apt-get install python3-pip -y; sudo -H pip3 install --upgrade pip
```

Install NetPow from the source code -
```
$ git clone https://github.com/rahil-g/netpow.git
$ cd netpow/
```

Install the required Linux packages from the packages.txt file -
```
$ sudo apt-get update ; cat packages.txt | xargs sudo apt-get install -y
```

Next, install the required Python libraries from the requirements.txt file -
```
$ sudo -H pip3 install -r requirements.txt
```

Start the SNMP agents simulation using the sim_snmp.py app -
```
$ python3 sim_snmp.py 3
```
> This step is not required if using network devices that support EMAN MIBs.

More options can be cheked using -h. The sim_snmp.py app simulates SNMP agents based on simulation data stored in .snmprec files in the data/ directory. The simple plain-text files are in the format OID|TYPE|VALUE format.

>The entity<#>.snmprec files are based on the ENTITY MIB defined in [RFC 6933](https://tools.ietf.org/html/rfc6933) and are used to identify the specific device label and its entPhysicalIndex.

```
$ cat data/entity1.snmprec
1.3.6.1.2.1.47.1.1.1.1.2.1|4|Device A       #Device label
```
>The eopower#.snmprec files are based on the EMAN MIB defined in [RFC 7460](https://tools.ietf.org/html/rfc7460) and are used to indicate the power metering capability, current power in Watts, and unit multiplier. Additional customized OIDs are defined to exchange the current bandwidth in Mbps, current delay in ms, and current packet loss in % values.
```
$ cat data/eopower1.snmprec
1.3.6.1.2.1.229.1.1.1.1.1|2|4               #Power metering capability
1.3.6.1.2.1.229.1.2.1.1.1|4|50              #Current power consumption in Watts
1.3.6.1.2.1.229.1.2.1.3.1|2|0               #Unit multiplier
1.2.3.4.5.6.7.8.9|4|1000                    #Current bandwidth in Mbps
1.8.7.6.5.4.3.2.1|4|100                     #Current delay in ms
1.9.2.8.3.7.4.6.5|4|10                      #Current packet loss in %
```

On another terminal, start the NetPow app -
```
$ python3 netpow.py
```
The NetPow app first reads the file SNMP-NSOT.csv to discover the SNMP agents. Therefore, any SNMP config changes would also need to be reflected in the SNMP-NSOT.csv file.
>The format of the file is - IP,Port,SNMP_ver,Security_level,Auth_protocol,Auth_pass,Security_name,Priv_protocol,Priv_pass
```
$ cat SNMP-NSOT.csv
127.0.0.1,1024,3,authPriv,MD5,auctoritas,simulator,DES,privatus
```

On another terminal, start the REST endpoints app -
```
$ python3 REST_endpoint.py
```
Send HTTP requests to the IP:5002, IP:5002/devices, IP:5002/devices/(endpoint) (like - IP:5002/devices/127.0.0.1:1024).

To check the dynamic nature of the NetPow app, on another terminal, navigate to the data/ directory and start the dynamic data app-
```
cd data/
python3 dynamic_data.py
```

## To-do list:
* 

## Status
Project is: in progress.

## Contact
Created by Rahil Gandotra - feel free to contact me!
