# Provides useful operations on files: copy file path or URI, MD5 digest, *nix strings
# Requires root, SL4A, and Python for Android

# Has limited support for remounting permission constrained filesystems, but I 
# have not put in the time to make it universally capable. Right now it only 
# remounts the rootfs, others may be inacessible depending on your system.

import android, os, sys, time, hashlib, subprocess
droid  = android.Android()

#global vars:
selected_dir_contents = []
dirs_only = []
files_only = []
selected_dir = ''
pipe=()
std_out=''
chmodded=[]
remounted = False

def cleanup():
	global chmodded, std_out, remounted
	for n  in range(len(chmodded)):
		sudo('busybox chmod o-rx %s'%(chmodded[n]))
		print 'Cleanup: Removed permissions r,x from %s'%chmodded[n]
		print '         response:',std_out
	if remounted == True:
		sudo ('mount -ro remount rootfs /')
		print 'Cleanup: Remounted root filesystem r/o'
		print '         response:',std_out
	print 'Cleanup complete.\nGoodbye'

def startMenu():
	global selected_dir
	try:
		choices = ['Root','SD Card']
		droid.dialogCreateAlert('Choose start directory:', None)
		droid.dialogSetItems(choices)
		droid.dialogShow()
		initial = droid.dialogGetResponse()
		if initial[1]['item'] == 0:
			selected_dir = '/'	
		elif initial[1]['item'] == 1:
			selected_dir = '/mnt/sdcard/'
		iterate()
	except KeyError:
		print 'KeyError: exiting'
		cleanup()
		sys.exit()

def clearLists():
	global 	selected_dir_contents, dirs_only, files_only
	selected_dir_contents = []
	dirs_only = []
	files_only = []

def sudo(command):
	global pipe, std_out
	pipe = subprocess.Popen(['su','-c','/system/bin/sh'], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
	std_out = pipe.communicate(input=command)	#use std_out[0] as shell response
	#print std_out[0]

def md5_for_file(file, block_size=2**20): #read and store only 2^20 bytes per iteration to handle files larger than RAM
    md5 = hashlib.md5()
    while True:
        data = file.read(block_size)
        if not data:
            break
        md5.update(data)
    return md5.hexdigest()
	
def iterate():
	try:
		global selected_dir_contents, dirs_only, files_only, selected_dir, std_out, chmodded, remounted
		try:
			os.chdir(selected_dir)
		except OSError, e:
			if e.errno == 13:
				if remounted == False:
					print 'Permissions: Remounting filesystem r/w'
					# handle remounting more than just the root filesystem.? I.E. tempfs, etc?
					sudo ('mount -o remount rootfs /')
					print '             response',std_out
					remounted = True
				print 'Permissions: chmodding %s +rx'%selected_dir
				sudo('busybox chmod o+rx %s'%selected_dir)
				print '             response',std_out
				chmodded.append(selected_dir)
				print 'chmodded[] = ',chmodded
				os.chdir(selected_dir)
		sudo('ls -a')
		selected_dir_contents = list(std_out)	#tuple to list
		selected_dir_contents = selected_dir_contents[0].split('\n')
		del(selected_dir_contents[-1])		#remove empty member left by split()
		print 'selected_dir_contents = ',selected_dir_contents
		for n in range(len(selected_dir_contents)):
			if os.path.isdir(selected_dir+selected_dir_contents[n]):
				selected_dir_contents[n] = selected_dir_contents[n] + '/'
				dirs_only.append(selected_dir_contents[n])
			else:
				files_only.append(selected_dir_contents[n])
		dirs_only.sort()
		files_only.sort()
		dirs_only[len(dirs_only):len(dirs_only)+len(files_only)] = files_only	#group files and directories into one list, directories first
		if len(dirs_only) == 0:		# empty directory
			droid.dialogCreateSpinnerProgress('Directory %s empty...'%selected_dir,'             No files found.')
			droid.dialogShow()
			selected_dir = ''
			time.sleep(1.7)
			clearLists()
			startMenu()
		if len(selected_dir) > 0:
			droid.dialogCreateAlert(selected_dir, None)
			droid.dialogSetItems(dirs_only)
			droid.dialogShow()
			choice_json_response = droid.dialogGetResponse()
			choice_num = int(choice_json_response[1]['item'])
			selected_dir = selected_dir + dirs_only[choice_num]		#now contains path to directory OR file, name is a bit misleading
			print 'selected path =',selected_dir
			clearLists()
			if os.path.isdir(selected_dir):
				iterate()
			elif os.path.isfile(selected_dir):
				filename = selected_dir.split('/')[-1]
				file = 'File: ' + filename
				droid.dialogCreateAlert(file, None)
				operations = ['MD5 Hash','Copy Path','Copy URI','Strings']
				droid.dialogSetItems(operations)
				droid.dialogShow()
				file_action = droid.dialogGetResponse()
				if file_action[1]['item'] == 0 :
					#sudo('cat %s'%selected_dir)		# selected_dir is actually a file path
					selected_file = open(selected_dir, 'rb')
					digest = md5_for_file(selected_file)
					print'MD5: %s\n    %s'%(selected_dir, digest)
					droid.dialogCreateAlert('MD5:  %s'%filename, digest)
					droid.dialogShow()
				elif file_action[1]['item'] == 1 :
					droid.setClipboard(selected_dir)
					droid.makeToast('Path to %s copied to clipboard'%filename)
				elif file_action[1]['item'] == 2 :
					droid.setClipboard('file://' + selected_dir)
					droid.makeToast('URI for %s copied to clipboard'%filename)
				elif file_action[1]['item'] == 3 :
					sudo('strings %s'%selected_dir)
					if len(std_out[0]) > 0:
						htm = '<pre>strings '+selected_dir+':\n'+std_out[0]+'</pre>'
					if len(std_out[0]) == 0:
						htm = 'No strings found in: %s'%selected_dir
					open('/mnt/sdcard/tmp/strings', 'w').write(htm)
					droid.startActivityForResult('android.intent.action.VIEW','file:///mnt/sdcard/tmp/strings', None, None,'com.android.browser','com.android.browser.BrowserActivity')
				cleanup()
	except KeyError:
		cleanup()

startMenu()
