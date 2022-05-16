# input = 1 to 2 liters of oil / 10 seconds
# output = .75 liters / second

import socket
import random
import time

HEADER = 64
PORT = 5050
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
SERVER = "127.0.1.1"
ADDR = (SERVER, PORT)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)

def send(msg):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    client.send(send_length)
    client.send(message)
    print(client.recv(2048).decode(FORMAT))

def main():
    time_count = 0

    while True:
        qnt_oil_recv = random.uniform(1, 2)
        time.sleep(1)

        if time_count % 10 == 0:
            print(f"[RECEIVING OIL] {qnt_oil_recv} liters")
            send("[OIL] sending oil...")
        
        time_count += 1


main()