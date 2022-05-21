# input = 1 to 2 liters of oil / 10 seconds
# output = .75 liters / second
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
    time_count = 0
    max_out = 0.75
    timeout = 2

    while True:
        oil_data = send("[OIL-GET]", client)
        oil_qnt = float(oil_data.split(" ")[1])

        if oil_qnt >= max_out:
            time.sleep(timeout)
            send(f"[OIL-OUT] {max_out}", client)
        elif oil_qnt < max_out and oil_qnt > 0:
            timeout = oil_qnt * max_out
            time.sleep(timeout)
            send(f"[OIL-OUT] {oil_qnt}", client)

        if time_count % 10 == 0:
            qnt_oil_recv = random.uniform(1, 2)
            print(f"[RECEIVING OIL] {qnt_oil_recv} liters")
            send(f"[OIL-SET] {qnt_oil_recv}", client)
        
        time.sleep(1)
        time_count += 1

main()