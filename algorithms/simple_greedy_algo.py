from collections import deque

from . import sort_queue
class SimpleGreedyAlgorithm:
    def __init__(self, task_list):
        self.waitingTaskQueue = deque(task_list)
        self.processingQueue = deque()
        self.separateQueue = deque()

    def execute(self, total_bandwidth):
        current_time = 0
        while True:
            # sort by priority and then by start time
            self.waitingTaskQueue = sort_queue(self.waitingTaskQueue, 'priority')
            self.waitingTaskQueue = sort_queue(self.waitingTaskQueue, 'created_time')
            # start running
            new_task = self.waitingTaskQueue.popleft()
