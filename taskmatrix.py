import numpy as np

DEFAULT_END_TIME = 0xFF
DEFAULT_MATRIX_END_TIME = 1000

class TaskMatrix:
    def __init__(self, max_bandwidth, end_time=DEFAULT_MATRIX_END_TIME):
        self.__max_bandwidth = max_bandwidth
        self.__end_time = end_time
        self.__matrix = np.zeros((self.__max_bandwidth, self.__end_time), dtype=int)

    @property
    def data(self):
        return self.__matrix

    def __zeros(self, rows, cols):
        return [[0 for col in range(cols)] for row in range(rows)]

    def __get_free_bandwidth_indices_list(self, time_stamp):
        cnt = 0
        rows_list = []
        for i in range(self.__max_bandwidth):
            if self.__matrix[i][time_stamp] == 0:
                cnt += 1
                rows_list.append(i)
        return cnt, rows_list

    def add_task(self, task):
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
        # print the matrix in a nice way
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
