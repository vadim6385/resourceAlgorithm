from collections import deque

from task import TaskStatus
from utils import DEBUG_HALT
from . import sort_queue


class SimpleGreedyAlgorithm:
    def __init__(self, task_list: list):
        self.waitingTaskQueue = deque(task_list)
        self.processingQueue = deque()
        self.completedQueue = deque()

    def execute(self, total_bandwidth):
        """
        execute tasks
        :param total_bandwidth: bandwidth to work with
        :return: completed queue
        """
        current_time = 0
        while self.waitingTaskQueue or self.processingQueue:  # run while there are tasks in operation
            # sort by priority and then by start time
            self.waitingTaskQueue = sort_queue(self.waitingTaskQueue, 'priority')
            self.waitingTaskQueue = sort_queue(self.waitingTaskQueue, 'created_time')
            # go over processing queue and remove tasks that are done
            for one_task in self.processingQueue:
                if one_task.actual_end_time < current_time:  # mark task as completed
                    one_task.status = TaskStatus.FINISHED
                    self.completedQueue.append(one_task)
                    total_bandwidth += one_task.bandwidth  # return task bandwidth to the bandwidth pool
            for one_task in self.completedQueue:
                if one_task in self.processingQueue:
                    self.processingQueue.remove(one_task)
            # start running
            for one_task in self.waitingTaskQueue:
                if one_task.actual_start_time == current_time:
                    if one_task.bandwidth <= total_bandwidth:
                        one_task.status = TaskStatus.IN_PROGRESS  # mark task as in progress
                        total_bandwidth -= one_task.bandwidth  # occupy the bandwidth
                        if total_bandwidth < 0:
                            DEBUG_HALT()  # shouldn't get here
                        self.processingQueue.append(one_task)  # add task to processing queue
                    else:  # if no available bandwidth, we add task time
                        one_task.actual_start_time += 1
            for one_task in self.processingQueue:  # remove IN_PROGRESS tasks from waiting queue
                if one_task in self.waitingTaskQueue:
                    self.waitingTaskQueue.remove(one_task)
            current_time += 1  # advance time
        return self.completedQueue
