#!/usr/bin/python
import subprocess
import sys
import random

class Command(object):

    def __init__(self, path):
        self.path = path

    def __call__(self, *args):
        call_args = list(args)
        call_args.insert(0, self.path)
        return subprocess.check_call(call_args)

def octect(i): 
    return "{0:02x}".format(i)

def random_macaddr():
    always_start_with_zero = [0]
    random_bytes = always_start_with_zero + random.sample(range(256), 5)
    random_octects = map(octect, random_bytes)
    return ":".join(random_octects)

if __name__ == '__main__':
    ifname = "wlan0"
    if len(sys.argv) == 2:
        ifname = sys.argv[1]
    ifconfig = Command("/sbin/ifconfig") 
    new_macaddr = random_macaddr()
    ifconfig(ifname, "down") 
    ifconfig(ifname, "hw", "ether", new_macaddr)
    ifconfig(ifname, "up")
    print "{0} mac address now is {1}".format(ifname, new_macaddr)
