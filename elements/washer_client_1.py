
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
SERVER_LINUX = "192.0.1.1"

cur_os = platform.system()

if cur_os == "Windows":
    ADDR = (SERVER_WIN, PORT)
else:
    ADDR = (SERVER_LINUX, PORT)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)

def main():
    washer_out_dict = {}
    max_out = 1.5

    while True:
        washer_data = float(send("[WASHER-GET@1]"), client)
        print(f'[WASHER-GET-1] {washer_data}')

        washer_out_dict["out-volume"] = washer_data * 0.975
        
        if washer_out_dict["out-volume"] >= max_out:
            washer_out_dict["out-volume"] = max_out

        print(washer_out_dict)
            
        send(f"[WASHER-OUT@1]_{washer_out_dict}", client)

        time.sleep(1)
main()