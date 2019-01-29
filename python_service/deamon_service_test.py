import sys
import socket

# Create a UDS socket
sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)

# Connect the socket to the port where the server is listening
server_address = '/tmp/echo1.sock'
print("Connecting to {}".format(server_address))
try:
    sock.connect(server_address)
except socket.error as msg:
    print(sys.stderr, msg)
    sys.exit(1)

try:
    
    # Send data
    message = b'This is the message.  It will be repeated.'
    print('sending "%s"' % message)
    sock.sendall(message)

    amount_received = 0
    amount_expected = len(message)
    
    while amount_received < amount_expected:
        data = sock.recv(4096)
        amount_received += len(data)
        print('received "%s"' % data)

finally:
    print('closing socket')
    sock.close()