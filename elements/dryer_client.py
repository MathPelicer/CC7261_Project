import socket
import time
import platform
from multiclient_functions.multiclient_functions import send

HEADER = 1024
PORT = 5050
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
SERVER_WIN = "192.168.0.6"
SERVER_LINUX = "127.0.1.1"

cur_os = platform.system()

if cur_os == "Windows":
    ADDR = (SERVER_WIN, PORT)
else:
    ADDR = (SERVER_LINUX, PORT)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)

def main():
    dryer_out_dict = {}
    standard_sleeptime = 5

    while True:
        dryer_data = float(send("[DRYER-GET]", client))
        print(f'[DRYER-GET] {dryer_data}')

        if dryer_data >= 1:
            time.sleep(standard_sleeptime)
            dryer_out_dict["dryer"] = 1
            dryer_out_dict["EtOH"] = 0.995
        else:
            sleep_time = standard_sleeptime * dryer_data
            time.sleep(sleep_time)
            dryer_out_dict["dryer"] = dryer_data
            dryer_out_dict["EtOH"] = dryer_data * 0.995

        send(f"[DRYER-OUT]_{dryer_out_dict}", client)

        time.sleep(1)

main()