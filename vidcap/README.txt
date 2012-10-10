vidcap - Android Video Screen Capture Proof-of-Concept for HTC EVO 4G
---------------------------------------------------------------------
A collection of Python scripts to capture screen video from the HTC EVO 4G

Requires:
	--SL4A, Python for Android, & root access on Android device
	--imagemagick, mencoder, ffmpeg, & VLC on linux dev machine
	--1.5MB of temporary storage per frame

Contents
-------------
frame-grab.py 
	--run this first on Android device; dumps frames from buffer, ouputs a zip file

get-n-split.py 
	--run on linux dev machine; FTP's into Android device, gets zip, extracts raw frames

fb2img.py
	--run last; shuffles bytes & adds header to convert raw frames to BMPs,
	  calls external binaries to convert: bmp -> jpg -> avi -> mp4,
	  launches mp4 video in VLC
	  
Issues...
---------
Intial testing only captured ~2 frames/second. The bottleneck is most likely the writes to sdcard b/w reads to the framebuffer. Possible soutions may involve writing to a ramdisk or emmc, or simply holding (limited) frame data in process memory. Also, reads of the frambuffer occur while OS is writing to it, so some/most frames contain "tearing" (see included jpgs). A possible solution may involve calling the native fbtool binary in place of head, though this has not been tested.