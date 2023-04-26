from collections import deque

class Executor:
    def __init__(self, bandwidth, start_time=0):
        self.__bandwidth = bandwidth
        self.__start_time = start_time
        self.__submission_queue_list = [] # list of submission queues by time
        self.__execution_queue_list = [] # list of execution queues by time
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

    def add_tasks(self, *args):
        """
        add tasks to submission queue, sort submission queue by time and priority
        :param args:
        :return:
        """