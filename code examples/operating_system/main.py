from operating_system.scheduler import Scheduler
from operating_system.system_call import GetTid, NewTask, WaitTask, KillTask


def foo():
    child = yield GetTid()  # creates a GetTid object
    while True:
        print(f"FOO {child}")
        yield


def bar():
    """
    GetTid() will create a SystemCall object and yield it
    :return:
    """
    mytid = yield GetTid()
    for _ in range(10):
        print(f"BAR {mytid}")
        yield


def main():
    child2 = yield NewTask(foo())
    # the child will return a tid of of the process
    yield WaitTask(child2)
    for _ in range(10):
        yield
    yield KillTask(child2)


if __name__ == '__main__':
    sched = Scheduler()
    sched.new(main())
    sched.mainloop()