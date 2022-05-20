# input = .5 liters / second
# output = max of 1 liter / second

import socket
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
    qnt_naoh_recv = 0.5
    sleep_time = 1

    while True:
        naoh_data = send("[NaOH-GET]")
        naoh_qnt = float(naoh_data.split(" ")[1])

        if naoh_qnt > 0 and naoh_qnt < 1:
            sleep_out_time = naoh_qnt * sleep_time
            time.sleep(sleep_out_time)
            send(f"[NaOH-OUT] {naoh_qnt}")
        elif naoh_qnt > 1:
            time.sleep(sleep_time)
            send(f"[NaOH-OUT] 1")

        print(f"[RECEIVING NaOH] {qnt_naoh_recv} liters")
        send(f"[NaOH-SET] {qnt_naoh_recv}")

main()