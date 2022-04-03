import queue


def func():
    a = yield 2
    for _ in range(10):
        print("Inside:", a)
        yield


def queue_test():
    q = queue.Queue()
    q.put(1)
    q.put(2)
    q.get()
    print()


if __name__ == '__main__':
    f = func()
    print("Outside:", f.send(None))
    print("Outside:", f.send(1))

    queue_test()
