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


def compare_lists(list1, list2):
    """
    Compare two lists and return a set of differences.
    :param list1: First list to be compared.
    :param list2: Second list to be compared.
    :return: A set containing differences between the two lists.
    """
    set1 = set(list1)
    set2 = set(list2)
    # Find the differences
    diff_set = set1.symmetric_difference(set2)
    return diff_set


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

    def group_tasks_by_time():
        """Group tasks by their start time and add them to the waiting queue."""
        nonlocal task_list
        for one_task in task_list:
            add_task_to_waiting_queue(one_task)

    def add_task_to_waiting_queue(one_task):
        """Add a task to the waiting queue at its start time."""
        nonlocal waitingTaskQueue
        start_time = one_task.actual_start_time
        if start_time not in waitingTaskQueue:
            waitingTaskQueue[start_time] = deque()
        waitingTaskQueue[start_time].append(one_task)

    def add_task_to_processing_queue(new_task):
        """Add a task to the processing queue and deduct its bandwidth from the total."""
        nonlocal total_bandwidth, processingQueue
        total_bandwidth -= new_task.bandwidth
        if total_bandwidth < 0:  # Bandwidth should not fall below zero
            DEBUG_HALT()
        new_task.status = TaskStatus.IN_PROGRESS
        processingQueue.append(new_task)

    def remove_task_from_processing_queue(task_to_remove=None):
        """Remove task from processing queue and re-add its bandwidth."""
        nonlocal total_bandwidth, processingQueue
        if task_to_remove:
            processingQueue.remove(task_to_remove)
        else:
            task_to_remove = processingQueue.pop()
        total_bandwidth += task_to_remove.bandwidth
        if total_bandwidth > orig_bandwidth:  # Bandwidth should not exceed original
            DEBUG_HALT()
        return task_to_remove

    def preempt_tasks_in_processing_queue(new_task):
        """
        Preempt tasks in the processing queue if necessary to make room for a new task.
        Tasks are preempted based on their priority and remaining duration.
        """
        nonlocal processingQueue, waitingTaskQueue, total_bandwidth, current_time
        preemptedTempQueue = deque()
        # Sort tasks by priority and remaining duration for preemption
        processingQueue = sort_list(processingQueue, 'priority', is_reverse=False)
        processingQueue = sort_list(processingQueue, 'remaining_duration', is_reverse=True)
        new_task_added = False
        for one_task in processingQueue:
            if one_task.priority <= new_task.priority:
                remove_task_from_processing_queue(one_task)
                preemptedTempQueue.append(one_task)
                if new_task.bandwidth <= total_bandwidth:
                    add_task_to_processing_queue(new_task)
                    new_task_added = True
                    break
        while preemptedTempQueue:
            one_task = preemptedTempQueue.pop()
            if new_task_added:
                one_task.preempt(current_time)
                add_task_to_waiting_queue(one_task)
            else:
                add_task_to_processing_queue(one_task)
        return new_task_added

    def finish_task(one_task, end_time):
        """Finish a task and move it to the completed queue."""
        nonlocal completedQueue
        one_task.status = TaskStatus.FINISHED
        one_task.actual_end_time = end_time
        remove_task_from_processing_queue(one_task)
        completedQueue.append(one_task)

    waitingTaskQueue = {}  # Initialize waiting queue grouped by start time
    group_tasks_by_time()
    processingQueue = []  # Initialize processing queue
    completedQueue = []  # Initialize completed tasks queue
    orig_bandwidth = total_bandwidth  # Store original bandwidth
    current_time = 0

    while waitingTaskQueue or processingQueue:
        # Remove tasks that are done from the processing queue
        for one_task in processingQueue:
            # Decrease remaining duration for tasks in progress
            one_task.remaining_duration -= 1
            if one_task.remaining_duration == 0:
                finish_task(one_task, current_time)

        # Process tasks at the current time
        try:
            current_time = sorted(waitingTaskQueue.keys())[0]
            one_queue = waitingTaskQueue.pop(current_time) # Pop the processed time slice from the waiting queue
            one_queue = deque(sort_list(one_queue, 'priority', is_reverse=True))
            while one_queue:
                one_task = one_queue.popleft()
                if one_task.bandwidth <= total_bandwidth:
                    add_task_to_processing_queue(one_task)
                else:
                    if not preempt_tasks_in_processing_queue(one_task):
                        # If task wasn't added to processing, increment its start time and requeue
                        one_task.actual_start_time += 1
                        add_task_to_waiting_queue(one_task)
        except IndexError:
            current_time += 1 # advance current time
            continue  # No tasks at the current time, move forward

    # check if there are lost tasks
    diff_list = compare_lists(task_list, completedQueue)
    if diff_list:
        DEBUG_HALT()

    return list(completedQueue)
