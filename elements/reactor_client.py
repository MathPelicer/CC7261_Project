# input = 1/4 NaOh, 1/4 EtOH and 1/2 oil
# max capacity = 5 liters / second
# output = 1 liter / second

import socket
import time
import platform
import json

HEADER = 64
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
    reactor_data = send("[REACTOR-GET]")
    reactor_dict = json.loads(reactor_data.replace("\'", "\""))
    print(f'[REACTOR-GET] OIL: {reactor_dict["oil"]} | EtOH: {reactor_dict["EtOH"]} | NaOH: {reactor_dict["NaOH"]}')

    # while True:
    #     qnt_naoh_recv = 0.5
    #     print(f"[RECEIVING NaOH] {qnt_naoh_recv} liters")
    #     send(f"[NaOH-SET] {qnt_naoh_recv}")

    #     naoh_qnt = float(send("[NaOH-GET]"))
    #     print(f"[NaOH-GET] {naoh_qnt} liters")

    #     if naoh_qnt > 0 and naoh_qnt < 1:
    #         send(f"[NaOH-SENT] {naoh_qnt}")
    #     elif naoh_qnt > 1:
    #         send(f"[NaOH-SENT] 1")

    #     time.sleep(1)

main()

