#!/usr/bin/env python
import random
import socket
import time
from urlparse import urlparse, parse_qs
import jinja2
from StringIO import StringIO
import cgi

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
    loader = jinja2.FileSystemLoader('./templates')
    env = jinja2.Environment(loader=loader)
    retval = 'HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n'
    content = ''

    response = {
                '/' : 'index.html', \
                '/content' : 'content.html', \
                '/file' : 'file.html', \
                '/image' : 'image.html', \
                '/form' : 'form.html', \
                '/submit' : 'submit.html', \
               }

    req = conn.recv(1)
    count = 0
    while req[-4:] != '\r\n\r\n':
        req += conn.recv(1)

    req, data = req.split('\r\n',1)
    headers = {}
    for line in data.split('\r\n')[:-2]:
        k, v = line.split(': ', 1)
        headers[k.lower()] = v

    path = urlparse(req.split(' ', 3)[1])

    args = parse_qs(path[4])
    if req.startswith('POST '):
        while len(content) < int(headers['content-length']):
            content += conn.recv(1)
    fs = cgi.FieldStorage(fp=StringIO(content), headers=headers, environ={'REQUEST_METHOD' : 'POST'})
    args.update(dict([(x, [fs[x].value]) for x in fs.keys()]))

    try:
        template = env.get_template(response[path[2]])
    except KeyError:
        args['path'] = path[2]
        retval = 'HTTP/1.0 404 Not Found\r\n\r\n'
        template = env.get_template('404.html')

    retval += template.render(args)
    conn.send(retval.encode('utf-8'))

    conn.close()


if __name__ == '__main__':
   main()
