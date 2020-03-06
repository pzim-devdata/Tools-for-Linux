#!/usr/bin/env python
#-*-coding:utf-8-*-
# Trust in Pzim !
# python3-xlib package must be installed to run this script :
#sudo apt-get install python3-xlib
#or sudo apt-get install python-xlib

import os
from Xlib import X, display
from Xlib.ext import record
from Xlib.protocol import rq

Screen_resolution = (1920,1080) # write here your screen resolution

Corner_area = 30 # write here the size of the virtual squares that receive wheel up and down event at the corner of your screen 

# Let's set up the commands
def volume_up():

    os.system("amixer set Master 5%+ & pid=$!")
    #os.system("amixer -q sset Master 5%+ & pid=$!")
    #os.system("pactl set-sink-volume 0 +5% & pid=$!")  
    #os.system("pactl set-sink-volume 2 +5% & pid=$!")
    #os.system("pactl set-sink-volume 1 +5% & pid=$!")

    # write your bash command between "" to volume up

    # use "& pid=$!" end of your command to prevent freezing python script if your command takes long time to process.

def volume_down():

    os.system("amixer set Master 5%- & pid=$!")  
    #os.system("amixer -q sset Master 5%- & pid=$!") 
    #os.system("pactl set-sink-volume 0 -5% & pid=$!")
    #os.system("pactl set-sink-volume 2 -5% & pid=$!")
    #os.system("pactl set-sink-volume 1 -5% & pid=$!")

    # write your bash command between "" to volume up

record_dpy = display.Display()

ctx = record_dpy.record_create_context(
        0,
        [record.AllClients],
        [{
                'core_requests': (0, 0),
                'core_replies': (0, 0),
                'ext_requests': (0, 0, 0, 0),
                'ext_replies': (0, 0, 0, 0),
                'delivered_events': (0, 0),
                'device_events': (X.KeyPress, X.MotionNotify),
                'errors': (0, 0),
                'client_started': False,
                'client_died': False,
        }])

def record_callback(reply):

    data = reply.data
    while len(data):
        event, data = rq.EventField(None).parse_binary_value(data, record_dpy.display, None, None)
        
        if event.type == X.ButtonPress:
            print (event.detail, event.root_x, event.root_y)

            # Let's set up right up corner 

            #if all( [event.root_x > Screen_resolution[0] - Corner_area, event.root_y < Corner_area] ):

             #  print ("right up corner detected") 

               # event.detail 4 means wheel up event

              # if event.detail is 4 : 
               #   print ("volume up!")
                #  volume_up() 

               # event.detail 5 means wheel down event

              # if event.detail is 5 :
               #   print ("volume down!")
                #  volume_down() 

            # Let's set up left up corner

            if all( [event.root_x < Corner_area , event.root_y < Corner_area] ):

               print ("left up corner detected")

               if event.detail is 4 :
                  print ("volume up!")
                  volume_up() 

               if event.detail is 5 :
                  print ("volume down!")
                  volume_down() 
  
            # Let's set up right down corner

            #if all( [event.root_x > Screen_resolution[0] - Corner_area, event.root_y > Screen_resolution[1] - Corner_area] ):

             #  print "right down corner detected"

              # if event.detail is 4 :
               #   print "volume up!"
                #  volume_up() 

              # if event.detail is 5 :
               #   print "volume down!"
                #  volume_down() 

            # Let's set up left down corner 

            if all( [event.root_x < Corner_area , event.root_y > Screen_resolution[1] - Corner_area] ):

               print ("left down corner detected")

               if event.detail is 4 :
                  print ("volume up!") 
                  volume_up() 

               if event.detail is 5 :
                  print ("volume down!") 
                  volume_down() 
                                   
            
        elif event.type == X.ButtonRelease:

            print  (event.detail, event.root_x, event.root_y)
            
        elif event.type == X.MotionNotify:

            print (event.root_x, event.root_y)
            

record_dpy.record_enable_context(ctx, record_callback)
