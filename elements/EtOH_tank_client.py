# input = .25 liters / second
# output = max of 1 liter / second

import socket
import time

HEADER = 64
PORT = 5050
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
SERVER = "192.168.0.6"
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

    msg_recv = client.recv(2048).decode(FORMAT)
    print(msg_recv)
    return msg_recv

def main():
    etoh_qnt = float(send("[EtOH-GET]"))
    print(f"[EtOH-GET] {etoh_qnt} liters")

    while True:
        qnt_etoh_recv = 0.25
        print(f"[RECEIVING EtOH] {qnt_etoh_recv} liters")
        send(f"[EtOH-SET] {qnt_etoh_recv}")

        etoh_qnt = float(send("[EtOH-GET]"))
        print(f"[EtOH-GET] {etoh_qnt} liters")

        if etoh_qnt > 0 and etoh_qnt < 1:
            send(f"[EtOH-SENT] {etoh_qnt}")
        elif etoh_qnt > 1:
            send(f"[EtOH-SENT] 1")

        time.sleep(1)

main()