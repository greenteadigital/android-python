# Turns the phone ringer and bluetooth off, monitors incoming calls for a
# privileged caller, and turns on ringer and bluetooth if detected. Imported by
# Napping.py

import android
import time, sys

droid = android.Android()
PRIV_NUM = ''
RING_VOL = ''
droid.startTrackingPhoneState()
droid.toggleRingerSilentMode(True)
droid.setRingerVolume(0)
        
def getPrivNum():
    global PRIV_NUM
    PRIV_NUM = droid.pickPhone()[1]                #choose the contact who is allowed to ring through
    PRIV_NUM = PRIV_NUM.replace('-','')            #some numbers are stored as: '123-456-7890'
    print 'PRIV_NUM ==',PRIV_NUM
    return

def getRingVol():
    global RING_VOL
    droid.dialogCreateSeekBar(2,6,'Select ringer volume:','1     2       3       4        5       6      7')
    droid.dialogSetPositiveButtonText(' Set ')
    droid.dialogShow()
    t=droid.dialogGetResponse()
    print 'RING_VOL ==',int(t[1]['progress']) + 1
    RING_VOL = str( int( t[1]['progress'] ) + 1 )
    return

def main():
    global PRIV_NUM, RING_VOL
    if len(PRIV_NUM) == 10:
        prettyNum = '%s-%s-%s'%(PRIV_NUM[0:3],PRIV_NUM[3:6],PRIV_NUM[6:])
    elif len(PRIV_NUM) == 7:
        prettyNum = '%s-%s'%(PRIV_NUM[0:3],PRIV_NUM[3:])
    else:
        prettyNum = PRIV_NUM
    droid.notify('Ring Through','Ring through enabled for '+ prettyNum)
    droid.toggleBluetoothState(False,False)
    print 'monitoring phone state...'
    while True:
        state = droid.readPhoneState()
        curr_vol = droid.getRingerVolume()[1]
        if ((state[1]['incomingNumber'].find(PRIV_NUM) > -1
        and state[1]['state'] == 'ringing')
        or (PRIV_NUM.find(state[1]['incomingNumber']) > -1 and state[1]['state'] == 'ringing')
        or (curr_vol != 0)):        #allow privileged caller to ring through
            droid.setRingerVolume(int(RING_VOL))
            droid.toggleRingerSilentMode(False)
            print 'Allowed', prettyNum, 'to ring through'
            droid.toggleBluetoothState(True,False)
            sys.exit()
        else:
			# IF SCRIPT BEGINS TO FAIL INTERMITTENTLY, SHORTEN THIS PAUSE !!
            time.sleep(0.3)
if __name__ == "__main__":
    getPrivNum()
    getRingVol()
    main()