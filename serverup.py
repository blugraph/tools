import netifaces as ni
import time
import requests
import json
import os
import subprocess
import re
import shutil



WPA_DIR="/etc/wpa_supplicant"
WPA_FILE="wpa_supplicant.conf"
#IDLINE="SVCSENSOR"
IDLINE="NUS"
stID="P1001"
#IDLINE="BGWIFI"
#IDLINE="BluSense"
STATUS_URL="http://52.74.191.39/blupower/getstatus.php"
WIFI_UPDATE_URL="http://52.74.191.39/blupower/wifiupdate.php"



dev_ID="D1070"
#SERVER_ADDR="http://172.18.53.42:81/BluIEQ/sensorstatus.php""
SERVER_ADDR="http://52.74.191.39/BluIEQ/sensorstatus.php"



payload=[{"stationID":stID}]
#try:
while 1:
  r1 = requests.put(STATUS_URL, json.dumps(payload), timeout=0.1)
  data= json.loads(r1.content)	
  print data
  print data[0]	
  print r1.status_code,": server response."
  print "This is the data"
  dir_name="/etc/wpa_supplicant"		
  base_filename=(time.strftime("%Y-%m-%d_%H_%M_%S")+"." + "bak")
  abs_file_name=os.path.join(dir_name, base_filename)
  curr_file='/etc/wpa_supplicant/wpa_supplicant.conf'
  if data[0]=="Per":
	shutil.copy2(curr_file, abs_file_name) 	
  	f = open('/etc/wpa_supplicant/wpa_supplicant.conf', 'a')
	print f
	f.write("network={\n")
        f.write("\tssid="+"\""+str(data[2])+"\""+"\n")
        f.write("\tpsk="+"\""+str(data[4])+"\""+"\n")
        f.write("\tpriority="+str(data[1])+"\n")
	f.write("}\n")
	f.close()
#	try:    
#                r1 = requests.put(WIFI_UPDATE_URL, json.dumps(payload), timeout=0.1)
#                print r1.content
#        except:
 #               print "Network Connection failure"

  elif data[0]=="Ent":
	shutil.copy2(curr_file, abs_file_name) 
	f = open('/etc/wpa_supplicant/wpa_supplicant.conf', 'a')
        print f
	f.write("network={\n")
	f.write("\tssid="+"\""+str(data[2])+"\""+"\n")
        f.write("\tkey_mgmt=WPA-EAP\n")
        f.write("\teap=PEAP\n")
        f.write("\tidentity="+"\""+str(data[5])+"\""+"\n")
        f.write("\tpassword="+"\""+str(data[4])+"\""+"\n")
        f.write("\tphase2="+"\""+"MSCHAPV2"+"\""+"\n")
	f.write("\tpriority="+str(data[1])+"\n")
        f.write("}\n")
        f.close()
 # 	try:	
#		r1 = requests.put(WIFI_UPDATE_URL, json.dumps(payload), timeout=0.1)
#  		print r1.content
#	except:
#		print "Network Connection failure"	
  else:
	print "Nothing to update"	
  time.sleep(10) 	
#except:
#  print ": Network Failed when getting the WiFI Update"





tofile=[]

from uuid import getnode as get_mac
mac = get_mac()
print hex(mac)
mac = hex(mac)

def findThisProcess( process_name ):
  ps     = subprocess.Popen("ps -eaf | grep "+process_name, shell=True, stdout=subprocess.PIPE)
  output = ps.stdout.read()
  ps.stdout.close()
  ps.wait()

  return output

def isThisRunning( process_name ):
  output = findThisProcess( process_name )

  if re.search('/home/arkbg/dev/'+process_name, output) is None:
    return False
  else:
    return True

if isThisRunning('sense_2.py') == False:
  print("Not running")
  state="Not running"	
else:
  print("Running!")
  state="Running"	


ni.ifaddresses('wlan0')
ip = ni.ifaddresses('wlan0')[2][0]['addr']
print ip 

t = time.strftime("%Y-%m-%d %H:%M:%S")

print t

payload = {"deviceID":dev_ID, "ip": ip,"mac": mac, "status":state, "time":t}
tofile.append(payload)

try:
  r1 = requests.put(SERVER_ADDR, data=json.dumps(tofile), timeout=0.1)
  print t,r1.status_code,": server response."
  del tofile[:]
except:
  print t,": Network Failed while uploading data buffer:"
  del tofile[:]

