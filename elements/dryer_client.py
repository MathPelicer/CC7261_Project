
import json
import socket
import random
import time
import platform

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

def send(msg):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    client.send(send_length)
    client.send(message)

    msg_recv = client.recv(2048).decode(FORMAT)
    print(msg_recv)
    return msg_recv

def main():
    dryer_out_dict = {}
    standard_sleeptime = 5

    while True:
        dryer_data = send("[DRYER-GET]")
        print(f'[DRYER-GET] {dryer_data}')

        if dryer_data >= 1:
            time.sleep(standard_sleeptime)
            dryer_out_dict["dryer"] = dryer_data - 1
            dryer_out_dict["EtOH"] = 0.95
        else:
            sleep_time = standard_sleeptime * dryer_data
            time.sleep(sleep_time)
            dryer_out_dict["dryer"] = dryer_data
            dryer_out_dict["EtOH"] = dryer_data * 0.95

        send(F"[DRYER-OUT]_{dryer_out_dict}")


main()