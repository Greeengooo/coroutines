import socket
from socket import socket, SOCK_STREAM, AF_INET
import sys
sys.path.append(".")
sys.path.append("../")
from operating_system.scheduler import Scheduler
from operating_system.system_call import NewTask, ReadWait, WriteWait


def handle_client(client, addr):
    print("Connection from", addr)
    while True:
        yield ReadWait(client)
        data = client.recv(65536)
        if not data:
            break
        yield WriteWait(client)
        client.send(data)
    client.close()
    print("Client closed")
    # with yield we make a function a generator/coroutine
    yield


def server(port):
    print("Server starting")
    sock = socket(AF_INET, SOCK_STREAM)
    sock.bind(('', port))
    sock.listen(2)  # listens to 5 connections
    while True:
        # yield ReadWait(sock)
        client, addr = sock.accept()  # accept blocks the execution and waits for an incoming connection
        yield NewTask(handle_client(client, addr))


if __name__ == '__main__':
    sched = Scheduler()
    sched.new(server(8888))
    sched.mainloop()
