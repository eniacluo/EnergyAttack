import threading
import socket
import sys
import time
import numpy as np

UDP_PORT = 5011
SEND_ADDR = '127.0.0.1'
BIND_ADDR = '0.0.0.0'
    
def recv_UDP():
    while True:
        try:
            global recv_buffer
            global sock
            global stop_sign
            time.sleep(0.1)
            if stop_sign == 1:
                break
            recv_buffer, addr = sock.recvfrom(1024)
            # print "received message:", data
        except NameError:
            print 'the sock is broken.'
            sys.exit(1);

def send_UDP():
    global addr
    global sock
    global stop_sign
    while True:
        time.sleep(0.5)
        data = str(np.random.normal(size=3))
        try:
            if stop_sign == 1:
                break
            sock.sendto(data, (SEND_ADDR, UDP_PORT))
        except socket.error:
            print 'send data failed.'
            sys.exit(2);

if __name__ == '__main__':
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    try:
        sock.bind((BIND_ADDR, UDP_PORT))
    except:
        print 'bind failed.'
        sys.exit(3)
    
    stop_sign = 0 # for controlling the socket threads
    
    recv_thread = threading.Thread(target=recv_UDP)
    recv_thread.start()
    
    send_thread = threading.Thread(target=send_UDP)
    send_thread.start()
    
    start_time = time.time()
    
    recv_buffer = 'Nothing received'
    
    while True:
        time.sleep(0.2)
        if time.time() - start_time > 5:
            stop_sign = 1 # let the socket threads stop
            recv_thread.join()
            send_thread.join()
            try:
                sock.close()
            except socket.error, msg:
                print "socket close failed."
            break
        else:
            print 'The packet received is: ' + recv_buffer

