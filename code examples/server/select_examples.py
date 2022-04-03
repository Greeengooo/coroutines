from socket import socket, AF_INET, SOCK_STREAM


def server():
    server = socket(AF_INET, SOCK_STREAM)
    server.bind(("localhost", 10000))
    server.listen(5)
