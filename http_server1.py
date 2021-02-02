import socket
import sys


def parse(data):
    data = data.decode()
    return (data.split()[0], data.split()[1])


port = int(sys.argv[1])
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(("", port))
print('starting up on port', port)

sock.listen(1)

while True:
    print('waiting for a connection')
    connection, client_address = sock.accept()
    try:
        # Receive the data in small chunks and retransmit it
        data = connection.recv(2083)
        if data:
            method, path = parse(data)
            path = path[1:]
            if method != 'GET':
                break
            if path[:7] == 'rfc2616' and path[-4:] != '.htm' and path[-5:] != '.html':
                connection.sendall(b'HTTP/1.0 403 Forbidden\r\n\r\n')
            else:
                f = open(path)
                out = f.read()
                f.close()
                connection.sendall(b'HTTP/1.0 200 OK\r\nContent-Type: text/html\r\n\r\n' + out.encode())
    except FileNotFoundError:
        connection.sendall(b'HTTP/1.0 404 Not Found\r\n\r\n')
    finally:
        # Clean up the connection
        connection.close()

