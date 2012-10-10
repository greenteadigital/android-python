#!/usr/bin/env python
# Dump the EVO frame buffer with:
#			head -c 1536000 /dev/graphics/fb0 > /mnt/sdcard/fb0.raw

import os, struct

header = ''

def buildHdr():
	global header
	# pasted this in from hex editor with BMP header file open
	hexhdr = " 42 4D 36 70 17 00 00 00 00 00 36 00 00 00 28 00 00 00 E0 01 00 00 20 03 00 00 01 00 20 00 00 00 00 00 00 70 17 00 13 0B 00 00 13 0B 00 00 00 00 00 00 00 00 00 00"
	hdrlist = hexhdr.replace(" "," 0x").split(" ")	#build a list of strings repr. hex numbers
	del hdrlist[0]  #del zero length member at beginning
	ints=[]
	# Turn the strings in hdrlist[] which represent hexadecimal numbers into decimal integers
	# Useful/necessary for struct.pack()
	# i.e. string '0x42' becomes integer 66
	for n in range(len(hdrlist)):
		ints.append( int(hdrlist[n],16) )	# declares the strings to hold base 16 nums
	for n in range(len(ints)):
		next = struct.pack("<B", ints[n])
		header = header + next
buildHdr()
dest = "/home/ben/Desktop/bmp/"
if len(os.listdir(dest)) > 0:
	os.system("rm %s*"%dest)	#clear out old bmp's

src = "/home/ben/Desktop/fb"
frames = os.listdir(src)
frames.sort()

j = 0
while j < len(frames):
	fb=open("%s/%s"%(src, frames[j]) ,"rb").read()
	byte_count = 0
	temp = []			# never holds more than 4 bytes at a time
	middle = []		# intermediate container, ea. member is 4 bytes long

	# Reverse bytes 1 and 3 in each 4 byte sequence
	# this corrects for the discrepancy where the frame buffer stores values as RGBA
	# but BMP requires it in BGR* format
	while byte_count < len(fb):
		temp.append( fb[byte_count] )
		temp.append( fb[byte_count+1] )
		temp.append( fb[byte_count+2] )
		temp.reverse()
		temp.append( fb[byte_count+3] )
		byte_count += 4
		middle.append( temp[0]+temp[1]+temp[2]+temp[3] )
		temp = []

		
	scanlines = []	#for holding scan lines, ea. member 480 DWORDs long
	lines_built = 0
	while lines_built < 800:	# 800 scanlines in height
		chunk = ''
		for n in range(480):	# 480 px wide
			chunk = chunk + (middle [ (lines_built * 480) + n] )
		scanlines.append(chunk)
		#chunk = ''
		lines_built += 1

	scanlines.reverse()		# bmp stores scanlines upside down, so flip it vertically
	scanlines.insert(0, header)	#stick header in at the top
	file2=open("/home/ben/Desktop/bmp/%s.bmp"% (j+1000),"wb").writelines(scanlines)
	j += 1

bmps = os.listdir(dest)
bmps.sort()
jpg = "/home/ben/Desktop/jpg/"

if len(os.listdir(jpg)) > 0:
	os.system("rm %s*"%jpg)

for n in range(len(bmps)):
	os.system("convert %s%s %s%s.jpg"%(dest, bmps[n] , jpg, n+1000))

#include '-vf-add rotate=2' in the following mencoder call to rotate for landscape capture: 
os.system("mencoder \"mf:///home/ben/Desktop/jpg/*.jpg\" -mf fps=2 -o /home/ben/Desktop/test.avi -ovc lavc -lavcopts vcodec=mpeg4:vbitrate=800")
os.system("ffmpeg -r 3 -i /home/ben/Desktop/test.avi -vcodec h264 /home/ben/Desktop/screenvid.mp4")
os.system("vlc /home/ben/Desktop/screenvid.mp4")
