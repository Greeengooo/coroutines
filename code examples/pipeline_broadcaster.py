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


# broadcaster
@coroutine
def broadcast(targets):
    while True:
        item = (yield)
        for target in targets:
            target.send(item)


# filter
@coroutine
def grep(pattern, target):
    while True:
        line = (yield)
        if pattern in line:
            target.send(line)


# sink
@coroutine
def printer():
    while True:
        line = (yield)
        print(line)


def main():
    with open('data/sample-2mb-text-file.txt') as file:
        follow(file,
               broadcast([grep('python', printer()),
                          grep('test', printer()),
                          grep('sample', printer())]))


def main_single_sink():
    with open('data/sample-2mb-text-file.txt') as file:
        sink = printer()
        follow(file,
               broadcast([grep('python', sink),
                          grep('test', sink),
                          grep('sample', sink)]))


main_single_sink()
