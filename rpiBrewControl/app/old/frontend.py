import CGIHTTPServer
import BaseHTTPServer
import sys, os

#os.symlink("dbFunctions.py","www/cgi/dbFunctions.py")
#os.symlink("configFunctions.py","www/cgi/configFunctions.py")

os.chdir("www")

class Handler(CGIHTTPServer.CGIHTTPRequestHandler):
    cgi_directories = ["/cgi"]         #make sure this is where you want it. [was "/cgi"]

PORT = 8000

httpd = BaseHTTPServer.HTTPServer(("", PORT), Handler)

def runserver():
    print "serving at port", PORT
    httpd.serve_forever()

import thread
thread.start_new_thread(runserver, ())

#print "opening browser"

#import webbrowser  
#url = 'http://127.0.0.1:8000/cgi/myCGI.py'
#webbrowser.open_new(url)

quit = 'n'
while not(quit=='quit'):
    quit = raw_input('\n ***Type "quit" and hit return to exit myPyServer.*** \n\n') 

print "myPyServer will now exit."

sys.exit(0)    
