from OSC import OSCServer
import sys
from time import sleep
import RPi.GPIO as GPIO
import time

connected = False

while not connected:
	try:
		server = OSCServer( ("10.2.7.87", 7100) )
		server.timeout = 0
		run = True
		connected = True

	except: 
		print "OSC connection fail..."
		time.sleep(5)

GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.OUT) ## GPIO 17 como salida
GPIO.setup(27, GPIO.OUT) ## GPIO 27 como salida
GPIO.setup(22, GPIO.OUT) ## GPIO 22 como salida

time1 = 0
timer1 = 1
time2 = 0
timer2 = 2
active2 = False
active3 = False


# this method of reporting timeouts only works by convention
# that before calling handle_request() field .timed_out is 
# set to False
def handle_timeout(self):
    self.timed_out = True

# funny python's way to add a method to an instance of a class
import types
server.handle_timeout = types.MethodType(handle_timeout, server)

def user_callback1(path, tags, args, source):
    global time1
    # which user will be determined by path:
    # we just throw away all slashes and join together what's left
    user = ''.join(path.split("/"))
    # tags will contain 'fff'
    # args is a OSCMessage with data
    # source is where the message came from (in case you need to reply)
    # print ("Now do something with", user,args[2],args[0],1-args[1]) 
    time1 = time.time()
    GPIO.output(17, True)

def user_callback2(path, tags, args, source):
    global active2
    # which user will be determined by path:
    # we just throw away all slashes and join together what's left
    user = ''.join(path.split("/"))
    # tags will contain 'fff'
    # args is a OSCMessage with data
    # source is where the message came from (in case you need to reply)
    # print ("Now do something with", user,args[2],args[0],1-args[1]) 

    if args[0] == 1.0:
    	active2 = True;
    else:
    	active2 = False;

def user_callback3(path, tags, args, source):
    global active3
    # which user will be determined by path:
    # we just throw away all slashes and join together what's left
    user = ''.join(path.split("/"))
    # tags will contain 'fff'
    # args is a OSCMessage with data
    # source is where the message came from (in case you need to reply)
    # print ("Now do something with", user,args[2],args[0],1-args[1]) 

    if args[0] == 1.0:
    	active3 = True;
    else:
    	active3 = False;

def quit_callback(path, tags, args, source):
    # don't do this at home (or it'll quit blender)
    global run
    run = False

server.addMsgHandler( "/1/push1", user_callback1 )
server.addMsgHandler( "/1/push2", user_callback2 )
server.addMsgHandler( "/1/push3", user_callback3 )

# user script that's called by the game engine every frame
def each_frame():
    global time1, timer1, time2, timer2, time3, timer3
    # clear timed_out flag
    server.timed_out = False
    # handle all pending requests then return
    while not server.timed_out:
        server.handle_request()

# simulate a "game engine"
while run:

    # do the game stuff:
    if time.time() - time1 > timer1:
        GPIO.output(17, False)

    if active2:
    	GPIO.output(27, True)
    else:
    	GPIO.output(27, False)

    if active3:
    	GPIO.output(22, True)
    else:
    	GPIO.output(22, False)





    # call user script
    each_frame()

server.close()