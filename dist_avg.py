import threading
import socket
import sys
import time
import numpy as np
import json

DEBUG_ITERATION_VALUE   = False
DEBUG_RECV_PACKAGE      = True
DEBUG_NEIGHBOR_INFO     = True

UDP_PORT        = 5011
BCAST_ADDR      = '10.0.0.255'
CONTROL_ADDR    = '10.0.0.254'
BIND_ADDR       = '0.0.0.0'

VECTOR_SIZE     = 100 

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
            if data_dict['iter'] == 0:
                print "iter = %d, cmd received." % data_dict['iter']
                if addr == CONTROL_ADDR:
                    return data_dict['cmd']
                else:
                    print "received cmd from unknown person and dropped."
            else:
                data_dict['addr'] = addr
                dist_avg(data_dict)
        except Exception as error:
            print str(error)
            print 'an unknown format package from %s and length = %s' % (str(addr), len(str(data_buffer)))
    else:
        print 'a broken packege received from %s and length = %s' % (str(addr), len(str(data_buffer)))
    return 0

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
    data_ready = 0
    iter_index = 0
    
    recv_thread = threading.Thread(target=recv_UDP)
    recv_thread.start()
    
    send_thread = threading.Thread(target=send_UDP)
    send_thread.start()
    
    start_time = time.time()
    
    recv_buffer = 'Nothing received'
    recvfrom_addr = ()

    neighbor_list = {}
    local_value = np.array([0.0] * VECTOR_SIZE)
    
    while True:
        if time.time() - start_time > TESTING_TIME_LENGTH:
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
            if data_ready == 1:
                # print 'The packet received is: ' + recv_buffer + ' from ' + str(recvfrom_addr)
                cmd = parse_buffer(recv_buffer, str(recvfrom_addr[0]))
                if cmd == CMD_TERMINATE:
                    stop_sign = 1
                else:
                    pass
                data_ready = 0
