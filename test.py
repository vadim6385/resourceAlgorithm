import random
from collections import deque

from task import Task, TaskPriority
from taskmatrix import DEFAULT_END_TIME
from executor import Executor
from utils import DEBUG_HALT


def generate_random_tasks(num_tasks, max_bandwidth, start_time=0, end_time=DEFAULT_END_TIME):
    ret = deque()
    for i in range(num_tasks):
        task_bandwidth = random.randint(0, int(max_bandwidth/2))
        priority = random.randrange(TaskPriority.REGULAR, TaskPriority.ENTERPRISE + 10, 10)
        task_start_time = random.randint(start_time, int(end_time-1))
        max_duration = end_time - task_start_time
        duration = random.randint(1, max_duration)  # Use max_duration as the upper limit
        if (task_start_time + duration) > end_time:
            DEBUG_HALT()
        new_task = Task(bandwidth=task_bandwidth, start_time=task_start_time,
                        duration=duration, priority=priority)
        ret.append(new_task)
    return ret


def main():
    max_bandwidth = 100
    start_time = 0
    num_tasks = 50
    task_exec = Executor(max_bandwidth, start_time)
    task_generated_queue = generate_random_tasks(num_tasks=num_tasks, max_bandwidth=max_bandwidth)
    while task_generated_queue:
        task = task_generated_queue.popleft()
        task_exec.add_tasks(task)
    task_exec.execute_tasks()

if __name__ == "__main__":
    main()

