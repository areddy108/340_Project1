import socket
import sys
import select

def parse(data):
    data = data.decode()
    return (data.split()[0], data.split()[1])

# port = int(sys.argv[1])
port = 8888
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(("", port))
print('starting up on port', port)

sock.listen(5)

connections = [sock]

while True:
    readable, writable, exceptional = select.select(connections, connections, connections)
    for s in readable:
        if s is sock:
            connection, client_address = s.accept()
            connection.setblocking(False)
            connections.append(connection)
        else:
            try:
                # Receive the data in small chunks and retransmit it
                data = s.recv(2083)
                if data:
                    method, path = parse(data)
                    path = path[1:]
                    if path == '' or method != 'GET':
                        break
                    if path[:7] == 'rfc2616' and path[-4:] != '.htm' and path[-5:] != '.html':
                        s.sendall(b'HTTP/1.0 403 Forbidden\r\n\r\n')
                    else:
                        f = open(path)
                        out = f.read()
                        f.close()
                        s.sendall(b'HTTP/1.0 200 OK\r\nContent-Type: text/html\r\n\r\n' + out.encode())
            except FileNotFoundError:
                s.sendall(b'HTTP/1.0 404 Not Found\r\n\r\n')
            finally:
                connections.remove(s)
                s.close()


