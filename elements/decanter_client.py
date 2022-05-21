# input = 1 liter / second coming from the reactor
# condition = needs to rest for 5 seconds

import json
import socket
import random
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
    max_capacity = 10
    decanter_time = 5

    while True:
        decanter_out_dict = {}

        decanter_data = send("[DECANTER-GET]", client)
        decanter_dict = json.loads(decanter_data.replace("\'", "\""))
        print(f'[DECANTER-GET] CAPACITY: {decanter_dict["capacity"]} | STATUS: {decanter_dict["status"]}')

        if decanter_dict['status'] == "processing":
            print(f"waiting {decanter_time} to process")
            time.sleep(decanter_time)
            decanter_out_dict["glycerine"] = decanter_dict["capacity"] * 0.01
            decanter_out_dict["EtOH"] = decanter_dict["capacity"] * 0.03
            decanter_out_dict["solution"] = decanter_dict["capacity"] * 0.96

            decanter_out_dict["status"] = "waiting"
            
            send(f"[DECANTER-OUT]_{decanter_out_dict}", client)

        time.sleep(1)

main()