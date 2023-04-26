"""
This module defines a TaskMatrix class that helps manage tasks and their bandwidth allocation.
"""

import numpy as np

# Constants for default end time values
DEFAULT_END_TIME = 0xFF
DEFAULT_MATRIX_END_TIME = 1000


class TaskMatrix:
    """
    A class representing a matrix of tasks and their bandwidth allocation.
    """

    def __init__(self, max_bandwidth, end_time=DEFAULT_MATRIX_END_TIME):
        """
        Initialize the TaskMatrix.

        @param max_bandwidth: maximum bandwidth for the task matrix
        @type max_bandwidth: int
        @param end_time: end time for the task matrix, default is DEFAULT_MATRIX_END_TIME
        @type end_time: int
        """
        self.__max_bandwidth = max_bandwidth
        self.__end_time = end_time
        self.__matrix = np.zeros((self.__max_bandwidth, self.__end_time), dtype=int)

    @property
    def data(self):
        """
        Get the underlying task matrix data.

        @return: the task matrix data
        @rtype: numpy.ndarray
        """
        return self.__matrix

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

    def add_task(self, task):
        """
        Add a task to the TaskMatrix and allocate bandwidth.

        @param task: task to be added
        @type task: Task
        @return: True if the task was added, False if not enough bandwidth
        @rtype: bool
        """
        bandwidth = task.bandwidth
        start_time = task.start_time
        free_bandwidth, free_rows_list = self.__get_free_bandwidth_indices_list(start_time)
        if bandwidth > free_bandwidth:
            return False
        task_id = task.id
        end_time = start_time + task.duration
        # "paint" the appropriate places in task matrix with task id number
        for i in free_rows_list:  # matrix rows
            for j in range(start_time, end_time):  # matrix columns
                self.__matrix[i][j] = task_id
            bandwidth -= 1
            if bandwidth <= 0:
                break
        return True

    def __repr__(self):
        """
        Generate a string representation of the TaskMatrix.

        @return: string representation of the TaskMatrix
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
