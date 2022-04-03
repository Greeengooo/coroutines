from queue import Queue
from threading import Thread
from common.coroutine import coroutine

messages = Queue()


@coroutine
def threaded(target):
    """
    1. initialize message queue
    2. run the Thread with the function that
       - pulls the elements from the queue and sens it to the target
         coroutine
       - on generator exit it closes the target coroutine
    3. populate the queue untill the GeneratorExit is sent
    """
    Thread(target=run_target, args=(target,)).start()
    try:
        while True:
            item = (yield)
            messages.put(item)
    except GeneratorExit:
        messages.put(GeneratorExit)


def run_target(target):
    while True:
        item = messages.get()
        if item is GeneratorExit:
            target.close()
            return
        else:
            target.send(item)
