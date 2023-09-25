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
    processingQueue = []
    completedQueue = []
    preempted_task_stack = deque()
    waiting_temp_stack = deque()
    current_time = 0
    while waitingTaskQueue or processingQueue:  # run while there are tasks in waiting or operation
        # Sort by priority and then by start time
        waitingTaskQueue = sort_list(waitingTaskQueue, 'priority', is_reverse=True)
        waitingTaskQueue = sort_list(waitingTaskQueue, 'actual_start_time')
        # Go over processing queue and remove tasks that are done
        for one_task in processingQueue:
            if one_task.actual_end_time < current_time: # or one_task.remaining_duration == 0:
                one_task.status = TaskStatus.FINISHED
                completedQueue.append(one_task)
                total_bandwidth += one_task.bandwidth  # return task bandwidth to the bandwidth pool
        for one_task in completedQueue:
            if one_task in processingQueue:
                processingQueue.remove(one_task)
        # Start running tasks
        while waitingTaskQueue:
            one_task = waitingTaskQueue.pop()
            if one_task.actual_start_time == current_time or one_task.preempted_time == current_time:
                if one_task.bandwidth <= total_bandwidth:
                    total_bandwidth -= one_task.bandwidth
                    if total_bandwidth < 0:
                        DEBUG_HALT()  # shouldn't get here
                    one_task.status = TaskStatus.IN_PROGRESS
                    processingQueue.append(one_task)  # add task to processing queue
                else:
                    # preempt tasks already in processing
                    processingQueue = sort_list(processingQueue, 'priority', is_reverse=False)
                    processingQueue = sort_list(processingQueue, 'remaining_duration', is_reverse=True)
                    if not processingQueue:
                        DEBUG_HALT()  # processing queue will always be populated
                    task_counter = len(processingQueue)
                    while one_task.bandwidth > total_bandwidth:  # do until enough bandwidth to add the new task
                        if task_counter == 0:
                            break  # exit loop if gone over all tasks
                        removed_task = processingQueue.pop(0)
                        if removed_task.priority <= one_task.priority:  # if priority is less or more
                            total_bandwidth += removed_task.bandwidth
                            removed_task.preempted_time = current_time + 1
                            removed_task.status = TaskStatus.SUSPENDED
                            preempted_task_stack.append(removed_task)  # append task to stack
                            if one_task.bandwidth <= total_bandwidth:  # last check if there is enough bandwidth
                                total_bandwidth -= one_task.bandwidth
                                if total_bandwidth < 0:
                                    DEBUG_HALT()  # shouldn't get here
                                one_task.status = TaskStatus.IN_PROGRESS
                                processingQueue.append(one_task)  # add task to processing queue
                                break
                        else:
                            processingQueue.append(removed_task)
                        task_counter -= 1
                    if not one_task.status == TaskStatus.IN_PROGRESS:
                        one_task.actual_start_time += 1
                        waiting_temp_stack.append(one_task)
            else:
                waiting_temp_stack.append(one_task)
        # re-add the tasks from waiting temp stack to the waiting queue
        while waiting_temp_stack:
            task_to_waiting = waiting_temp_stack.pop()
            waitingTaskQueue.append(task_to_waiting)
        # now clean up the removed task stack, and add them back to waiting queue
        while preempted_task_stack:
            task_to_waiting = preempted_task_stack.pop()
            waitingTaskQueue.append(task_to_waiting)
        current_time += 1  # advance time
        for one_task in processingQueue:
            if one_task in waitingTaskQueue:  # remove IN_PROGRESS tasks from waiting queue
                waitingTaskQueue.remove(one_task)
            # decrease remaining duration for tasks in progress
            # one_task.remaining_duration -= 1
    return list(completedQueue)
