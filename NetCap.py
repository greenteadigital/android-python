# A packet capture script. Requires root and the tcpdump binary at /system/xbin/

import os
import android
import datetime
import time
import subprocess

droid = android.Android()
now = ''

def sudo(command):
	global pipe, std_out
	pipe = subprocess.Popen(['su','-c','/system/bin/sh'], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
	std_out = pipe.communicate(input=command)	#use 'std_out[0]' as shell response
	#print std_out[0]

def getNow():
	global now
	now = str(datetime.datetime.now())
	now = now .replace(':','-')
	now = now .replace(' ','t=')
	now = now[0:-7]

def setName():
	global now, droid
	
	getNow()
	ifaces = sudo('/system/xbin/tcpdump -D > /sdcard/pcap/tmp.txt')
	file1 = open('/sdcard/pcap/tmp.txt','r').readlines()
	op_iface = file1[0].split('.')[1]
	name = droid.dialogGetInput('Filename', 'Name for capture file:', now )

	if name[1] != None:
		droid.dialogCreateAlert('Capturing on %s'%op_iface, None)
		droid.dialogShow()
		full_name = '%s.%s'%(name[1],op_iface)
		sudo('/system/xbin/tcpdump -s0 -w /sdcard/pcap/%s'%full_name)
		
	elif name[1] == None:
		droid.dialogCreateAlert('Filename Required','Filename may not be \'None\'')
		droid.dialogShow()
		time.sleep(2)
		droid.dialogDismiss()
		name = now = ''
		setName()

setName()