# This I wrote to scratch a very specific itch. When I was living a couple hours
# away from my daughter and her mama, i frequently would nap @ 6pm for a couple
# hours. I would text them before I went to sleep and let them know when I was
# laying down, and whether they should call me, or I would call them for my
# daughter's bedtime story. This script sends a variable but generic text with
# the time I went to sleep, turns off the ringer/bluetooth, and monitors incoming
# calls. If they call, the phone will ring and wake me up, otherwise it stays
# silent. Also turns on bluetooth with ringer. Optionally opens my alarm clock if
# I select the option to set a wake up alarm.

# Requires SL4A, Python for Android, and also, for this implementation,
# the HTC alarm clock app.

import android, random, time, Ringthru as ringthru
droid = android.Android()

# phone numbers have been changed to protect the innocent
#rcvr = '5555555555'		# testing
rcvr = '5555555555'		# production

current_hour = int(time.strftime('%H'))
current_minute = int(time.strftime('%M'))
droid.dialogCreateTimePicker(current_hour, current_minute, True)
droid.dialogShow()
raw_time = droid.dialogGetResponse()

# get current time in a friendly format
if raw_time[1]['hour'] >= 12:
	day_half = 'p.m.'
	hour = (raw_time[1]['hour']) - 12
	if hour == 0:
		hour = 12
if raw_time[1]['hour'] < 12:
	day_half = 'a.m.'
	hour = raw_time[1]['hour']
	if hour == 0:
		hour = 12
if raw_time[1]['minute'] < 10:
	minute = '0%s'%raw_time[1]['minute']
else:
	minute = raw_time[1]['minute']

greetings = ['Hi', 'Hello', 'Hola', 'Aloha']
names = ['sweethearts','sweet girls', 'chickabees', 'Mama and Baby', 'sweet potatoes', 'mis amores']
pretty_time = '%s:%s %s'%(hour, minute, day_half)
#message = random.choice(greetings) + random.choice(names) + '. I\'m napping at %s'%pretty_time 
droid.dialogCreateAlert('Select wake method:', None)
droid.dialogSetPositiveButtonText('Call')
droid.dialogSetNeutralButtonText('Both')
droid.dialogSetNegativeButtonText('Alarm')
droid.dialogShow()
wake = droid.dialogGetResponse()
preamble = random.choice(greetings) + ' '+ random.choice(names) + '. I\'m napping '
bye = ' Love you both bunches, -B.'

if wake[1]['which'] == 'positive': # 'Call'
	message = preamble + 'at %s Please call on Mama\'s phone to wake me up for a story.'%pretty_time + bye
	edit = droid.dialogGetInput('Text Message','Edit if needed:', message)
	#print edit[1]
	if edit[1] != None:
		droid.smsSend(rcvr, edit[1])
	ringthru.PRIV_NUM = rcvr
	ringthru.getRingVol()
	ringthru.main()

if wake[1]['which'] == 'neutral': # 'Both'
	message = preamble + 'at %s You can call and wake me up, but I\'m also setting an alarm.'%pretty_time + bye
	edit = droid.dialogGetInput('Text Message','Edit if needed:', message)
	#print edit[1]
	if edit[1] != None:
		droid.smsSend(rcvr, edit[1])
	droid.makeToast('Set for %s'%pretty_time)
	droid.startActivityForResult('com.htc.android.worldclock.action.ALARMCLOCK')
	ringthru.PRIV_NUM = rcvr	
	ringthru.getRingVol()
	ringthru.main()

if wake[1]['which'] == 'negative': # 'Alarm'
	message = preamble + 'at %s and setting my alarm for <TIME>. Please call after for a story.'%pretty_time + bye
	edit = droid.dialogGetInput('Text Message','Edit if needed:', message)
	#print edit[1]
	if edit[1] != None:
		droid.smsSend(rcvr, edit[1])
	droid.makeToast('Set for %s'%pretty_time)
	droid.startActivityForResult('com.htc.android.worldclock.action.ALARMCLOCK')
