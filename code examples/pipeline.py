from unix_tail_f import follow

"""
Pipeline approach
"follow" script yields every new line added to logfile whereas grep script returns the line that contain a specific pattern
"""


def grep(pattern, lines):
    for line in lines:
        if pattern in line:
            yield line


def grep_coroutine(pattern):
    print("Looking for pattern")
    while True:
        line = (yield)  # here we receive the value from send method
        if pattern in line:
            print(line)


def main_grep():
    with open("data/sample-2mb-text-file.txt") as logfile:
        loglines = follow(logfile)
        matched_lines = grep("test", loglines)
        for line in matched_lines:
            print(line)


def main_grep_coroutine():
    g = grep_coroutine("test")
    # we need to prime the coroutine
    g.send(None)
    g.send("It is good but bad, BUUUT amazing")
    g.send("Still amazing but test")


if __name__ == '__main__':
    # main_grep()
    main_grep_coroutine()
