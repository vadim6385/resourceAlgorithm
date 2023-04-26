from collections import deque
from operator import attrgetter


def sort_queue(Q, attrib):
    """
    sort deque by attribute
    :param Q: deque to sort
    :param attrib: deque sort by attribute
    :return: sorted deque
    """
    return deque(sorted(Q, key=attrgetter(attrib)))


class Executor:
    def __init__(self, bandwidth, start_time=0):
        self.__bandwidth = bandwidth
        self.__start_time = start_time
        self.__submission_queue_dict = {}  # list of submission queues by time
        self.__execution_queue_list = []  # list of execution queues by time
        self.__current_time = self.__start_time

    @property
    def bandwidth(self):
        return self.__bandwidth

    @property
    def start_time(self):
        return self.__start_time

    @property
    def current_time(self):
        return self.__current_time

    @current_time.setter
    def current_time(self, val):
        self.__current_time = val

    def advance_time(self):
        self.__current_time += 1

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

    def execute_tasks(self, start_time=0, end_time=0xFFFF, step=1):
        for i in range(start_time, end_time, step):
            try:
                one_time_task_queue = self.__submission_queue_dict[i]
                while one_time_task_queue:
                    task = one_time_task_queue.pop()


