
""" sending OSC messages from Raspberry
    Author: Kike Ramirez
    12.09.2016
"""

# 23 boton
# 24 radio

PIN = 24
from OSC import OSCServer,OSCClient, OSCMessage
import time, random
import RPi.GPIO as GPIO


timerPulse = 1
timePulse = time.time()

timerPing = 4

def my_callback(channel):
    global timePulse;
    if (time.time() - timePulse) > timerPulse:
        try:
            msg = OSCMessage() #  we reuse the same variable msg used above overwriting it
            msg.setAddress("/keydown")
	    print "/keydown"
            client.send(msg) # now we dont need to tell the client the address anymore
            timePulse = time.time()
        except:
            print("Sin conexion OSC")

GPIO.setmode(GPIO.BCM)
GPIO.setup(PIN,GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.add_event_detect(PIN, GPIO.FALLING, callback=my_callback)

server_IP = '10.2.7.87', 7100
verbose = True

try:

    server = OSCServer( server_IP )
    server.timeout = 0
except:
    if verbose: print("No se encuentra el servidor OSC")

connected = False

while (connected == False):

    try:
        client_IP = '10.2.7.75', 7110

        # Creamos el objeto "Cliente"
        client = OSCClient()

        # Realizamos la conexion
        client.connect( client_IP )

        connected = True
    except:
        print("Esperando cliente OS ")

print("Sending OSC messages to: " + str(client_IP))
try :    
    while 1: # endless loop
        try: 
            msg = OSCMessage() #  we reuse the same variable msg used above overwriting it
            msg.setAddress("/ping")
            print "/ping"
            client.send(msg) # now we dont need to tell the client the address anymore
        except:
            print("Sin conexion OSC")
            time.sleep(timerPing)
        time.sleep(timerPing)

except KeyboardInterrupt:
    print "Closing OSCClient"
    client.close()
    print "Done"
        


