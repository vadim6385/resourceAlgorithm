import heapq
from collections import deque

from task import TaskStatus
from utils import DEBUG_HALT, ASSERT


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
    # Initialize task queues and variables
    waitingTaskQueue = deque(sorted(task_list, key=lambda x: (x.actual_start_time, -x.priority)))  # Waiting tasks are sorted by start time and priority
    processingQueue = []  # Tasks that are currently being processed
    completedQueue = []  # Tasks that have been completed
    orig_bandwidth = total_bandwidth  # Original total bandwidth, for reference
    current_time = 0  # Start time of the scheduling

    def add_task_to_processing_queue(task):
        """Adds a task to the processing queue and allocates bandwidth."""
        nonlocal total_bandwidth
        # Check if enough bandwidth is available for the task
        if total_bandwidth >= task.bandwidth:
            total_bandwidth -= task.bandwidth  # Allocate bandwidth
            task.status = 'IN_PROGRESS'  # Update task status
            processingQueue.append(task)  # Add to processing queue
        else:
            # Handle error if bandwidth is insufficient
            ASSERT("Insufficient Bandwidth")

    def finish_task(task):
        """Marks a task as finished and releases its bandwidth."""
        nonlocal total_bandwidth
        task.status = 'FINISHED'  # Update task status
        completedQueue.append(task)  # Move task to completed queue
        processingQueue.remove(task)  # Remove task from processing queue
        total_bandwidth += task.bandwidth  # Release bandwidth back to the pool

    def preempt_tasks():
        """Preempts tasks to free up bandwidth for higher priority tasks."""
        nonlocal processingQueue
        nonlocal total_bandwidth
        # Sort processing queue based on priority and remaining duration
        processingQueue = sorted(processingQueue, key=lambda x: (-x.priority, x.remaining_duration), reverse=True)
        # Preempt tasks if there is not enough bandwidth
        while processingQueue and total_bandwidth < orig_bandwidth:
            task = processingQueue.pop()  # Remove the least urgent task
            total_bandwidth += task.bandwidth  # Reclaim its bandwidth
            task.preempt(current_time)  # Handle task preemption logic
            waitingTaskQueue.appendleft(task)  # Put the task back in the waiting queue

    # Main loop to process tasks until all are completed
    while waitingTaskQueue or processingQueue:
        # Check and start tasks that are ready to run
        while waitingTaskQueue and waitingTaskQueue[0].actual_start_time <= current_time:
            task = waitingTaskQueue.popleft()
            if task.bandwidth <= total_bandwidth:
                add_task_to_processing_queue(task)
            else:
                # If not enough bandwidth, try preempting tasks
                waitingTaskQueue.appendleft(task)
                preempt_tasks()
                # Try to add the task again if bandwidth is now available
                if task.bandwidth <= total_bandwidth:
                    add_task_to_processing_queue(waitingTaskQueue.popleft())

        # Update processing tasks and finish those that are done
        for task in list(processingQueue):
            task.remaining_duration -= 1  # Decrement remaining duration of each task
            if task.remaining_duration <= 0:
                finish_task(task)  # Finish tasks with no remaining duration

        # Increment the current time for the next cycle
        current_time += 1

    # Return the list of completed tasks
    return completedQueue
