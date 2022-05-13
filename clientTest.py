import socket
import _thread
import re

host = '0.0.0.0'
port = 8080

class Server:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.sock = ""

    def create_and_bind_socket(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((host, port))
        self.sock.listen(100)

    def new_connection(self):
        conn, addr = self.sock.accept()
        print(f'{addr[0]} connected')
        return conn, addr
    
    def run(self, conn, addr):
        conn.send("==========================================\n".encode())
        conn.send("welcome to chat room!\n\n".encode())
        conn.send("/register - register a new user\n/login - login into an existing account\n/join_lobby - join an existing lobby\n/create_lobby - create a new lobby\n/list_lobby - list all the existing lobbies\n/logout - logout from your current account\n/help - list available commands\n\n".encode())

        user = ''

        while True:
            msg = conn.recv(2048).decode()
            msg = re.sub(r'\r\n', '', msg)

server = Server(host, port)
server.create_and_bind_socket()

while True:
    conn, addr = server.new_connection()
    _thread.start_new_thread(server.run, (conn, addr))