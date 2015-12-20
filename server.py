#!/usr/bin/python

"""
Save this file as server.py

>>> python server.py
Serving on 0.0.0.0:8000

You can use this to test GET and POST methods.

SERVER PORT 2468
"""

import RPi.GPIO as GPIO
import SimpleHTTPServer
import SocketServer
import logging
import urlparse
import sys


if len(sys.argv) > 1:
    PORT = int(sys.argv[1])
    I = "0.0.0.0"
else:
    PORT = 2468
    I = "0.0.0.0"

GPIO.setmode(GPIO.BCM)
pinlist=[17, 18, 27, 22]

#17 = bed-light
#18 = focus light
#27 = fan

for i in pinlist:
    GPIO.setup(i,GPIO.OUT)
    GPIO.output(i,GPIO.HIGH)

class ServerHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):


    def do_POST(self):
        
        print "======= POST VALUES ======="
        length = int(self.headers.getheader('content-length'))
        field_data = self.rfile.read(length)
        fields = urlparse.parse_qs(field_data)
        for key,value in fields.iteritems():
            value=int(value[0])
            print key,value
            print "Switching ",
            if(value==1):
                print "on ",
            else:
                print "off ",
            print key.split('_')            

            if(key=="bed_light"):
	        if(value==1):                   # switch light on
                	GPIO.output(17,GPIO.LOW)
                elif(value==0):                 #switch light off
                	GPIO.output(17,GPIO.HIGH)

            elif(key=="focus_light"):
                if(value==1):
                    GPIO.output(18,GPIO.LOW)
                elif(value==0):
                    GPIO.output(18,GPIO.HIGH)

            elif(key=="fan"):
                if(value==1):
                	GPIO.output(27,GPIO.LOW)
                elif(value==0):
              		GPIO.output(27,GPIO.HIGH)
            
        self.send_response(200) #create header
        self.send_header("Content-type", "text/html")
        self.end_headers()

        self.wfile.write("Success") #send response


Handler = ServerHandler

try:
    httpd = SocketServer.TCPServer(("", PORT), Handler)
    print "Serving at: http://%(interface)s:%(port)s" % dict(interface=I or "localhost", port=PORT)
    httpd.serve_forever()

except KeyboardInterrupt:
    print 'Interrupt received, shutting down the web server'
    httpd.socket.close()
    GPIO.cleanup()    
