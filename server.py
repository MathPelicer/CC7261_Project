from socket import *
import os
import sys
import codecs
import glob

def Server():
  HOST = ''
  PORT = 9000

  server_socket = socket(AF_INET, SOCK_STREAM)
  orig = (HOST, PORT)
  server_socket.bind(orig)
  server_socket.listen(1)

  print("creating server...")

  try:
    print("entering while loops")
    while(1):
      (connectionSocket, addr) = server_socket.accept()

      while True:
        print("Cliente {} conectado ao servidor".format(addr))

        request = connectionSocket.recv(1024).decode()
        print(request)

        connectionSocket.sendall(request.encode())

  except KeyboardInterrupt:
    print("\n Shutting down... \n")
  except Exception as exc:
    print("Error: \n")
    print(exc)

Server()