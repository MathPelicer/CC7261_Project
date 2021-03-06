# input = 1/4 NaOh, 1/4 EtOH and 1/2 oil
# max capacity = 5 liters / second
# output = 1 liter / second

import socket
import time
import platform
import json
from multiclient_functions.multiclient_functions import send

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

def main():
    quarter_mix = 1.25
    half_mix = 2.5
    max_mix = 5

    while True:
        reactor_data = send("[REACTOR-GET]", client)
        reactor_dict = json.loads(reactor_data.replace("\'", "\""))
        print(f'[REACTOR-GET] OIL: {reactor_dict["oil"]} | EtOH: {reactor_dict["EtOH"]} | NaOH: {reactor_dict["NaOH"]} | MIX: {reactor_dict["mix"]}')

        mix_value = reactor_dict["mix"]
        reactor_dict.pop("mix")
        reactor_dict.pop("cycles")
        smallest_element = min(reactor_dict, key=reactor_dict.get)
        
        if smallest_element == 'NaOH' or smallest_element == 'EtOH':
            smallest_qnt = float(reactor_dict[smallest_element])

            if smallest_qnt >= quarter_mix and (reactor_dict["oil"] >= (smallest_qnt * 2)):
                reactor_dict["EtOH"] = quarter_mix
                reactor_dict["NaOH"] = quarter_mix
                reactor_dict["oil"] = half_mix
                reactor_dict["mix"] = max_mix
                print(f'[REACTOR-MIX] OIL: {reactor_dict["oil"]} | EtOH: {reactor_dict["EtOH"]} | NaOH: {reactor_dict["NaOH"]} | MIX: {reactor_dict["mix"]}')
                time.sleep(max_mix)
                send(f"[REACTOR-PROC]_{reactor_dict}", client)

            elif smallest_qnt < quarter_mix and smallest_qnt > 0 and (reactor_dict["oil"] >= (smallest_qnt * 2)):
                reactor_dict["EtOH"] = smallest_qnt
                reactor_dict["NaOH"] = smallest_qnt
                reactor_dict["oil"] = smallest_qnt * 2
                reactor_dict["mix"] = (smallest_qnt * 4)
                print(f'[REACTOR-MIX] OIL: {reactor_dict["oil"]} | EtOH: {reactor_dict["EtOH"]} | NaOH: {reactor_dict["NaOH"]} | MIX: {reactor_dict["mix"]}')
                time.sleep(smallest_qnt * 4)
                send(f"[REACTOR-PROC]_{reactor_dict}", client)
            
            else:
                reactor_dict["mix"] = mix_value

        elif smallest_element == 'oil':
            smallest_qnt = float(reactor_dict[smallest_element])

            if smallest_qnt <= half_mix:

                reactor_dict["EtOH"] = smallest_qnt / 2
                reactor_dict["NaOH"] = smallest_qnt / 2
                reactor_dict["oil"] = smallest_qnt
                reactor_dict["mix"] = (smallest_qnt * 4)
                print(f'[REACTOR-MIX] OIL: {reactor_dict["oil"]} | EtOH: {reactor_dict["EtOH"]} | NaOH: {reactor_dict["NaOH"]} | MIX: {reactor_dict["mix"]}')
                time.sleep(smallest_qnt * 4)
                send(f"[REACTOR-PROC]_{reactor_dict}", client)

            else:
                reactor_dict["EtOH"] = quarter_mix
                reactor_dict["NaOH"] = quarter_mix
                reactor_dict["oil"] = half_mix
                reactor_dict["mix"] = max_mix
                print(f'[REACTOR-MIX] OIL: {reactor_dict["oil"]} | EtOH: {reactor_dict["EtOH"]} | NaOH: {reactor_dict["NaOH"]} | MIX: {reactor_dict["mix"]}')
                time.sleep(max_mix)
                send(f"[REACTOR-PROC]_{reactor_dict}", client)

        if mix_value > 0:
            send(f"[REACTOR-OUT] {mix_value}", client)

        time.sleep(1)

main()

