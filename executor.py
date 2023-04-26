from collections import deque

from taskmatrix import TaskMatrix, DEFAULT_END_TIME
from utils import sort_queue


class Executor:
    def __init__(self, max_bandwidth, start_time=0):
        self.__max_bandwidth = max_bandwidth
        self.__start_time = start_time
        self.__submission_queue_dict = {}  # list of submission queues by time
        self.__task_matrix = TaskMatrix(self.__max_bandwidth)

    @property
    def max_bandwidth(self):
        return self.__max_bandwidth

    @property
    def start_time(self):
        return self.__start_time

    @property
    def task_matrix(self):
        return self.__task_matrix

    def add_tasks(self, *tasks):
        """
        add tasks to submission queue,
        create subqueues by time and priority
        :param tasks: tasks to add
        :return: None
        """
        # append tasks to queues by time
        for one_task in tasks:
            try:
                time_deque = self.__submission_queue_dict[one_task.start_time]
            except KeyError:
                self.__submission_queue_dict[one_task.start_time] = deque()
                time_deque = self.__submission_queue_dict[one_task.start_time]
            time_deque.append(one_task)
        # after appending, sort queues by priority and add them to submission queue
        for one_time in self.__submission_queue_dict.keys():
            sorted_q = sort_queue(self.__submission_queue_dict[one_time], "priority")
            self.__submission_queue_dict[one_time] = sorted_q

    def add_task_to_exec_matrix(self, task):
        if self.__task_matrix.add_task(task):  # task added successfully
            return
        else:
            # increase task time and priority, return task to submission queue
            task.priority += 1
            task.start_time += 1
            self.add_tasks(task)

    def execute_tasks(self, start_time=0, end_time=DEFAULT_END_TIME, step=1):
        for i in range(start_time, end_time, step):
            try:
                one_time_task_queue = self.__submission_queue_dict[i]
                while one_time_task_queue:
                    task = one_time_task_queue.pop()
                    self.add_task_to_exec_matrix(task)
            except KeyError:
                pass
        # print(self.__task_matrix)
