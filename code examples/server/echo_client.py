import socket

if __name__ == '__main__':
    socket = socket.create_connection(('', 8888))
    while True:
        msg = input("Type text: ")
        if msg == "stop":
            socket.close()
            break
        socket.sendall(msg.encode("utf-8"))
