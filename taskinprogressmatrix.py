"""
This module defines a TaskInProgressMatrix class that helps manage task and their bandwidth allocation.
"""
from operator import attrgetter

import numpy as np

# Constants for default end time values
from utils import TaskStatus, DEBUG_HALT

DEFAULT_END_TIME = 0xFF
DEFAULT_MATRIX_END_TIME = 0x200


class TaskInProgressMatrix:
    """
    A class representing a matrix of task and their bandwidth allocation.
    """

    def __init__(self, max_bandwidth, end_time=DEFAULT_END_TIME, compress=False):
        """
        Initialize the TaskInProgressMatrix.

        @param max_bandwidth: maximum bandwidth for the task matrix
        @type max_bandwidth: int
        @param end_time: end time for the task matrix, default is DEFAULT_MATRIX_END_TIME
        @type end_time: int
        """
        self.__max_bandwidth = max_bandwidth
        self.__end_time = end_time+1
        self.__matrix = np.zeros((self.__max_bandwidth, self.__end_time), dtype=int)
        self.__starved_tasks_list = []
        self.__completed_tasks_list = []
        self.__task_execution_dict = {}
        self.__compress = compress

    @property
    def data_matrix(self):
        """
        Get the underlying task matrix data.
        @return: the task matrix data
        @rtype: numpy.ndarray
        """
        self.__draw_matrix()
        return self.__matrix

    @property
    def data_dict(self):
        return self.__task_execution_dict

    @property
    def starved_tasks(self):
        return self.__starved_tasks_list

    @property
    def completed_tasks(self):
        return self.__completed_tasks_list

    @property
    def compress(self):
        return self.__compress

    def __update_task(self, task):
        time_start = task.actual_start_time
        time_end = task.actual_end_time
        task_id = task.id
        for i in range(time_start, time_end+1):
            for j in range(len(self.__task_execution_dict[i])):
                if self.__task_execution_dict[i][j].id == task_id:
                    self.__task_execution_dict[i][j] = task
                    break

    def __draw_matrix(self):
        for i in sorted(self.__task_execution_dict.keys()):  # columns, time stamps
            task_list = self.__task_execution_dict[i]
            bandwidth_count = 0
            for j in range(len(task_list)):  # task list in bandwidth allocated for task
                task = task_list[j]
                task_id = task.id
                task_bandwidth = bandwidth_count + task.bandwidth
                if task_bandwidth > self.__max_bandwidth:
                    DEBUG_HALT()
                while bandwidth_count < task_bandwidth:
                    self.__matrix[bandwidth_count][i] = task_id
                    bandwidth_count += 1

    def __get_free_bandwidth(self, time_slot, custom_list=None):
        if custom_list is not None:
            task_list = custom_list
        else:
            try:
                task_list = self.__task_execution_dict[time_slot]
            except KeyError:  # No tasks allocated, so all is free
                return self.__max_bandwidth
        sum_bandwidth = self.__max_bandwidth
        for one_task in task_list:
            sum_bandwidth -= one_task.bandwidth
        return sum_bandwidth

    def __get_free_bandwidth_indices_list(self, time_stamp):
        """
        Get a list of indices for free bandwidth at the given time stamp.

        @param time_stamp: time stamp to check for free bandwidth
        @type time_stamp: int
        @return: count of free bandwidth and list of indices
        @rtype: tuple(int, list[int])
        """
        cnt = 0
        rows_list = []
        for i in range(self.__max_bandwidth):
            if self.__matrix[i][time_stamp] == 0:
                cnt += 1
                rows_list.append(i)
        return cnt, rows_list

    def __add_task_to_in_progress_dict(self, task):
        task_start_time = task.actual_start_time
        task_end_time = task.actual_end_time
        for one_time_slot in range(task_start_time, task_end_time + 1):
            try:
                task_list = self.__task_execution_dict[one_time_slot]
            except KeyError:
                self.__task_execution_dict[one_time_slot] = []
                task_list = self.__task_execution_dict[one_time_slot]
            task_list.append(task)

    def __sorted_task_list(self, time_slot, reversePriority=False):
        try:
            task_list = self.__task_execution_dict[time_slot]
        except KeyError:
            return
        if len(task_list) <= 1:  # no need to waste time on sorting
            return
        sorted_list = sorted(task_list, key=attrgetter('created_time'))  # sort by created time first (secondary key)
        sorted_list = sorted(sorted_list, key=attrgetter('priority'), reverse=reversePriority)  # then sort by priority
        return sorted_list

    def __add_task_compress(self, task):
        task_start_time = task.actual_start_time
        task_bandwidth = task.bandwidth
        compressed_task_list = []
        # get task list sorted by priority, lowest first
        lp_sorted_list = self.__sorted_task_list(task_start_time, reversePriority=False)
        for i in range(len(lp_sorted_list)):
            lowest_task = lp_sorted_list[i]
            lowest_task.compress()
            free_bandwidth = self.__get_free_bandwidth(task_start_time, lp_sorted_list)
            compressed_task_list.append(lowest_task)
            if free_bandwidth >= task_bandwidth:
                task.status = TaskStatus.IN_PROGRESS
                self.__add_task_to_in_progress_dict(task)
                for task in compressed_task_list:
                    self.__update_task(task)
                return True
        # could not find bandwidth for the task
        for one_task in compressed_task_list:
            one_task.decompress()
        return False

    def add_task(self, task):
        """
        Add a task to the TaskInProgressMatrix and allocate bandwidth.
        @param task: task to be added
        @type task: Task
        @return: True if the task was added, False if not enough bandwidth
        @rtype: bool
        """
        task_bandwidth = task.bandwidth
        start_time = task.actual_start_time
        free_bandwidth = self.__get_free_bandwidth(start_time)
        task_end_time = start_time + task.duration
        # if task end time is more than total allocated time, nothing to do here,
        # task is dropped and moved to starved task list
        if task_end_time > self.__end_time:
            task.status = TaskStatus.DROPPED
            self.__starved_tasks_list.append(task)
            return True
        if task_bandwidth > free_bandwidth:
            if self.compress:
                return self.__add_task_compress(task)
            else:
                return False
        # set task status as in progress
        task.status = TaskStatus.IN_PROGRESS
        # add the task to the task allocation dictionary
        self.__add_task_to_in_progress_dict(task)
        return True

    def __repr__(self):
        """
        Generate a string representation of the TaskInProgressMatrix.

        @return: string representation of the TaskInProgressMatrix
        @rtype: str
        """
        ret = "\t"
        for col in range(self.__end_time):
            ret += "{}\t".format(str(col))
        ret += "\n"
        for row in range(self.__max_bandwidth):
            ret += "{}:\t".format(str(row))
            for col in range(self.__end_time):
                ret += "{}\t".format(str(self.__matrix[row][col]))
            ret += "\n"
        return ret
