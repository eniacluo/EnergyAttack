import threading
import socket
import sys
import time
import numpy as np
import json

DEBUG_ITERATION_VALUE   = False
DEBUG_RECV_PACKAGE      = True
DEBUG_NEIGHBOR_INFO     = True
DEBUG_CONTROL_ENABLE    = True

UDP_PORT        = 5011
UDP_CMD_PORT    = 5012
BCAST_ADDR      = '10.0.0.255'
CONTROL_ADDR    = '172.16.0.254'
BIND_ADDR       = '0.0.0.0'

VECTOR_SIZE     = 100 
BUFFER_SIZE     = 1024

CMD_TERMINATE   = 1
CMD_START       = 2

# how long does the program runs
TESTING_TIME_LENGTH = 60

# how many points to print of np array
np.set_printoptions(threshold = 20)

def recv_UDP():
    while True:
        try:
            global recv_buffer
            global recvfrom_addr
            global sock
            global stop_sign
            global data_ready
            if stop_sign == 1:
                break
            recv_buffer, recvfrom_addr = sock.recvfrom(VECTOR_SIZE * 80)
            if DEBUG_RECV_PACKAGE:
                print "Received a package from %s and len = %d." %(str(recvfrom_addr), len(recv_buffer))
            data_ready = 1
        except NameError:
            print 'the sock is broken when recv.'
            break
        except socket.error as error:
            if error.errno != socket.errno.EAGAIN:
                # data not available
                print 'the sock error. %s' % str(error)
                break

def send_UDP():
    global addr
    global sock
    global stop_sign
    global iter_index
    while True:
        time.sleep(0.5)
        value = [float(x) for x in np.random.normal(size=VECTOR_SIZE)]
        send_data = {'iter': iter_index, 'data': value, 'time': time.time()}
        json_data = json.dumps(send_data)
        try:
            if stop_sign == 1:
                break
            sock.sendto(json.dumps(send_data), (BCAST_ADDR, UDP_PORT))
            iter_index = iter_index + 1
        except socket.error, msg:
            print 'send data failed.' + str(msg)
            break
        except Exception as error:
            print 'Unknown error: ' + str(error)
            break

def dist_avg(data_dict):
    global neighbor_list
    global local_value
    # neighbor_list format: {'10.0.0.1': <vec1>, 
    #                       '10.0.0.2': <vec2>, ...}
    neighbor_list[data_dict['addr']] = data_dict['data']
    all_vectors = np.array([0.0] * VECTOR_SIZE)
    for vector in neighbor_list.values():
        all_vectors = all_vectors + np.array(vector)
    local_value = all_vectors / len(neighbor_list)
    if DEBUG_ITERATION_VALUE:
        print '---iter = %d---\nvalue = \n%s' % (data_dict['iter'], (local_value))

def parse_buffer(data_buffer, addr):
    data_dict = json.loads(data_buffer)
    if type(data_dict) == dict:
        try:
            if data_dict['iter'] != 0:
                data_dict['addr'] = addr
                dist_avg(data_dict)
            else:
                print "iter = %d received." % data_dict['iter']
        except Exception as error:
            print str(error)
            print 'an unknown format package from %s and length = %s' % (str(addr), len(str(data_buffer)))
    else:
        print 'a broken packege received from %s and length = %s' % (str(addr), len(str(data_buffer)))
    return 0

def recv_cmd():
    while True:
        try:
            global sock_cmd
            global stop_sign
            global cmd_ready
            global cmd
            if stop_sign == 1:
                break
            cmd_buffer, cmd_addr = sock_cmd.recvfrom(BUFFER_SIZE)
            if cmd_addr[0] == CONTROL_ADDR:
                try:
                    cmd_dict = json.loads(cmd_buffer)
                    if type(cmd_dict) == dict:
                        print 'cmd: %d' % cmd_dict['cmd']
                        cmd = cmd_dict['cmd']
                        cmd_ready = 1
                    else:
                        print 'a broken packege received from %s and length = %s' % (str(cmd_addr), len(str(cmd_buffer)))
                except Exception as error:
                    print str(error)
                    print 'an unknown format package from %s and length = %s' % (str(cmd_addr), len(str(cmd_buffer)))
            else:
                print 'an package from unknown address %s and length = %s' % (str(cmd_addr), len(str(cmd_buffer)))
            if DEBUG_RECV_PACKAGE:
                print "Received a package from %s and len = %d." %(str(cmd_addr), len(cmd_buffer))
        except NameError as error:
            print 'the sock is broken. %s' % str(error)
            break
        except socket.error as error:
            if error.errno != socket.errno.EAGAIN:
                # data not available
                print 'the sock error. %s' % str(error)
                break


if __name__ == '__main__':
    # sock for data exchange
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    sock.setblocking(0)
    try:
        sock.bind((BIND_ADDR, UDP_PORT))
    except Exception as error:
        print 'sock bind failed. %s' % str(error)
        sys.exit()
    
    if DEBUG_CONTROL_ENABLE == True:
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
    data_ready = 0
    iter_index = 0
    
    recv_thread = threading.Thread(target=recv_UDP)
    recv_thread.start()
    
    send_thread = threading.Thread(target=send_UDP)
    send_thread.start()
   
    if DEBUG_CONTROL_ENABLE == True:
        cmd_ready = 0
        cmd = 0
        recv_cmd_thread = threading.Thread(target=recv_cmd)
        recv_cmd_thread.start()

    start_time = time.time()
    
    recv_buffer = 'Nothing received'
    recvfrom_addr = ()

    neighbor_list = {}
    local_value = np.array([0.0] * VECTOR_SIZE)
    
    while True:
        if time.time() - start_time > TESTING_TIME_LENGTH or stop_sign == 1:
            stop_sign = 1 # let the socket threads stop
            try:
                sock.close()
                if DEBUG_CONTROL_ENABLE == True:
                    sock_cmd.close()
            except socket.error, msg:
                print "socket close failed."
            if recv_thread.is_alive:
                recv_thread.join()
            if send_thread.is_alive:
                send_thread.join()
            if DEBUG_CONTROL_ENABLE == True:
                if recv_cmd_thread.is_alive:
                    recv_cmd_thread.join()
            break
        else:
            if data_ready == 1:
                # print 'The packet received is: ' + recv_buffer + ' from ' + str(recvfrom_addr)
                parse_buffer(recv_buffer, str(recvfrom_addr[0]))
                data_ready = 0
            if cmd_ready == 1:
                if cmd == CMD_TERMINATE:
                    stop_sign = 1
                else:
                    pass
                cmd_ready = 0

