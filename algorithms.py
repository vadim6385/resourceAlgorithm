import heapq
from collections import deque

from task import TaskStatus
from utils import DEBUG_HALT


def sort_list(orig_list, prop, is_reverse=False):
    """
    sort list of objects by attribute
    :param is_reverse: reverse sort
    :param orig_list: list to sort
    :param prop: property to sort by
    :return: sorted list
    """
    return sorted(orig_list, key=lambda x: getattr(x, prop), reverse=is_reverse)


def simple_greedy_algorithm(task_list, total_bandwidth):
    """
    Execute tasks using a simple greedy algorithm.
    :param task_list: List of tasks to execute
    :param total_bandwidth: Total available bandwidth
    :return: List of completed tasks
    """
    waitingTaskQueue = task_list
    processingQueue = []
    completedQueue = []
    current_time = 0
    while waitingTaskQueue or processingQueue:  # run while there are tasks in waiting or operation
        # Sort by priority and then by start time
        waitingTaskQueue = sort_list(waitingTaskQueue, 'priority', is_reverse=True)
        waitingTaskQueue = sort_list(waitingTaskQueue, 'actual_start_time')
        # Go over processing queue and remove tasks that are done
        for one_task in processingQueue:
            if one_task.actual_end_time < current_time:
                completedQueue.append(one_task)
                total_bandwidth += one_task.bandwidth  # return task bandwidth to the bandwidth pool
        for one_task in completedQueue:
            if one_task in processingQueue:
                processingQueue.remove(one_task)
        # Start running tasks
        for one_task in waitingTaskQueue:
            if one_task.actual_start_time == current_time:
                if one_task.bandwidth <= total_bandwidth:
                    total_bandwidth -= one_task.bandwidth
                    if total_bandwidth < 0:
                        DEBUG_HALT()  # shouldn't get here
                    processingQueue.append(one_task)  # add task to processing queue
                else:
                    one_task.actual_start_time += 1
        for one_task in processingQueue:
            if one_task in waitingTaskQueue:  # remove IN_PROGRESS tasks from waiting queue
                waitingTaskQueue.remove(one_task)
        current_time += 1  # advance time
    return list(completedQueue)


def greedy_compression_algorithm(task_list, total_bandwidth):
    """
    Execute tasks using a simple greedy algorithm.
    :param task_list: List of tasks to execute
    :param total_bandwidth: Total available bandwidth
    :return: List of completed tasks
    """
    waitingTaskQueue = task_list
    processingQueue = []
    completedQueue = []
    current_time = 0
    compression_success = False
    while waitingTaskQueue or processingQueue:  # run while there are tasks in waiting or operation
        # Sort by priority and then by start time
        waitingTaskQueue = sort_list(waitingTaskQueue, 'priority', is_reverse=True)
        waitingTaskQueue = sort_list(waitingTaskQueue, 'actual_start_time')
        # Go over processing queue and remove tasks that are done
        for one_task in processingQueue:
            if one_task.actual_end_time < current_time:
                completedQueue.append(one_task)
                total_bandwidth += one_task.bandwidth  # return task bandwidth to the bandwidth pool
        for one_task in completedQueue:
            if one_task in processingQueue:
                processingQueue.remove(one_task)
        # Start running tasks
        for one_task in waitingTaskQueue:
            if one_task.actual_start_time == current_time:
                if one_task.bandwidth <= total_bandwidth:
                    total_bandwidth -= one_task.bandwidth
                    if total_bandwidth < 0:
                        DEBUG_HALT()  # shouldn't get here
                    processingQueue.append(one_task)  # add task to processing queue
                else:  # try to do compression
                    compression_success = False
                    compressed_tasks = []
                    temp_bandwidth = total_bandwidth
                    for running_task in processingQueue:
                        if running_task.is_compressed:
                            continue
                        running_task.compress()
                        compressed_tasks.append(running_task)
                        temp_bandwidth += running_task.bandwidth_diff
                        if one_task.bandwidth <= temp_bandwidth:
                            total_bandwidth = temp_bandwidth
                            total_bandwidth -= one_task.bandwidth
                            processingQueue.append(one_task)
                            compression_success = True
                            break
                    if not compression_success:  # if compression did not succeed, decompress compressed tasks
                        for one_comp_task in compressed_tasks:
                            one_comp_task.decompress()
                        one_task.actual_start_time += 1  # advance start time for original task
        for one_task in processingQueue:
            if one_task in waitingTaskQueue:  # remove IN_PROGRESS tasks from waiting queue
                waitingTaskQueue.remove(one_task)
        current_time += 1  # advance time
    return list(completedQueue)


def preemptive_scheduling_algorithm(task_list, total_bandwidth):
    """
    Execute tasks using a preemptive scheduling algorithm.
    :param task_list: List of tasks to execute
    :param total_bandwidth: Total available bandwidth
    :return: List of completed tasks
    """
    waitingTaskQueue = deque(task_list)
    waitingTaskQueue = sort_list(waitingTaskQueue, 'priority', is_reverse=True)
    waitingTaskQueue = sort_list(waitingTaskQueue, 'actual_start_time')
    processingQueue = []
    separateQueue = deque()
    stack = deque()
    current_time = 0

    while waitingTaskQueue or processingQueue:
        # Go over processing queue and remove tasks that are done
        tasks_to_remove = []
        for one_task in processingQueue:
            if one_task.actual_end_time < current_time:
                one_task.status = TaskStatus.FINISHED
                total_bandwidth += one_task.bandwidth
                tasks_to_remove.append(one_task)
        for task in tasks_to_remove:
            processingQueue.remove(task)

        while waitingTaskQueue:
            one_task = waitingTaskQueue.pop()
            if one_task.bandwidth <= total_bandwidth:
                total_bandwidth -= one_task.bandwidth
                one_task.status = TaskStatus.IN_PROGRESS
                processingQueue.append(one_task)
            else:
                # Sort processingQueue for removal
                processingQueue = sort_list(processingQueue, 'priority', is_reverse=False)
                processingQueue = sort_list(processingQueue, 'remaining_duration', is_reverse=True)
                for task in processingQueue:
                    if one_task.bandwidth <= total_bandwidth:
                        break
                    if task.priority <= one_task.priority:
                        processingQueue.remove(task)
                        stack.append(task)
                        total_bandwidth += task.bandwidth
                if one_task.bandwidth <= total_bandwidth:
                    total_bandwidth -= one_task.bandwidth
                    one_task.status = TaskStatus.IN_PROGRESS
                    processingQueue.append(one_task)
                else:
                    separateQueue.appendleft(one_task)

        # Empty the separate queue back into the main queue
        waitingTaskQueue.extend(separateQueue)
        separateQueue.clear()

        # Handle the stack
        while stack:
            task = stack.pop()
            if task.bandwidth <= total_bandwidth:
                total_bandwidth -= task.bandwidth
                task.status = TaskStatus.IN_PROGRESS
                processingQueue.append(task)
            else:
                separateQueue.appendleft(task)

        current_time += 1
    return [task for task in task_list if task.status == TaskStatus.FINISHED]