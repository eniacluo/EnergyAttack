import threading
import socket
import sys
import time
import numpy as np

UDP_PORT = 5011
BCAST_ADDR = '10.0.0.255'
BIND_ADDR = '0.0.0.0'

VECTOR_SIZE = 1
    
def recv_UDP():
    while True:
        try:
            global recv_buffer
            global recvfrom_addr
            global sock
            global stop_sign
            time.sleep(0.1)
            if stop_sign == 1:
                break
            recv_buffer, recvfrom_addr = sock.recvfrom(1024)
        except NameError:
            print 'the sock is broken.'
            break
        except socket.error as error:
            if error.errno != socket.errno.EAGAIN:
                # data not available
                print 'the sock error.'
                break

def send_UDP():
    global addr
    global sock
    global stop_sign
    while True:
        time.sleep(0.5)
        data = str(np.random.normal(size=VECTOR_SIZE))
        try:
            if stop_sign == 1:
                break
            sock.sendto(data, (BCAST_ADDR, UDP_PORT))
        except socket.error:
            print 'send data failed.'
            break
        except:
            print 'Unknown error.'
            break

if __name__ == '__main__':
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    sock.setblocking(0)
    try:
        sock.bind((BIND_ADDR, UDP_PORT))
    except:
        print 'bind failed.'
        sys.exit()
    
    stop_sign = 0 # for controlling the socket threads
    
    recv_thread = threading.Thread(target=recv_UDP)
    recv_thread.start()
    
    send_thread = threading.Thread(target=send_UDP)
    send_thread.start()
    
    start_time = time.time()
    
    recv_buffer = 'Nothing received'
    recvfrom_addr = ()
    
    while True:
        time.sleep(0.2)
        if time.time() - start_time > 5:
            stop_sign = 1 # let the socket threads stop
            try:
                sock.close()
            except socket.error, msg:
                print "socket close failed."
            if recv_thread.is_alive:
                recv_thread.join()
            if send_thread.is_alive:
                send_thread.join()
            break
        else:
            print 'The packet received is: ' + recv_buffer + ' from ' + str(recvfrom_addr)

