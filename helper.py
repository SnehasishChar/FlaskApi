import sys

sys.path.insert(1, 'D:\daksh\TICK4.0\RestAPI_IOT')
import config as conf


INFLUX_DB_IP = '192.168.1.47'  # conf.INFLUX_DB_IP
INFLUX_DB_PORT = '8086'  # conf.INFLUX_DB_PORT
INFLUX_DB = 'EMSDatabase'  # conf.INFLUX_DB

# Sub-process/Thread count
sub_process_count = 4
