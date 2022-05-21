# input = .25 liters / second
# output = max of 1 liter / second

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

    while True:
        etoh_data = send("[EtOH-GET]", client)
        etoh_qnt = float(etoh_data.split(" ")[1])

        if etoh_qnt > 0 and etoh_qnt < 1:
            send(f"[EtOH-OUT] {etoh_qnt}", client)
        elif etoh_qnt > 1:
            send(f"[EtOH-OUT] 1", client)

        qnt_etoh_recv = 0.25
        print(f"[RECEIVING EtOH] {qnt_etoh_recv} liters")
        send(f"[EtOH-SET] {qnt_etoh_recv}", client)

        time.sleep(1)

main()