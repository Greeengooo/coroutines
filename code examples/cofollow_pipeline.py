import time
from common.coroutine import coroutine


# source
def follow(file, target):
    file.seek(0, 2)
    while True:
        line = file.readline()
        if not line:
            time.sleep(0.1)
            continue
        target.send(line)


# sink
@coroutine
def printer():
    while True:
        line = (yield)
        print(line)


def main():
    with open('data/sample-2mb-text-file.txt') as file:
        follow(file, printer())


main()