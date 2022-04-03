import time


def follow(file):
    file.seek(0, 2)
    while True:
        line = file.readline()
        if not line:
            time.sleep(0.1)
            continue
        yield line


def main():
    with open('data/sample-2mb-text-file.txt') as file:
        for line in follow(file):
            print(line)


if __name__ == '__main__':
    main()
