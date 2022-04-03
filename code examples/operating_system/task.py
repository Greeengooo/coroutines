# Task is a wrapper around coroutine
class Task:
    taskid = 0

    def __init__(self, target):
        """
        Here we create a Task object and initialize
        * tid,
        * target coroutine,
        * sendval value that we send to the coroutine (foo)
        :param target: target coroutine
        """
        Task.taskid += 1
        self.tid = Task.taskid  # task id
        self.target = target  # target coroutine
        self.sendval = None  # value to send

    # run a task until it hits the next yield statement
    def run(self):
        """
        sends a value back to the coroutine and
        returns a result from yield inside coroutine
        :return:
        """
        return self.target.send(self.sendval)
