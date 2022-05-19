import socket 
import threading
import json
import time

HEADER = 1024
PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"

element_machinery = {"oil": 0,
                "EtOH": 0,
                "NaOH": 0,
                "reactor": {
                    "oil": 3,
                    "EtOH": 1,
                    "NaOH": 1,
                    "mix": 0
                },
                "decanter": {
                    "capacity": 0,
                    "status": "waiting"
                },
                "glycerine": 0,
                "dryer": 0,
                "washer": 0}

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
            if "[OIL-GET]" in msg:
                conn.send(f'[OIL-GET] {element_machinery["oil"]}'.encode(FORMAT))
                print(f'[OIL-GET] {element_machinery["oil"]}')

            if "[OIL-OUT]" in msg:
                element_machinery["oil"] -= 0.75
                element_machinery["reactor"]["oil"] += 0.75
                conn.send("[OIL->REACTOR] 0.75 liter".encode(FORMAT))

            if "[OIL-SET]" in msg:
                msg_set = msg.split(" ")
                element_machinery["oil"] += float(msg_set[1])
                conn.send("[OIL RECEIVED IN RESERVOIR]".encode(FORMAT))
                print(f'[OIL RECEIVED] {element_machinery["oil"]} liters in total')

            # EtOH communication protocol #

            if "[EtOH-GET]" in msg:
                conn.send(f'[EtOH-GET] {element_machinery["EtOH"]}'.encode(FORMAT))
                print(f'[EtOH-GET] {element_machinery["EtOH"]}')

            if "[EtOH-OUT]" in msg:
                msg_set = msg.split(" ")
                etoh_qnt = float(msg_set[1])
                element_machinery["EtOH"] -= etoh_qnt
                element_machinery["reactor"]["EtOH"] += etoh_qnt
                conn.send(f"[EtOH->REACTOR] {msg_set[1]} liter".encode(FORMAT))

            if "[EtOH-SET]" in msg:
                msg_set = msg.split(" ")
                element_machinery["EtOH"] += float(msg_set[1])
                conn.send("[EtOH RECEIVED]".encode(FORMAT))
                print(f'[EtOH RECEIVED] {element_machinery["EtOH"]} liters in total')

            # NaOH communication protocol #

            if "[NaOH-GET]" in msg:
                conn.send(f'[NaOH-GET] {element_machinery["NaOH"]}'.encode(FORMAT))
                print(f'[NaOH-GET] {element_machinery["NaOH"]}')

            if "[NaOH-OUT]" in msg:
                msg_set = msg.split(" ")
                naoh_qnt = float(msg_set[1])
                element_machinery["NaOH"] -= naoh_qnt
                element_machinery["reactor"]["NaOH"] += naoh_qnt
                conn.send(f"[NaOH->REACTOR] {msg_set[1]} liter".encode(FORMAT))
                
            if "[NaOH-SET]" in msg:
                msg_set = msg.split(" ")
                element_machinery["NaOH"] += float(msg_set[1])
                conn.send("[NaOH RECEIVED]".encode(FORMAT))
                print(f'[NaOH RECEIVED] {element_machinery["NaOH"]} liters in total')

            # REactor communication protocol #

            if "[REACTOR-GET]" in msg:
                conn.send(str(element_machinery["reactor"]).encode(FORMAT))
                print(f'[REACTOR-GET] {element_machinery["reactor"]}')

            if "[REACTOR-PROC]" in msg:
                msg_reactor_proc = msg.split("_")
                print(msg_reactor_proc[1].replace("\'", "\""))
                reactor_data = json.loads(msg_reactor_proc[1].replace("\'", "\"").strip())
                element_machinery["reactor"] = reactor_data
                conn.send("[REACTOR MIXING]".encode(FORMAT))
                print(f'[REACTOR MIX] {element_machinery["reactor"]}')
            
            if "[REACTOR-OUT]" in msg:
                msg_out = msg.split(" ")
                while element_machinery["decanter"]["status"] != "waiting":
                    print("[REACTOR] Waiting for decanter...")
                    time.sleep(1)

                if element_machinery["decanter"]["status"] == "waiting":
                    if element_machinery["decanter"]["capacity"] + float(msg_out[1]) <= 10:
                        print(f"[REACTOR->DECANTER] {msg_out[1]} liters")
                        time.sleep(int(float(msg_out[1])))
                        element_machinery["reactor"]["mix"] -= float(msg_out[1])
                        element_machinery["decanter"]["capacity"] += float(msg_out[1])
                        element_machinery["decanter"]["status"] = "processing"
                    else:
                        print("DO SOMETHING HERE, GREATER THAN THE MAX CAPACITY")
                
                conn.send(str(element_machinery["reactor"]).encode(FORMAT))

            if "[DECANTER-GET]" in msg:
                conn.send(str(element_machinery["decanter"]).encode(FORMAT))
                print(f'[DECANTER-GET] {element_machinery["decanter"]}')

            if "[DECANTER-OUT]" in msg:
                decanter_out_dict = msg.split("_")
                print(decanter_out_dict[1].replace("\'", "\""))
                decanter_data = json.loads(decanter_out_dict[1].replace("\'", "\"").strip())
                element_machinery["glycerine"] = decanter_data["glycerine"]
                element_machinery["dryer"] = decanter_data["EtOH"]
                element_machinery["washer"] = decanter_data["solution"]
                element_machinery["decanter"]["status"] = decanter_data["status"]
                conn.send("[DECANTER OUT]".encode(FORMAT))
                print(f'[DECANTER OUT] {element_machinery["decanter"]}')

            if "[DRYER-GET]" in msg:
                conn.send(str(element_machinery["dryer"].encode(FORMAT)))
                print(f'[DRYER-GET] {element_machinery["dryer"]}')

            if msg == DISCONNECT_MESSAGE:
                connected = False

            print(f"[{addr}] {msg}")
            print(element_machinery)

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