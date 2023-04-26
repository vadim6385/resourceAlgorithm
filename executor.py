"""
Task executor class
"""

from collections import deque

from taskmatrix import TaskMatrix, DEFAULT_END_TIME
from utils import sort_queue


class Executor:
    """
    The Executor class manages the task execution and bandwidth allocation process.
    """
    def __init__(self, max_bandwidth, start_time=0):
        """
        Initialize the Executor.
        @param max_bandwidth: maximum bandwidth for the executor
        @type max_bandwidth: int
        @param start_time: start time for the executor, default is 0
        @type start_time: int
        """
        self.__max_bandwidth = max_bandwidth
        self.__start_time = start_time
        self.__submission_queue_dict = {}  # list of submission queues by time
        self.__task_matrix = TaskMatrix(self.__max_bandwidth)

    @property
    def max_bandwidth(self):
        """
        Get the maximum bandwidth for the executor.
        @return: the maximum bandwidth
        @rtype: int
        """
        return self.__max_bandwidth

    @property
    def start_time(self):
        """
        Get the start time for the executor.
        @return: the start time
        @rtype: int
        """
        return self.__start_time

    @property
    def task_matrix(self):
        """
        Get the task matrix for the executor.
        @return: the task matrix
        @rtype: TaskMatrix
        """
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
                time_deque = self.__submission_queue_dict[one_task.created_time]
            except KeyError:
                self.__submission_queue_dict[one_task.created_time] = deque()
                time_deque = self.__submission_queue_dict[one_task.created_time]
            time_deque.append(one_task)
        # after appending, sort queues by priority and add them to submission queue
        for one_time in self.__submission_queue_dict.keys():
            sorted_q = sort_queue(self.__submission_queue_dict[one_time], "priority", True)
            self.__submission_queue_dict[one_time] = sorted_q

    def add_task_to_exec_matrix(self, task):
        """
        Add a task to the task execution matrix.
        @param task: task to add
        @type task: Task
        @return: None
        """
        if self.__task_matrix.add_task(task):  # task added successfully
            return
        else:
            # increase task time and priority, return task to submission queue
            # task.priority += 1
            task.actual_start_time += 1
            self.add_tasks(task)

    def execute_tasks(self, start_time=0, end_time=DEFAULT_END_TIME, step=1):
        """
        Execute tasks between a given start and end time.
        @param start_time: start time for executing tasks, default is 0
        @type start_time: int
        @param end_time: end time for executing tasks, default is DEFAULT_END_TIME
        @type end_time: int
        @param step: step size for iterating through time, default is 1
        @type step: int
        @return: None
        """
        for i in range(start_time, end_time, step):
            try:
                one_time_task_queue = self.__submission_queue_dict[i]
                while one_time_task_queue:
                    task = one_time_task_queue.pop()
                    self.add_task_to_exec_matrix(task)
            except KeyError:
                pass
        # print(self.__task_matrix)
