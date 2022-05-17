import socket 
import threading

HEADER = 64
PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
oil_qnt = 0
list_of_things = {"oil_qnt": 0,
                "EtOH": 0,
                "NaOH": 0}

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

def handle_client(conn, addr):
    
    
    print(f"[NEW CONNECTION] {addr} connected.")

    connected = True
    while connected:
        msg_length = conn.recv(HEADER).decode(FORMAT)
        if msg_length:
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT)

            # OIL communication protocol #

            if "[OIL-SENT]" in msg:
                list_of_things["oil_qnt"] -= 0.75
                conn.send("[OIL->REACTOR] 0.75 liter of oil".encode(FORMAT))

            if "[OIL-GET]" in msg:
                conn.send(str(list_of_things["oil_qnt"]).encode(FORMAT))
                print(f'[OIL-GET] {list_of_things["oil_qnt"]}')

            if "[OIL-SET]" in msg:
                msg_set = msg.split(" ")
                list_of_things["oil_qnt"] += float(msg_set[1])
                conn.send("[OIL RECEIVED IN RESERVOIR]".encode(FORMAT))
                print(f'[OIL RECEIVED] {list_of_things["oil_qnt"]} liters in total')

            # EtOH communication protocol #

            if "[EtOH-GET]" in msg:
                conn.send(str(list_of_things["EtOH"]).encode(FORMAT))
                print(f'[EtOH-GET] {list_of_things["EtOH"]}')

            if "[EtOH-SENT]" in msg:
                msg_set = msg.split(" ")
                list_of_things["EtOH"] -= float(msg_set[1])
                conn.send(f"[EtOH->REACTOR] {msg_set[1]} liter".encode(FORMAT))

            if "[EtOH-SET]" in msg:
                msg_set = msg.split(" ")
                list_of_things["EtOH"] += float(msg_set[1])
                conn.send("[EtOH RECEIVED]".encode(FORMAT))
                print(f'[EtOH RECEIVED] {list_of_things["EtOH"]} liters in total')

            # NaOH communication protocol #

            if "[NaOH-GET]" in msg:
                conn.send(str(list_of_things["NaOH"]).encode(FORMAT))
                print(f'[NaOH-GET] {list_of_things["NaOH"]}')

            if "[NaOH-SENT]" in msg:
                msg_set = msg.split(" ")
                list_of_things["NaOH"] -= float(msg_set[1])
                conn.send(f"[NaOH->REACTOR] {msg_set[1]} liter".encode(FORMAT))

            if "[NaOH-SET]" in msg:
                msg_set = msg.split(" ")
                list_of_things["NaOH"] += float(msg_set[1])
                conn.send("[NaOH RECEIVED]".encode(FORMAT))
                print(f'[NaOH RECEIVED] {list_of_things["NaOH"]} liters in total')

            if msg == DISCONNECT_MESSAGE:
                connected = False

            print(f"[{addr}] {msg}")

    conn.close()
        

def start():
    server.listen()
    print(f"[LISTENING] Server is listening on {SERVER}")
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")


print("[STARTING] server is starting...")
start()