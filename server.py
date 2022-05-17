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
                "EtOH": 0}

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
                print(f'[OIL RECEIVED] {list_of_things["oil_qnt"]} liters in the tank   ')

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