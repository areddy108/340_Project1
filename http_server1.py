import socket
import sys

def parse(data):
    data = data.decode()
    return data.split()[1]

port = int(sys.argv[1])
#port = 10000
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(("", port))
print('starting up on port', port)

sock.listen(1)

while True:
    print('waiting for a connection')
    connection, client_address = sock.accept()
    try:
        #print('client connected:', client_address)
        # Receive the data in small chunks and retransmit it
        data = connection.recv(32)
        if data:
            #print('sending data back to the client')
            path = parse(data)
            f = open(path[1:])
            out = f.read()
            f.close()
            connection.sendall(b'HTTP/1.0 200 OK\r\nContent-Type: text/html\r\n')
            for l in out:
                connection.sendall(l.encode())
            #connection.sendall(data)
    except FileNotFoundError:
        connection.sendall(b'HTTP/1.0 404 Not Found\r\n')
    finally:
        # Clean up the connection
        connection.close()

