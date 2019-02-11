import threading
import socket
import sys
import time
import json

DEBUG_RECV_PACKAGE      = True

UDP_CMD_PORT    = 5012
BCAST_ADDR      = '172.16.0.255'
BIND_ADDR       = '172.16.0.254'

BUFFER_SIZE     = 1024

CMD_TERMINATE   = 1
CMD_START       = 2

def recv_data():
    while True:
        try:
            global sock_cmd
            global stop_sign
            if stop_sign == 1:
                break
            recv_buffer, recvfrom_addr = sock_cmd.recvfrom(BUFFER_SIZE)
            if DEBUG_RECV_PACKAGE:
                print "Received a package from %s and len = %d." %(str(recvfrom_addr), len(recv_buffer))
        except NameError:
            print 'the sock is broken.'
            break
        except socket.error as error:
            if error.errno != socket.errno.EAGAIN:
                # data not available
                print 'the sock error.'
                break

def send_cmd(cmd):
    send_data = {'cmd': cmd}
    json_data = json.dumps(send_data)
    try:
        sock_cmd.sendto(json.dumps(send_data), (BCAST_ADDR, UDP_CMD_PORT))
    except socket.error, msg:
        print 'send data failed.' + str(msg)
    except Exception as error:
        print 'Unknown error: ' + str(error)

if __name__ == '__main__':
    sock_cmd = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock_cmd.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock_cmd.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    sock_cmd.setblocking(0)
    try:
        sock_cmd.bind((BIND_ADDR, UDP_CMD_PORT))
    except Exception as error:
        print 'sock_cmd bind failed. %s' % str(error)
        sys.exit()
    
    stop_sign = 0 # for controlling the socket threads
    
    recv_thread = threading.Thread(target=recv_data)
    recv_thread.start()
    
    recv_buffer = 'Nothing received'
    recvfrom_addr = ()

    while True:
        try:
            input_str = raw_input('>> ')
        except Exception as error:
            print str(error)

        if input_str == 'stop':
            send_cmd(CMD_TERMINATE)
        elif input_str == 'start':
            send_cmd(CMD_START)
        elif input_str == 'quit':
            stop_sign = 1 # let the socket threads stop
            try:
                sock_cmd.close()
            except socket.error, msg:
                print "socket close failed."
            if recv_thread.is_alive:
                recv_thread.join()
            break
        elif input_str == 'help':
            print 'supported cmd: stop, start, quit, help'
        else:
            print 'unknown command.'

