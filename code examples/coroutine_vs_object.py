from timeit import timeit

from common.coroutine import coroutine


class GrepHandler(object):
    def __init__(self, pattern, target):
        self.pattern = pattern
        self.target = target

    def send(self, line):
        if self.pattern in line:
            self.target.send(line)


@coroutine
def null():
    while True: item = (yield)


@coroutine
def grep(pattern, target):
    while True:
        line = (yield)
        if pattern in line:
            target.send(line)


line = "test"
p1 = grep("test", null())
p2 = GrepHandler("test", null())
print(timeit("for _ in range(10): p1.send(line)", "from __main__ import line,p1"))
print(timeit("for _ in range(10): p2.send(line)", "from __main__ import line,p2"))


