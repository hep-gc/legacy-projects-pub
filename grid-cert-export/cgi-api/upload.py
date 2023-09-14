#!/usr/local/bin/python

import cgi, subprocess, os, random, string
from datetime import datetime

#--------------------- READ ME FIRST! --------------------------
# Since this script will return the private key as the responce to the POST
# reqest from the client, this should be only hosted over a SECURE SSL connection!
#---------------------------------------------------------------

#CGI traceback (enable FOR DEBUG ONLY)
#import cgitb
#cgitb.enable()

# Location of OpenSSL binary (full path)
OPEN_SSL_PATH = "/usr/bin/openssl"

# Location of logfile - logging disabled if None (apache needs write permissions to this)
LOG_FILE = None

BORDER = "########PRIVATE KEY ENDS HERE - CERTIFICATE BEGINS HERE########"

def main():
    #Necassary Headers
    print "Content-Type: text/html"
    #blank line indicates end of headers
    print              
    
    form = cgi.FieldStorage()

    #The second line of checks shouldn't be necessary since empty values are not supposed
    # to be included in the dictionary (according to Python Docs), but for some reason they are...
    if "pwd_in" not in form or "pwd_out" not in form or "certificate" not in form\
    or form["pwd_in"].value == "" or form["pwd_out"].value == "" or not form["certificate"].filename:
        print "<H1>Error: Missing certificate or password(s)</H1>"
        cgi.print_environ()
        
    else:
        file = form["certificate"].file
        pkcs12_data = file.read()

        #The file descriptors for the password pipe
        rfd,wfd = os.pipe()
        
        #######Create the Private Key#######
        
        #The openSSL command, reading the PKCS12 from stdin (fd:0) and reading passwords from rfd end of a pipe
        #Passwords get input one per line (see openssl manpages under "PASS PHRASE ARGUMENTS" for details)
        arguments = [OPEN_SSL_PATH, "pkcs12", "-nocerts", "-passin", "fd:" + str(rfd), "-passout", "fd:" + str(rfd)]
        #Start the openssl process
        proc = subprocess.Popen(arguments, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        #Write passwords to the password pipe
        os.write(wfd, form["pwd_in"].value + "\n" + form["pwd_out"].value + "\n")
        #Write the data to stdin pipe for openssl and close it to send EOF
        proc.stdin.write(pkcs12_data)
        proc.stdin.close()

        privkey = proc.stdout.read()
        error = proc.stderr.read()
        
        if not privkey:
            print "openssl private key generation error: ",
            print error,
            return
        else:
            print privkey,
            
        ###########Create the Certificate########
        arguments = [OPEN_SSL_PATH, "pkcs12", "-clcerts", "-passin", "fd:" + str(rfd)]
        proc = subprocess.Popen(arguments, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        os.write(wfd, form["pwd_in"].value + "\n");
        proc.stdin.write(pkcs12_data)
        proc.stdin.close()
        
        cert_noText = proc.stdout.read()
        error = proc.stderr.read()
        
        if not cert_noText:
            print "openssl certificate generation error:"
            print error,

        ###########Create the Certificate WITH human readable text########
        arguments = [OPEN_SSL_PATH, "x509", "-text"]
        proc = subprocess.Popen(arguments, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        proc.stdin.write(cert_noText)
        proc.stdin.close()
        
        cert = proc.stdout.read()
        error = proc.stderr.read()
        
        if not cert:
            print "openssl cert with text generation error:"
            print error,
        else:
            print BORDER,
            print cert,
        
        ###########Log the current date/time and  DN + email for certificate ########
        if LOG_FILE:
            arguments = [OPEN_SSL_PATH, "x509", "-noout", "-issuer", "-subject", "-email"]
            proc = subprocess.Popen(arguments, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            proc.stdin.write(cert_noText)
            proc.stdin.close()

            data = proc.stdout.read()
            error = proc.stderr.read()

            logfile = open(LOG_FILE, "a")
            if not data:
                logfile.write(error)
            else:
                logfile.write("\n### " + str(datetime.now()) + " ###\n" + data)
            logfile.close()

        #We don't need the password pipe anymore, clean up the open file descriptors
        os.close(rfd)
        os.close(wfd)
        
if __name__ == "__main__":
    main()    
