#! /opt/python262/python
import os, zipfile, ftplib

src = "/home/ben/Desktop/frames.zip"
dest = "/home/ben/Desktop/fb"

ftp = ftplib.FTP()
ftp.connect("192.168.1.7","2110")
ftp.login("ben","hunter2") #lol
ftp.retrbinary('RETR frames.zip', open(src, 'wb').write)
ftp.quit()

full = os.listdir(dest)
if len(full) > 0:
	os.system("rm %s/*"%dest)		#clear out dest. dir., need empty workspace
zf = zipfile.ZipFile(src,'r')
zf.extractall(dest)
full = os.listdir(dest)

# a development artifact of unknown utility, leaving it for posterity ;)
'''
n=0
while n < len(full):
	os.system("head -c 3072000 %s/%s > %s/%s-clean"%(dest, full[n], dest, full[n]))
	os.system("rm %s/%s"%(dest, full[n]))
	n+=1
clean=os.listdir(dest)
k=0
while k < len(clean):
	os.system("head -c 1536000 %s/%s > %s/%s-A"%(dest, clean[k], dest, clean[k]))
	os.system("tail -c 1536000 %s/%s > %s/%s-B"%(dest, clean[k], dest, clean[k]))
	os.system("rm %s/%s"%(dest, clean[k]))
	k+=1
'''