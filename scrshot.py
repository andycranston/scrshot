#! /usr/bin/python3
#
# @(!--#) @(#) scrshot.py, version 006, 26-october-2019
#
# a screenshot program by Andy Cranston
#
# cool feature #1: screenshots saved as monochrome PNG
#
# cool feature #2: sending a specially formatted UDP packet to the host
#                  results in triggering a screen shot
#

############################################################################

DEBUG = False

############################################################################

import sys
import os
import argparse
import time
import datetime
import socket
import select
import pyautogui
from PIL import Image

import monopng

############################################################################

DEFAULT_UDP_PORT = 8333
SLEEP_INTERVAL = 0.1
WATCHDOG_INTERVAL = 20
PIXEL_REGION = 200
DEFAULT_TASKBAR_WIDTH = 40
DEFAULT_TASKBAR_POSITION = 'bottom'

############################################################################

def rgb2mono(rgb):
    return (rgb[0] + rgb[1] + rgb[2]) // 3

############################################################################

def string2bytearray(s):
    ba = bytearray(len(s))

    for i in range(0, len(s)):
        ba[i] = ord(s[i])

    return ba

############################################################################

def parseregion(regiontext):
    nlist = regiontext.split(',')

    if len(nlist) != 4:
        return False

    for number in nlist:
        try:
            n = int(number)
        except ValueError:
            return False
        if n < 0:
            return False

    return (
             int(nlist[0]) ,
             int(nlist[1]) ,
             int(nlist[2]) ,
             int(nlist[3]) ,
           )

############################################################################

#
# Main
#

def main():
    global progname

    try:
         userprofile = os.environ['USERPROFILE']
    except KeyError:
         userprofile = 'C:'

    defaultdir = userprofile + '\\Pictures'

    screenwidth, screenheight = pyautogui.size()

    screenregion = (0, 0, screenwidth, screenheight)

    parser = argparse.ArgumentParser()

    parser.add_argument('--dir',      help='directory to save screenshots to', default=defaultdir)
    parser.add_argument('--fs',       help='screenshot entire screen including taskbar', action="store_true")
    parser.add_argument('--region',   help='the region of the screen to screenshot')
    parser.add_argument('--tbw',      help='width of taskbar', default=DEFAULT_TASKBAR_WIDTH)
    parser.add_argument('--tbp',      help='taskbar position', default=DEFAULT_TASKBAR_POSITION)
    parser.add_argument('--noremote', help='do not allow remote triggering of screenshots', action="store_true")
    parser.add_argument('--port',     help='UDP port number to listen on', default=DEFAULT_UDP_PORT)
        
    args = parser.parse_args()

    dir = args.dir

    if not os.path.isdir(dir):
        print('{}: the path "{}" is not a directory'.format(progname, dir))
        sys.exit(1)

    if not os.access(dir, os.W_OK):
        print('{}: the directory "{}" is not writable'.format(progname, dir))
        sys.exit(1)

    try:
        tbw = int(args.tbw)
    except ValueError:
        print('{}: task bar width "{}" does not appear to be an integer'.format(progname, args.tbw))
        sys.exit(1)

    if tbw < 0:
        print('{}: task bar width "{}" is negative'.format(progname, args.tbw))
        sys.exit(1)

    tbp = args.tbp.lower()

    if (tbp == 'top') or (tbp == 't'):
        screenregion = (0, tbw, screenwidth, screenheight - tbw)
    elif (tbp == 'bottom') or (tbp == 'b'):
        screenregion = (0, 0, screenwidth, screenheight - tbw)
    elif (tbp == 'left') or (tbp == 'l'):
        screenregion = (tbw, 0, screenwidth - tbw, screenheight)
    elif (tbp == 'right') or (tbp == 'r'):
        screenregion = (0, 0, screenwidth - tbw, screenheight)
    else:
        print('{}: task bar position "{}" is not valid'.format(progname, args.tbp))
        sys.exit(1)

    if args.fs:
        screenregion = (0, 0, screenwidth, screenheight)

    if args.region:
        screenregion = parseregion(args.region)
        if screenregion == False:
            print('{}: region "{}" is not valid'.format(progname, args.region))
            sys.exit(1)

    ### print(screenregion)

    try:
        port = int(args.port)
    except ValueError:
        print('{}: UDP port number "{}" is not an integer'.format(progname, args.port))
        sys.exit(1)

    if not args.noremote:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind(('', port))

    packetpayload = string2bytearray('please take a screenshot now')

    mpng = monopng.MonoPNG(screenregion[2], screenregion[3])

    midWidth = screenwidth // 2

    lastMouseX = -1
    lastMouseY = -1

    watchdogcounter = WATCHDOG_INTERVAL

    while True:
        takescreenshot = False

        currentMouseX, currentMouseY = pyautogui.position()

        if DEBUG:
            print(lastMouseX, lastMouseY)
            print(currentMouseX, currentMouseY)

        # see if mouse movements mean a screenshot
        if (currentMouseX != lastMouseX) or (currentMouseY != lastMouseY):
            if (lastMouseY == 0) and (currentMouseY > 0):
                if abs(midWidth - currentMouseX) <= PIXEL_REGION:
                    takescreenshot = True

        # see if a UDP packet has been receieved which would trigger a screesnot
        if not args.noremote:
            rlist, wlist, xlist = select.select([sock], [], [], 0.0)
            if DEBUG:
                print(rlist)
            if len(rlist) > 0:
                try:
                    packet, address = sock.recvfrom(65536)
                    if len(packet) == len(packetpayload):
                        if packet == packetpayload:
                            takescreenshot = True
                except ConnectionResetError:
                    print("{}: connecton reset error - going again".format(progname), file=sys.stderr)

        if takescreenshot == False:
            if DEBUG:
                print('No Change - sleeping')
            time.sleep(SLEEP_INTERVAL)
            watchdogcounter += 1
            if watchdogcounter > WATCHDOG_INTERVAL:
                print('Waiting for screenshot trigger action')
                watchdogcounter = 0
        else:
            print('Taking screenshot')
            scrshotfile = '{}\\scrshot-{:%Y%m%d-%H%M%S}.png'.format(dir, datetime.datetime.now())

            scrshot = pyautogui.screenshot(region=screenregion)

            for x in range(0, screenregion[2]):
                for y in range(0, screenregion[3]):
                    mpng.plot(x, y, rgb2mono(scrshot.getpixel( (x, y) )))

            mpng.write(scrshotfile)

            print('Done')
                
        lastMouseX = currentMouseX
        lastMouseY = currentMouseY

    return 0

############################################################################

progname = os.path.basename(sys.argv[0])
try:
    sys.exit(main())
except KeyboardInterrupt:
    print('')
    print('Exiting')
    sys.exit(0)

# end of file
