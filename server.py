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
                    "oil": 5,
                    "EtOH": 5,
                    "NaOH": 5,
                    "mix": 0,
                    "cycles": 0
                },
                "decanter": {
                    "capacity": 5,
                    "status": "waiting",
                    "cycles": 0
                },
                "glycerine": 0,
                "dryer": 5,
                "washer_0": 0,
                "washer_1": 0,
                "washer_2": 0,
                "emulsion": 0,
                "bio_dryer": 5,
                "biodiesel": 0,
                "lost": 0}

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
                msg_out = msg.split(" ")
                oil_qnt = float(msg_out[1])
                element_machinery["oil"] -= oil_qnt
                element_machinery["reactor"]["oil"] += oil_qnt
                conn.send(f"[OIL->REACTOR] {oil_qnt} liter".encode(FORMAT))
                print(f"[OIL->REACTOR] {oil_qnt}")

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
                msg_out = msg.split(" ")
                etoh_qnt = float(msg_out[1])
                element_machinery["EtOH"] -= etoh_qnt
                element_machinery["reactor"]["EtOH"] += etoh_qnt
                conn.send(f"[EtOH->REACTOR] {etoh_qnt} liter".encode(FORMAT))
                print(f"[OIL->REACTOR] {etoh_qnt}")

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
                conn.send(f"[NaOH->REACTOR] {naoh_qnt} liter".encode(FORMAT))
                print(f"[NaOH->REACTOR] {naoh_qnt}")
                
            if "[NaOH-SET]" in msg:
                msg_set = msg.split(" ")
                element_machinery["NaOH"] += float(msg_set[1])
                conn.send("[NaOH RECEIVED]".encode(FORMAT))
                print(f'[NaOH RECEIVED] {element_machinery["NaOH"]} liters in total')

            # Reactor communication protocol #
            if "[REACTOR-GET]" in msg:
                conn.send(str(element_machinery["reactor"]).encode(FORMAT))
                print(f'[REACTOR-GET] {element_machinery["reactor"]}')

            if "[REACTOR-PROC]" in msg:
                msg_reactor_proc = msg.split("_")
                reactor_data = json.loads(msg_reactor_proc[1].replace("\'", "\"").strip())
                element_machinery["reactor"]["oil"] -= reactor_data["oil"]
                element_machinery["reactor"]["EtOH"] -= reactor_data["EtOH"]
                element_machinery["reactor"]["NaOH"] -= reactor_data["NaOH"]
                element_machinery["reactor"]["mix"] += reactor_data["mix"]
                element_machinery["reactor"]["cycles"] += 1
                conn.send("[REACTOR MIXING]".encode(FORMAT))
                print(f'[REACTOR PROCESSING] {element_machinery["reactor"]}')
            
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
                        print(f"[REACTOR->DECANTER] 10 liters")
                        max_transfer = 10
                        element_machinery["reactor"]["mix"] -= max_transfer
                        element_machinery["decanter"]["capacity"] += max_transfer
                        element_machinery["decanter"]["status"] = "processing"

                
                conn.send(str(element_machinery["reactor"]).encode(FORMAT))
                print(f"[REACTOR-OUT] {element_machinery['reactor']}")

            if "[DECANTER-GET]" in msg:
                conn.send(str(element_machinery["decanter"]).encode(FORMAT))
                print(f'[DECANTER-GET] {element_machinery["decanter"]}')

            if "[DECANTER-OUT]" in msg:
                decanter_out_dict = msg.split("_")
                decanter_data = json.loads(decanter_out_dict[1].replace("\'", "\"").strip())
                element_machinery["glycerine"] += decanter_data["glycerine"]
                element_machinery["dryer"] += decanter_data["EtOH"]
                element_machinery["washer_0"] += decanter_data["solution"]
                element_machinery["decanter"]["status"] = decanter_data["status"]
                element_machinery["decanter"]["capacity"] -= decanter_data["glycerine"] + decanter_data["EtOH"] + decanter_data["solution"]
                element_machinery["decanter"]["cycles"] += 1
                conn.send("[DECANTER-OUT]".encode(FORMAT))
                print(f'[DECANTER-OUT] {element_machinery["decanter"]}')

            if "[DRYER-GET]" in msg:
                conn.send(str(element_machinery["dryer"]).encode(FORMAT))
                print(f'[DRYER-GET] {element_machinery["dryer"]}')

            if "[DRYER-OUT]" in msg:
                dryer_out_dict = msg.split("_")
                dryer_data = json.loads(dryer_out_dict[1].replace("\'", "\"").strip())
                element_machinery["dryer"] -= dryer_data["dryer"]
                element_machinery["EtOH"] += dryer_data["EtOH"]
                element_machinery["lost"] += dryer_data["lost"]
                conn.send("[DRYER OUT]".encode(FORMAT))
                print(f'[DRYER OUT] {element_machinery["dryer"]}')

            if msg in ['[WASHER-GET@0]', '[WASHER-GET@1]', '[WASHER-GET@2]']:
                if "[WASHER-GET@0]" in msg:
                    conn.send(str(element_machinery["washer_0"]).encode(FORMAT))
                    print(f'[WASHER-GET@0] {element_machinery["washer_0"]}')
                elif "[WASHER-GET@1]" in msg:
                    conn.send(str(element_machinery["washer_1"]).encode(FORMAT))
                    print(f'[WASHER-GET@1] {element_machinery["washer_1"]}')
                elif "[WASHER-GET@2]" in msg:
                    conn.send(str(element_machinery["washer_2"]).encode(FORMAT))
                    print(f'[WASHER-GET@2] {element_machinery["washer_2"]}')

            if ('[WASHER-OUT@0]' in msg) or ('[WASHER-OUT@1]' in msg) or ('[WASHER-OUT@2]' in msg):
                washer_out_dict = msg.split("_")
                washer_data = json.loads(washer_out_dict[1].replace("\'", "\"").strip())
                if "[WASHER-OUT@0]" in msg:
                    element_machinery["washer_0"] -= washer_data["out-volume"] + washer_data["emulsion"]
                    element_machinery["washer_1"] += washer_data["out-volume"]
                    print(f"[WASHER-0 -> WASHER-1] {washer_data['out-volume']}")
                elif "[WASHER-OUT@1]" in msg:
                    element_machinery["washer_1"] -= washer_data["out-volume"] + washer_data["emulsion"]
                    element_machinery["washer_2"] += washer_data["out-volume"]
                    print(f"[WASHER-1 -> WASHER-2] {washer_data['out-volume']}")
                elif "[WASHER-OUT@2]" in msg:
                    element_machinery["washer_2"] -= washer_data["out-volume"] + washer_data["emulsion"]
                    element_machinery["bio_dryer"] += washer_data["out-volume"]
                    print(f"[WASHER-2 -> BIO-DRYER] {washer_data['out-volume']}")
                
                element_machinery["emulsion"] += washer_data["emulsion"]
                conn.send("[WASHER OUT]".encode(FORMAT))

            if "[BIO-DRYER-GET]" in msg:
                conn.send(str(element_machinery["bio_dryer"]).encode(FORMAT))
                print(f'[DRYER-GET] {element_machinery["bio_dryer"]}')

            if "[BIO-DRYER-OUT]" in msg:
                dryer_out_dict = msg.split("_")
                print(dryer_out_dict)
                dryer_data = json.loads(dryer_out_dict[1].replace("\'", "\"").strip())
                print(dryer_data)
                element_machinery["bio_dryer"] -= dryer_data["bio-dryer"]
                element_machinery["biodiesel"] += dryer_data["biodiesel"]
                element_machinery["lost"] += dryer_data["lost"]
                conn.send("[BIO-DRYER OUT]".encode(FORMAT))
                print(f'[BIO DRYER OUT] {element_machinery["bio_dryer"]}')

            if msg == DISCONNECT_MESSAGE:
                connected = False

            print(f"[{addr}] {msg}")
            print(element_machinery)
            #time.sleep(1)

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