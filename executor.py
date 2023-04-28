"""
Task executor class
"""

from collections import deque
from operator import attrgetter

from taskinprogressmatrix import TaskInProgressMatrix, DEFAULT_END_TIME
from utils import sort_queue


class Executor:
    """
    The Executor class manages the task execution and bandwidth allocation process.
    """
    def __init__(self, max_bandwidth, start_time=0, compress=False):
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
        self.__task_matrix = TaskInProgressMatrix(self.__max_bandwidth, compress=compress)

    @property
    def starved_tasks(self):
        return self.__task_matrix.starved_tasks

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
        @rtype: TaskInProgressMatrix
        """
        return self.__task_matrix

    def add_task(self, task):
        """
        add tasks to submission queue,
        create subqueues by time and priority
        :param task: task to add
        :return: None
        """
        # append task to queues by time
        task_start_time = task.actual_start_time
        try:
            time_deque = self.__submission_queue_dict[task_start_time]
        except KeyError:
            self.__submission_queue_dict[task_start_time] = deque()
            time_deque = self.__submission_queue_dict[task_start_time]
        time_deque.append(task)
        # after appending, sort queue by priority and add them to submission queue
        self.__sort_queue(task_start_time)

    def __sort_queue(self, queue_num):
        """
        sort queue by priority and original start time
        :param queue_num: number of queue by actual start time
        """
        original_que = self.__submission_queue_dict[queue_num]
        sorted_que = sorted(original_que, key=attrgetter('created_time')) # sort by created time first (secondary key)
        sorted_que = sorted(sorted_que, key=attrgetter('priority'), reverse=True) # then sort by priority
        # sorted_que = sorted(original_que, key= lambda task: (task.priority, task.created_time), reverse=True)
        self.__submission_queue_dict[queue_num] = sorted_que

    def __add_task_to_exec_matrix(self, task):
        """
        Add a task to the task execution matrix.
        @param task: task to add
        @type task: Task
        @return: None
        """
        if self.__task_matrix.add_task(task):  # task added successfully
            return
        else:
            # increase task time, return task to submission queue
            task.actual_start_time += 1
            self.add_task(task)

    def execute_tasks(self, start_time=0, end_time=DEFAULT_END_TIME, step=1):
        """
        Execute task between a given start and end time.
        @param start_time: start time for executing task, default is 0
        @type start_time: int
        @param end_time: end time for executing task, default is DEFAULT_END_TIME
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
                    self.__add_task_to_exec_matrix(task)
            except KeyError:
                pass
