import server

class FakeConnection(object):
    """
    A fake connection class that mimics a real TCP socket for the purpose
    of testing socket I/O.
    """
    def __init__(self, to_recv):
        self.to_recv = to_recv
        self.sent = ""
        self.is_closed = False

    def recv(self, n):
        if n > len(self.to_recv):
            r = self.to_recv
            self.to_recv = ""
            return r
            
        r, self.to_recv = self.to_recv[:n], self.to_recv[n:]
        return r

    def send(self, s):
        self.sent += s

    def close(self):
        self.is_closed = True

# Test a basic GET call.

def test_handle_connection():
    conn = FakeConnection("GET / HTTP/1.0\r\n\r\n")
    expected_return = 'HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n<html>\n\t<body>\n\t\t<h1>Hello, world</h1>\n\t\tThis is ConnorAvery\'s web server.<br />\n\t\t<a href=\'/content\'>Content</a><br />\n\t\t<a href=\'/file\'>Files</a><br />\n\t\t<a href=\'/image\'>Images</a><br />\n\t</body>\n</html>\n<form action=\'/submit\' method=\'GET\'>\n            <p>first name: <input type=\'text\' name=\'firstname\'></p>\n            <p>last name: <input type=\'text\' name=\'lastname\'></p>\n            <input type=\'submit\' value=\'Submit\'>\n</form>'

    server.handle_connection(conn)

    assert conn.sent == expected_return, 'Got: %s' % (repr(conn.sent),)

def test_handle_connection_content():
    conn = FakeConnection("GET /content HTTP/1.0\r\n\r\n")
    expected_return = 'HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n<html>\n\t<body>\n\t\t<h1>Content Page</h1>\n\t\tContent<br />\n\t</body>\n</html>'
    server.handle_connection(conn)

    assert conn.sent == expected_return, 'Got: %s' % (repr(conn.sent),)

def test_handle_connection_file():
    conn = FakeConnection("GET /file HTTP/1.0\r\n\r\n")
    expected_return = 'HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n<html>\n\t<body>\n\t\t<h1>File Page</h1>\n\t\tFile<br />\n\t</body>\n</html>'
    server.handle_connection(conn)

    assert conn.sent == expected_return, 'Got: %s' % (repr(conn.sent),)
    
def test_handle_connection_image():
    conn = FakeConnection("GET /image HTTP/1.0\r\n\r\n")
    expected_return = 'HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n<html>\n\t<body>\n\t\t<h1>Image Page</h1>\n\t\tImage<br />\n\t</body>\n</html>'
    

    server.handle_connection(conn)

    assert conn.sent == expected_return, 'Got: %s' % (repr(conn.sent),)

def test_post_submit():
    conn = FakeConnection("GET /submit?firstname=First&lastname=Last " + \
                          "HTTP/1.1\r\n\r\n")
    expected_return = 'HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n<html>\n\t<body>\n\t\t<h1>Hello Mr. First Last</h1>\n\t</body>\n</html>'

    server.handle_connection(conn)

    assert conn.sent == expected_return, 'Got: %s' % (repr(conn.sent),)
