# Base class for SystemCall
class SystemCall:
    def handle(self):
        pass


class GetTid(SystemCall):
    def handle(self):
        # we can treat this line as a return statement
        # we recieve the value of sendval in bar function
        self.task.sendval = self.task.tid
        # schedule the task
        self.sched.schedule(self.task)


class NewTask(SystemCall):
    """
    the target is the function that bounds to the task
    """
    def __init__(self, target):
        self.target = target

    def handle(self):
        """
        here we initialize a task along with
        value that we send
        and schedule this task by placing the task object to the queue
        """
        tid = self.sched.new(self.target)
        self.task.sendval = tid
        self.sched.schedule(self.task)


class KillTask(SystemCall):
    def __init__(self, tid):
        self.tid = tid

    def handle(self):
        task = self.sched.taskmap.get(self.tid, None)
        if task:
            task.target.close()
            self.task.sendval = True
        else:
            self.task.sendval = False
        self.sched.schedule(self.task)


class WaitTask(SystemCall):
    def __init__(self, tid):
        self.tid = tid

    def handle(self):
        result = self.sched.wait_for_exit(self.task, self.tid)
        self.task.sendval = result

        # if we wait for non-existent task we should return the result immediately
        if not result:
            self.sched.schedule(self.task)


class ReadWait(SystemCall):
    def __init__(self, f):
        self.f = f

    def handle(self):
        fd = self.f.fileno()
        self.sched.wait_for_read(self.task, fd)


class WriteWait(SystemCall):
    def __init__(self, f):
        self.f = f

    def handle(self):
        fd = self.f.fileno()
        self.sched.wait_for_write(self.task, fd)

