import socket
import sys

def parser(link):
    if 'https://' in link:
        print("ERROR: HTTPS / ENCRYPTED", file=sys.stderr)
        sys.exit([5])
    if 'http://' in link:
        link = link[7:]

    split = link.find('/')
    c = link.find(':')
    if c > 0:
        host = link[:c]
        port = int(link[c + 1:split])
        path = link[split:]
    elif split != -1:
        host = link[:split]
        path = link[split:]
        port = 80
    else:
        host = link
        path = '/'
        port = 80
    return host, path, port

def request(host,  path, port ):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    request = "GET %s HTTP/1.0\r\nHost: %s\r\n\r\n" % (path, host)
    s.connect((host, port))
    s.sendall(request.encode())

    response = s.recv(512)
    test = response

    while True:
        data = s.recv(512)
        if (len(data) < 1):
            break
        response = response + data

    response = response.decode("utf-8", errors="replace")
    response = response.split('\r\n\r\n')
    s.close()

    if len(response) > 1:
        return response[0], response[1]
    else:
        return response[0], 'Encrypted(HTTPS) or No HTML'

#orig = str(sys.argv[1])
orig = str(sys.argv[1])
host, path, port = parser(orig)
headers, html = request(host, path, port)

count = 0
while count < 10 and 'HTTP/1.1 302' in headers or 'HTTP/1.1 301' in headers or  'HTTP/1.0 301'in headers or 'HTTP/1.0 302' in headers:
    start = headers.find('Location')
    end = headers[start:].find('\r')
    if end == -1:
        redirect = headers[start+10:]
    else:
        redirect = headers[start+10:start+end]
    host, path, port = parser(redirect)
    headers, html = request(host, path, port)
    count = count + 1

if '200 OK' in headers:
    print(html)
    sys.exit([0])

if count == 10:
    print("300 ERROR", file=sys.stderr)
    sys.exit([3])

if '404 Not Found' in headers or '403 Forbidden' in headers:
    print(html)
    print("400 ERROR", file=sys.stderr)
    sys.exit([4])




