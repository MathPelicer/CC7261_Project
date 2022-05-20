
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
    washer_out_dict = {}
    max_out = 1.5

    while True:
        washer_data = float(send("[WASHER-GET@1]"))
        print(f'[WASHER-GET-1] {washer_data}')

        washer_out_dict["out-volume"] = washer_data * 0.975
        
        if washer_out_dict["out-volume"] >= max_out:
            washer_out_dict["out-volume"] = max_out

        print(washer_out_dict)
            
        send(f"[WASHER-OUT@1]_{washer_out_dict}")

        time.sleep(1)
main()