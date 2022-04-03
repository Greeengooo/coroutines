# it could hard to remember to do priming for coroutines,
# instead you can use decorator

def coroutine(func):
    def start(*args, **kwargs):
        cr = func(*args, **kwargs)
        cr.send(None)
        return cr
    return start


@coroutine
def grep(pattern):
    while True:
        line = (yield)
        if pattern in line:
            print(line)


if __name__ == '__main__':
    g = grep(pattern="test")
    g.send("Hello test")
    g.send("test")

    # close a coroutine
    g.close()
