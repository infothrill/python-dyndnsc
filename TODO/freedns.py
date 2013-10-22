#!/usr/bin/python

import urllib2
import os.path

OLDIP_FILE = '/var/lib/misc/oldip'

def updatedns(ip):
    print urllib2.urlopen("http://freedns.afraid.org/dynamic/update.php?YOUR-SECRET-KEY-HERE").read().strip()
    f = open(OLDIP_FILE, 'w')
    f.write(ip)
    f.close()

newip = urllib2.urlopen("http://ip.dnsexit.com/").read().strip()

if not os.path.exists(OLDIP_FILE):
    updatedns(newip)
else:
    f = open(OLDIP_FILE, 'r')
    oldip = f.read()
    f.close()
    if oldip != newip:
        updatedns(newip)