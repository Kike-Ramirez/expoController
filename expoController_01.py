from OSC import OSCServer,OSCClient, OSCMessage
import sys
from time import sleep
import RPi.GPIO as GPIO
import time
import types


activeLight = False
activeVideoOn = False
activeVideoOff = False

lastButtonCar = 1
sentButtonCar = 0
timerButtonCar = 0

connected = False

raspberryAddress = '192.168.1.100', 7100
milluminAddress = '192.168.1.21', 5000
milluminAddress2 = '192.168.1.22', 5000


while not connected:
	
	try:
		server = OSCServer( raspberryAddress )
		server.timeout = 0

    	# Creamos el objeto "Cliente"
		client = OSCClient()
		client2 = OSCClient()

		# Realizamos la conexion
		client.connect( milluminAddress )
		client2.connect( milluminAddress2 )

		connected = True

	except:
		print("No se encuentra el servidor OSC. Reintentando...")
		time.sleep(5)






# this method of reporting timeouts only works by convention
# that before calling handle_request() field .timed_out is 
# set to False
def handle_timeout(self):
    self.timed_out = True

# funny python's way to add a method to an instance of a class
server.handle_timeout = types.MethodType(handle_timeout, server)

def callback_lightOn(path, tags, args, source):
    global activeLight
    # which user will be determined by path:
    # we just throw away all slashes and join together what's left
    user = ''.join(path.split("/"))
    # tags will contain 'fff'
    # args is a OSCMessage with data
    # source is where the message came from (in case you need to reply)
    # print ("Now do something with", user,args[2],args[0],1-args[1]) 
    print "LightPlus"

    if args[0] == 1.0:
    	activeLight = True;


def callback_lightOff(path, tags, args, source):
    global activeLight
    # which user will be determined by path:
    # we just throw away all slashes and join together what's left
    user = ''.join(path.split("/"))
    # tags will contain 'fff'
    # args is a OSCMessage with data
    # source is where the message came from (in case you need to reply)
    # print ("Now do something with", user,args[2],args[0],1-args[1]) 
    print "LightMinus"

    if args[0] == 1.0:
    	activeLight = False;

def callback_videoOn1(path, tags, args, source):
    if args[0] == 1.0:
    	msg = OSCMessage() #  we reuse the same variable msg used above overwriting it
        msg.setAddress("/millumin/action/launchOrStopColumn")
        msg.append(1.0)
        client.send(msg) # now we dont need to tell the client the address anymore
        client2.send(msg) # now we dont need to tell the client the address anymore

        print "videoOn1"

def callback_videoOn1eng(path, tags, args, source):
    if args[0] == 1.0:
    	msg = OSCMessage() #  we reuse the same variable msg used above overwriting it
        msg.setAddress("/millumin/action/launchOrStopColumn")
        msg.append(3.0)
        client.send(msg) # now we dont need to tell the client the address anymore
        client2.send(msg) # now we dont need to tell the client the address anymore

        print "videoOn1eng"

def callback_videoOn2(path, tags, args, source):
    if args[0] == 1.0:
    	msg = OSCMessage() #  we reuse the same variable msg used above overwriting it
        msg.setAddress("/millumin/action/launchOrStopColumn")
        msg.append(5.0)
        print "videoOn2"
        client.send(msg) # now we dont need to tell the client the address anymore
        client2.send(msg) # now we dont need to tell the client the address anymore

def callback_videoOn2eng(path, tags, args, source):
    if args[0] == 1.0:
    	msg = OSCMessage() #  we reuse the same variable msg used above overwriting it
        msg.setAddress("/millumin/action/launchOrStopColumn")
        msg.append(6.0)
        print "videoOn2eng"
        client.send(msg) # now we dont need to tell the client the address anymore
        client2.send(msg) # now we dont need to tell the client the address anymore

def callback_videoOn3(path, tags, args, source):
    if args[0] == 1.0:
    	msg = OSCMessage() #  we reuse the same variable msg used above overwriting it
        msg.setAddress("/millumin/action/launchOrStopColumn")
        msg.append(7.0)
        print "videoOn3"
        client.send(msg) # now we dont need to tell the client the address anymore
        client2.send(msg) # now we dont need to tell the client the address anymore

def callback_videoOn4(path, tags, args, source):
    if args[0] == 1.0:
    	msg = OSCMessage() #  we reuse the same variable msg used above overwriting it
        msg.setAddress("/millumin/action/launchOrStopColumn")
        msg.append(9.0)
        print "videoOn4"
        client.send(msg) # now we dont need to tell the client the address anymore
        client2.send(msg) # now we dont need to tell the client the address anymore

def callback_videoStop(path, tags, args, source):
    if args[0] == 1.0:
    	msg = OSCMessage() #  we reuse the same variable msg used above overwriting it
        msg.setAddress("/millumin/action/stopColumn")
        print "stopVideo"
        client.send(msg) # now we dont need to tell the client the address anymore
        client2.send(msg) # now we dont need to tell the client the address anymore

server.addMsgHandler( "/1/lightPlus", callback_lightOn )
server.addMsgHandler( "/1/lightMinus", callback_lightOff )
server.addMsgHandler( "/1/videoOn1", callback_videoOn1 )
server.addMsgHandler( "/1/videoOn1eng", callback_videoOn1eng )
server.addMsgHandler( "/1/videoOn2", callback_videoOn2 )
server.addMsgHandler( "/1/videoOn2eng", callback_videoOn2eng )
server.addMsgHandler( "/1/videoOn3", callback_videoOn3 )
server.addMsgHandler( "/1/videoOn4", callback_videoOn4 )
server.addMsgHandler( "/1/videoStop", callback_videoStop )

# user script that's called by the game engine every frame
def each_frame():
    # clear timed_out flag
    server.timed_out = False
    # handle all pending requests then return
    while not server.timed_out:
        server.handle_request()



GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.OUT) ## GPIO 17 como salida (bajar luz)
GPIO.setup(27, GPIO.OUT) ## GPIO 27 como salida (subir luz)
GPIO.setup(22, GPIO.IN, pull_up_down=GPIO.PUD_UP) ## GPIO 23 como entrada (boton iniciar show)





time_stamp = time.time() - 30;

# simulate a "game engine"
while True:

	while not connected:
		try:
			server = OSCServer( raspberryAddress )
			server.timeout = 0

	    	# Creamos el objeto "Cliente"
			client = OSCClient()
			client2 = OSCClient()

			# Realizamos la conexion
			client.connect( milluminAddress )
			client2.connect( milluminAddress2 )

			connected = True

		except:
			print("No se encuentra el servidor OSC. Reintentando...")
			time.sleep(5)

	try:
		# do the game stuff:
		if activeLight:
			GPIO.output(17, False)

		else:
			GPIO.output(17, True)

		# print GPIO.input(22)

		if (GPIO.input(22) == 0) and (lastButtonCar == 1): 

			timerButtonCar = time.time()
			lastButtonCar = 0
			# print "Inicio Pulso"

		elif (GPIO.input(22) == 0) and (lastButtonCar == 0) and (not sentButtonCar):

			delta = time.time() - timerButtonCar

			if delta > 1.0:
				msg = OSCMessage()
				msg.setAddress("/millumin/action/launchorStopColumn")
				msg.append(9.0)
				client.send(msg) # now we dont need to tell the client the address anymore
				client2.send(msg) # now we dont need to tell the client the address anymore
				sentButtonCar = True
				print "Lanzando mapping coche"
			

		elif (GPIO.input(22) == 1) and (lastButtonCar == 0):

			timerButtonCar = time.time()
			lastButtonCar = 1
			# print "Fin pulso"

		elif (GPIO.input(22) == 1) and (lastButtonCar == 1) and (sentButtonCar):

			if (time.time() - timerButtonCar > 1.0):

				# print "Reseteando boton de coche"
				sentButtonCar = False


		each_frame()

	except KeyboardInterrupt:

		client.close()
		client2.close()
		server.close()
		GPIO.cleanup()

