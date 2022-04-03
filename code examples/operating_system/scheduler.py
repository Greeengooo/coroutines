import select
from queue import Queue

from operating_system.system_call import SystemCall
from operating_system.task import Task


class Scheduler:
    def __init__(self):
        self.ready = Queue()  # a queue of tasks that are ready to run
        self.taskmap = {}
        self.exit_waiting = {}
        self.read_waiting = {}
        self.write_waiting = {}

    # introduces a new task to the scheduler
    def new(self, target):
        """
        Here we create a new task and pass it
        to the taskmap and
        schedule by placing it inside ready queue

        :param target: coroutine that is wrapped by
        Task object
        :return: tid of the created task
        """
        newtask = Task(target)
        self.taskmap[newtask.tid] = newtask
        self.schedule(newtask)
        return newtask.tid

    # delete the task from map if we face stop iteration exception
    def exit(self, task):
        print(f"Task {task.tid} terminated")
        del self.taskmap[task.tid]
        # we need to notify other tasks waiting for exit
        for task in self.exit_waiting.pop(task.tid, []):
            self.schedule(task)

    def wait_for_exit(self, task, waitid):
        """
        This function checks if the task is in taskmap
        if so we append the
        :param task: the parent task
        :param waitid: the id of the task taht we shoul wait
        :return: boolean
        """
        if waitid in self.taskmap:
            self.exit_waiting.setdefault(waitid, []).append(task)
            return True
        else:
            return False

    def wait_for_read(self, task, fd):
        """
        file_descriptor is waiting to read and
        task is interested in the result
        """
        self.read_waiting[fd] = task

    def wait_for_write(self, task, fd):
        """
        file_descriptor is waiting to write and
        task is interested in the result
        """
        self.write_waiting[fd] = task

    def iopoll(self, timeout):
        # if anybody is waiting for I/O operations
        if self.write_waiting or self.read_waiting:
            readable, writable, exceptional = \
                select.select(self.read_waiting, self.write_waiting, [], timeout)  # timeout in seconds
            # unblock any associated task
            for fd in readable:
                self.schedule(self.read_waiting.pop(fd))
            for fd in writable:
                self.schedule(self.write_waiting.pop(fd))

    # puts a task on the ready queue
    def schedule(self, task):
        self.ready.put(task)

    def iotask(self):
        while True:
            if self.ready.empty():
                self.iopoll(None)
            else:
                self.iopoll(1)
            yield

    def mainloop(self):
        while self.taskmap:
            # check whether we face IO
            """
            When the server is waiting for the connection 
            it actually runs the iotask until the connection comes
            """
            self.new(self.iotask())
            # get the next task from the queue
            task = self.ready.get()
            try:
                result = task.run()
                if isinstance(result, SystemCall):
                    # set the parent task
                    result.task = task
                    # set the scheduler object
                    result.sched = self
                    # run the handler for current SystemCall task
                    result.handle()
                    continue
            except StopIteration:
                self.exit(task)
                continue
            self.schedule(task)
