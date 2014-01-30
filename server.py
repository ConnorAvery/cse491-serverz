#!/usr/bin/env python
import random
import socket
import time
import urlparse

def main():
    s = socket.socket()         # Create a socket object
    host = socket.getfqdn() # Get local machine name
    port = random.randint(8000, 9999)
    s.bind((host, port))        # Bind to the port

    print 'Starting server on', host, port
    print 'The Web server URL for this would be http://%s:%d/' % (host, port)

    s.listen(5)                 # Now wait for client connection.

    print 'Entering infinite loop; hit CTRL-C to exit'
    while True:
            # Establish connection with client.    
        c, (client_host, client_port) = s.accept()
        print 'Got connection from', client_host, client_port
        handle_connection(c)

def handle_connection(conn):
    request = conn.recv(1000)
    print request

    first_line = request.split('\r\n')[0].split(' ')

    request_type = first_line[0]
    print request_type
    
    try:
        parsed_url = urlparse.urlparse(first_line[1])
        path = parsed_url[2]
    except:
        path = "/404"

    #print parsed_url
    print path

    # send a response

    if request_type == "POST":
        if path == '/':
            print '//////////'
            handle_index(conn, '')
        elif path == '/submit':
            handle_submit(conn,request.split('\r\n')[-1])
    
    else:
        if path == '/':
            handle_index(conn, parsed_url)
        elif path == '/content':
            handle_content(conn, parsed_url)
        elif path == '/file':
            handle_file(conn, parsed_url)
        elif path == '/image':
            handle_image(conn, parsed_url)
        elif path == '/submit':
            handle_submit(conn,parsed_url)

    conn.close()

def handle_index(conn, parsed_url):
    conn.send('HTTP/1.0 200 OK\r\n' + \
            'Content-type: text/html\r\n' + \
            '\r\n' + \
            '<html><body>' + \
            '<h1>Hello world!</h1>This is ConnorAvery\'s Web server.' + \
            '<br/><a href="/content">Content</a>' + \
            '<br/><a href="/file">File</a>' + \
            '<br/><a href="/image">Image</a>' + \
            '</body></html>'+ \
            "<form action='/submit' method='GET'>\n" + \
            "<p>first name: <input type='text' name='firstname'></p>\n" + \
            "<p>last name: <input type='text' name='lastname'></p>\n" + \
            "<input type='submit' value='Submit'>\n\n" + \
            "</form>")
def handle_submit(conn, parsed_url):
    query = parsed_url[4]
    
    # each value is split by an &
    query = query.split("&")

    # format is name=value. We want the value.
    firstname = query[0].split("=")[1]
    lastname = query[1].split("=")[1]

    conn.send('HTTP/1.0 200 OK\r\n' + \
            'Content-type: text/html\r\n' + \
            '\r\n' + \
              "Hello Mr. %s %s." % (firstname, lastname))
    
def handle_content(conn, parsed_url):
    conn.send('HTTP/1.0 200 OK\r\n' + \
                      'Content-Type: text/html\r\n\r\n' + \
                      '<!DOCTYPE html><html><body><h1>Hello, world</h1> ' + \
                      'This is ConnorAvery\'s content page</body></html>')
def handle_image(conn, parsed_url):
    conn.send('HTTP/1.0 200 OK\r\n' + \
                      'Content-Type: text/html\r\n\r\n' + \
                      '<!DOCTYPE html><html><body><h1>Hello, world</h1> ' + \
                      'This is ConnorAvery\'s image page</body></html>'
)
def handle_file(conn, parsed_url):
    conn.send('HTTP/1.0 200 OK\r\n' + \
                      'Content-Type: text/html\r\n\r\n' + \
                      '<!DOCTYPE html><html><body><h1>Hello, world</h1> ' + \
                      'This is ConnorAvery\'s file page</body></html>')



if __name__ == '__main__':
   main()
