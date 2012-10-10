import time, os, zipfile, android
dest = "/mnt/sdcard/frames/"
if len(os.listdir(dest)) > 0:
	os.system("rm %s*"%dest)
	print 'deleted old frames'
time.sleep(5)
n=0
frames = 30
print 'beginning frame capture...'
begin = time.clock()
while n < frames:
	#head is faster that cat or dd
	os.system("head -c 1536000 /dev/graphics/fb0 > %sfb0_%s"%(dest, n+1000))
	n += 1
end = time.clock()
elapsed = end - begin
print '...complete'
print 'wrote %s frames in %s seconds'%(frames, elapsed)
fps = frames/elapsed
print 'fps = '+ str(fps)
print 'compressing frames...'
zf = zipfile.ZipFile("/mnt/sdcard/frames.zip","w")	#overwrites exising file of same name
raw_frames = os.listdir(dest)
for n in range(len(raw_frames)):
	zf.write(dest+raw_frames[n], raw_frames[n], zipfile.ZIP_DEFLATED)
zf.close()
print '...complete'
os.system("rm /mnt/sdcard/frames/*")
print 'removed large files'
n=30
print 'exit in'
while n > 0:
	print n
	n -= 1
	time.sleep(1)