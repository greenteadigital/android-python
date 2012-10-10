# A utility script to download some of my favorite NPR podcasts
# Requires SL4A and Python for Android

import urllib2, os, os.path, string, android, sys, time, datetime
droid = android.Android()
timestamp = str(datetime.datetime.today())
loglist = ["<pre>", timestamp + "\n"]	#will be written to log file
prettynames = {"car_talk":"Car Talk", "fresh_air":"Fresh Air", "radio_lab":"Radio Lab", "wait_wait":"Wait Wait"}
BASEPATH = "/mnt/extSdCard/Music/podcasts/"	#sgs3
#BASEPATH = "/home/ben/Desktop/"		#laptop

def log(message):
	global loglist
	print message
	loglist.append(message+"\n")

def getPodcasts(show_name, url, altFmt):	#argument 'show_name' must contain no spaces
	global BASEPATH, prettynames
	log( "\nBegin fetching %s podcasts"%prettynames[show_name])
	show_dir = BASEPATH + show_name + "/"
	log( "saving to: "+show_dir)
	if os.path.exists(show_dir) == False:
		log( "*couldn't find save directory for "+prettynames[show_name]+", creating...")
		os.mkdir(show_dir)
		log( "created show directory "+ show_dir)
	history_file = show_dir + show_name+".history"	#i.e. /mnt/sdcard/Music/podcasts/car_talk/car_talk.history
	if os.path.exists(history_file) == False:
		log( "*couldn't find history file for "+prettynames[show_name]+", creating...")
		f= open(history_file,"wb")
		f.write("")
		f.close()
		log( "created history file "+ history_file)
	if os.path.exists(history_file) == True:
		log("reading history for "+ prettynames[show_name])
		history = open(history_file,"rb").read()
	log("fetching RSS feed for "+ prettynames[show_name])
	pagesrc = urllib2.urlopen(url).readlines()
	enclosures = []		#array of available mp3 url's
	wrote = 0
	skipped = 0
	if altFmt == False:
		for n in range(len(pagesrc)):
			if pagesrc[n].find("<enclosure url=") > -1:
				enclosures.append(pagesrc[n])
	if altFmt == True:
		for n in range(len(pagesrc)):
			hook = "<media:content url=\"http://feeds.wnyc.org"
			if pagesrc[n].find(hook) > -1:
				idx0 = pagesrc[n].find(hook)
				idx1 = pagesrc[n].find("type=\"audio/mpeg\"")
				enclosures.append(pagesrc[n][idx0:idx1])
	for n in range(len(enclosures)):
		link_elements = enclosures[n].split("\"")
		log( "parsed link: \""+ link_elements[1]+"\"")
		filename = link_elements[1].split("/")[-1]
		listened = False
		have = False
		if string.find(history, filename) > -1:
			log( " found \""+filename+"\" in "+history_file.split("/")[-1]+", skipping")
			skipped += 1
			listened = True
		if listened == False and os.path.exists(show_dir + filename) == True:
			log( " found "+filename+" in "+show_dir+", skipping")
			skipped += 1
			have = True
			log( " updating history to show "+filename+" already stored")
			f= open(history_file, "ab")
			f.write(filename + "\n")
			f.close()
		if listened == False and have == False:
			log( " mp3 \""+filename+"\" not found in history or "+show_dir+", so...")
			log( " ...fetching " + filename)
			page = urllib2.urlopen(link_elements[1])
			filesize = page.info().get("Content-Length")
			if filesize == None:
				droid.dialogCreateSpinnerProgress("Downloading %s %s"%(prettynames[show_name],filename), link_elements[1], 100)
				droid.dialogShow()
				grab = page.read()
			if filesize != None:
				mb = int(filesize)/1000000
				kbytes = int(filesize)%1000000
				kb = kbytes/10000
				prettysize = '%s.%s MB'%(mb,kb)
				droid.dialogCreateHorizontalProgress("%s:  %s"%(prettynames[show_name],prettysize),"URL: %s"%link_elements[1], int(filesize))
				droid.dialogShow()
				mp3bytes = ''
				chunks_read = 0
				CHUNK_SIZE = 110208
				while len(mp3bytes) < int(filesize):
					grab = page.read(CHUNK_SIZE)
					mp3bytes = mp3bytes + grab
					chunks_read += 1
					droid.dialogSetCurrentProgress(CHUNK_SIZE * chunks_read)
			page.close()
			droid.dialogDismiss()
			oohShiny("Writing file to disk...")
			log( " writing " + filename)
			f= open(show_dir + filename,"wb")
			if mp3bytes:
				f.write(mp3bytes)
			else:
				f.write(grab)
			f.close()
			log( " wrote "+show_dir+filename)
			f= open(history_file, "ab")
			f.write(filename + "\n")
			f.close()
			log( " updated "+history_file+" with "+filename)
			wrote += 1
	log("skipped %s file(s)"%skipped)
	log( "wrote %s file(s)"%wrote)
	log( "Done fetching "+prettynames[show_name]+" podcasts\n")

def getAll():
	#print "called getAll()"
	getPodcasts("car_talk","http://www.npr.org/rss/podcast.php?id=510208", False)
	getPodcasts("fresh_air","http://www.npr.org/rss/podcast.php?id=13", False)
	getPodcasts("wait_wait","http://www.npr.org/rss/podcast.php?id=35", False)
	getPodcasts("radio_lab","http://feeds.wnyc.org/radiolab", True)	#uses FeedBurner, so altFmt = True

def writeLog():
	global BASEPATH, loglist
	loglist.append("</pre>")
	L = open(BASEPATH+"update-log.html","wb")
	L.writelines(loglist)
	L.close()

def oohShiny(message):
	droid.dialogCreateSpinnerProgress(None, message, 100)
	droid.dialogShow()

def main():
	global BASEPATH, droid
	init = ["Update All","Select Update","View Log File","Exit"]
	print init
	droid.dialogCreateAlert("Select Action:",None)
	droid.dialogSetItems(init)
	droid.dialogShow()
	init_resp = droid.dialogGetResponse()
	#print "init_resp = ",init_resp[1]['item']
	print str(init_resp)
	if init_resp[1]['item'] == 0:
		droid.wakeLockAcquireDim()
		oohShiny("Updating all podcasts...")
		getAll()
		oohShiny("Writing log file...")
		writeLog()
		droid.dialogDismiss()
	if init_resp[1]['item'] == 1:
		droid.wakeLockAcquireDim()
		choices = ["Car Talk", "Fresh Air", "Radio Lab", "Wait Wait"]
		droid.dialogCreateAlert("Select Podcast(s):", None)
		droid.dialogSetMultiChoiceItems(choices)
		droid.dialogSetPositiveButtonText('Go')
		droid.dialogSetNegativeButtonText('Cancel')
		droid.dialogShow()
		button_resp = droid.dialogGetResponse()
		#print "button_resp = ",button_resp[1]['which']
		selected = droid.dialogGetSelectedItems()
		#print "selected = ",selected[1]
		if button_resp[1]['which'] == "negative":
			sys.exit()
		if ( (button_resp[1]['which'] == "positive") and (len(selected[1]) > 0) ):
			if selected[1].count(0) > 0:
				oohShiny("Updating Car Talk...")
				getPodcasts("car_talk","http://www.npr.org/rss/podcast.php?id=510208", False)
				#print "commented call to getPodcasts(car_talk)"
				droid.dialogDismiss()
			if selected[1].count(1) > 0:
				oohShiny("Updating Fresh Air...")
				getPodcasts("fresh_air","http://www.npr.org/rss/podcast.php?id=13", False)
				#print "commented call to getPodcasts(fresh_air)"
				droid.dialogDismiss()
			if selected[1].count(2) > 0:
				oohShiny("Updating Radio Lab...")
				getPodcasts("radio_lab","http://feeds.wnyc.org/radiolab", True)
				#print "commented call to getPodcasts(radio_lab)"
				droid.dialogDismiss()
			if selected[1].count(3) > 0:
				oohShiny("Updating Wait Wait...")
				getPodcasts("wait_wait","http://www.npr.org/rss/podcast.php?id=35", False)
				#print "commented call to getPodcasts(wait_wait)"
				droid.dialogDismiss()
			oohShiny("Writing log file...")
			writeLog()
			droid.dialogDismiss()
	if init_resp[1]['item'] == 2:
		droid.startActivityForResult('android.intent.action.VIEW','file://'+BASEPATH+'update-log.html', None, None,'com.android.browser','com.android.browser.BrowserActivity')
		sys.exit()
	if init_resp[1]['item'] == 3:
		sys.exit()
	droid.dialogCreateAlert("Update Complete", None)
	droid.dialogSetPositiveButtonText(' View Log ')
	droid.dialogSetNegativeButtonText(' Exit ')
	droid.dialogShow()
	action = droid.dialogGetResponse()
	if action[1]['which'] == 'positive':
		droid.wakeLockRelease()
		#droid.webViewShow("file://"+BASEPATH+"update-log.html")
		droid.startActivityForResult('android.intent.action.VIEW','file://'+BASEPATH+'update-log.html', None, None,'com.android.browser','com.android.browser.BrowserActivity')
	if action[1]['which'] == 'negative':
		droid.wakeLockRelease()
		sys.exit()
#print "test"
main()
