import threading
import socket
import sys

def recv_UDP():
    while True:
        try:
            data, addr = sock.recvfrom(1024)
            # print "received message:", data
        except NameError:
            print 'the sock is broken.'
            sys.exit(1);
        return data

def send_UDP(data, addr):
    try:
        sock.sendto(data, (addr, UDP_PORT))
    except socket.error:
        print 'send data failed.'
        sys.exit(2);

if __name__ == '__main__':
    UDP_PORT = 5009
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        sock.bind(('0.0.0.0', UDP_PORT))
    except:
        print 'bind failed.'
        sys.exit(3)
        
    # The thread that ables the listen for UDP packets is loaded
    listen_UDP = threading.Thread(target=recv_UDP)
    listen_UDP.start()
    
    data = 'Nothing received'
    
    while True:
        send_UDP('hello', '127.0.0.1')
        print 'The packet received is: ' + data

