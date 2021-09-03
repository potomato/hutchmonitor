import glob
import time
import redis
import os

base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '28*')[0]
device_file = device_folder + '/w1_slave'
print(f"Device file is {device_file}")

MINS_PER_WEEK = 10080

def read_temp_raw():
    f = open(device_file, 'r')
    lines = f.readlines()
    f.close()
    return lines

def read_temp():
    lines = read_temp_raw()
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_temp_raw()
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        temp_c = float(temp_string) / 1000.0
        return temp_c

while True:
    temp=read_temp()
    print(temp)
    try:
        with redis.Redis(host=os.getenv('REDIS_HOST'), port=6379, db=0) as r:
            r.xadd('hutchtemp', { 'temp_c': temp}, maxlen=MINS_PER_WEEK)
    except BaseException as e:
        print(e)
    time.sleep(60)
