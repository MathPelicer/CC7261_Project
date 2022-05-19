# input = 1 to 2 liters of oil / 10 seconds
# output = .75 liters / second

import socket
import random
import time
import platform

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
    time_count = 0

    while True:
        oil_data = send("[OIL-GET]")
        oil_qnt = float(oil_data.split(" ")[1])

        if time_count % 10 == 0:
            qnt_oil_recv = random.uniform(1, 2)
            print(f"[RECEIVING OIL] {qnt_oil_recv} liters")
            send(f"[OIL-SET] {qnt_oil_recv}")

        if oil_qnt > 0.75:
            send("[OIL-OUT]")

        time.sleep(5)
        time_count += 5

main()