import socket

def Server():
  with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((socket.gethostname(), 50002))
    print(s)
    s.listen(10)
    try:
      while True:
        (connectionSocket, addr) = s.accept()
        print(f"Cliente conectado: {addr}")
        
        while True:
          dados = connectionSocket.recv(1024)
          if not dados:
            break
          print(f"Mensagem recebida: {dados.decode()}")
          connectionSocket.sendall(b"OBRIGADO. Desconectando")
    except KeyboardInterrupt:
      print("\n Shutting down... \n")
    except Exception as exc:
      print("Error: \n")
      print(exc)

Server()