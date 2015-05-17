import Queue
import threading
import os
import urllib2
import sys

#default values
threads = 10
target    = "http://www.blackpython.com"
directory = "/Users/Mark/Downloads/Joomla_3.4.1"
filters   = [".jpg", ".gif", "png", ".css"]

try:
    target, directory, num_threads, filters = sys.argv[1:]
except:
    print "Incorrect usage: python web_app_mapper target directory num_threads [filters]"
    print "Using default values"

os.chdir(directory)

web_paths = Queue.Queue()

for r, d, f in os.walk("."):
    """
    os.walk() returns a tuple of 3 values
    r: directory path
    d: directory names
    f: file names
    """
    for files in f:
        remote_path = "%s/%s" % (r, files)
        if remote_path.startswith("."):
            remote_path = remote_path[1:]
        if os.path.splitext(files)[1] not in filters:
            web_paths.put(remote_path)

def test_remote():
    while not web_paths.empty():
        path = web_paths.get()
        url = "%s%s" %(target, path)

        request = urllib2.Request(url)

        try:
            response = urllib2.urlopen(request)
            content  = response.read()

            print "[%d] => %s" % (response.code,path)
            response.close()
        except:
            pass

for i in range(threads):
    print "Spawning thread: %d" % i
    t = threading.Thread(target=test_remote)
    t.start()
