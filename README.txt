Python Applications for Android
-------------------------------
A collection of my Python scripts for doing various useful things in Android. These were all written to scratch a personal itch. Except vidcap, which outputs to the terminal, all scripts launch a GUI. All require the SL4A RPC server and the Python interpreter for Android.

Required Installers
-------------------
SL4A - https://android-scripting.googlecode.com/files/sl4a_r6.apk
Python for Android - https://python-for-android.googlecode.com/files/PythonForAndroid_r5.apk

Contents
--------
Podcat.py
	--An application for download/update of some of my favorite NPR podcasts.
	
SuFileOps.py
	--Provides useful operations on files: copy path or URI to clipboard, MD5 digest, Unix strings. Easily extendable, requires root.

Napping.py
	--See source for more info.
	  
Righthru.py
	--Turns off phone ringer and bluetooth, then monitors incoming calls for a user-selected privileged caller. Privileged calls turn on the ringer and bluetooth while others are dropped silently. Imported by Napping.py
	
NetCap.py
	--A simple packet capture script/tcpdump UI which monitors the first listed active interface (wifi/3g/4g). Capture files are pcap format for use in Wireshark. Requires root and tcpdump for ARM.
	
./vidcap
	--See ./vidcap/README.txt