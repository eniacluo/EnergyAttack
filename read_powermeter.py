#!/usr/bin/python

from ina219 import INA219, DeviceRangeError
import time
import subprocess
import sys
from thread import start_new_thread
 
SHUNT_OHMS = 0.1
MAX_EXPECTED_AMPS = 2.0
ina = INA219(SHUNT_OHMS, MAX_EXPECTED_AMPS)
ina.configure(ina.RANGE_16V)

BUFFER_SIZE = 500
SAMPLE_INTERVAL = 0.01

def collect_data(buf,ina,buf_index):
    power = ina.power()
    buf[buf_index] = [time.time(), power/1000]
    buf_index += 1
    return [buf, buf_index]

def send_data(buf):
    try:
        data_chunk = ""
        for b in buf:
            data_time = str(int(b[0]*1e9))
            data_value = str(b[1])
            data_chunk += "PSVirPower,type=PSVirPower value=%s %s\n" % (data_value, data_time)
        url = "http://localhost:8086/write?db=energy_meter"
        http_post = "curl -i -XPOST \'%s\' --data-binary \'%s\'" % (url, data_chunk)
        subprocess.call(http_post, shell=True)
    except DeviceRangeError as e:
        # Current out of device range with specified shunt resister
        print(e)

buf1 = [[0, 0]] * BUFFER_SIZE
buf0 = [[0, 0]] * BUFFER_SIZE
buf0_index = 0
buf1_index = 0
flag = 0
starttime = time.time()

# Double buffer to send data
while True:
    if flag == 1:
        [buf1, buf1_index] = collect_data(buf1, ina, buf1_index)
        if buf1_index == BUFFER_SIZE:
            try:
                start_new_thread(send_data, (buf1, ) )
                buf1_index = 0
            except:
                print "Error: unable to start thread"
            flag = 0
    else:
        [buf0, buf0_index] = collect_data(buf0, ina, buf0_index)
        if buf0_index == BUFFER_SIZE:
            try:
                start_new_thread(send_data, (buf0, ) )
                buf0_index = 0
            except:
                print "Error: unable to start thread"
            flag = 1
    time.sleep(SAMPLE_INTERVAL - ((time.time() - starttime) % SAMPLE_INTERVAL))

