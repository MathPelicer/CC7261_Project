def send(msg, client):
    FORMAT = 'utf-8'
    HEADER = 1024

    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    client.send(send_length)
    client.send(message)

    msg_recv = client.recv(2048).decode(FORMAT)
    print(msg_recv)
    return msg_recv