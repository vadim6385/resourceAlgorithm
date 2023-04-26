# from isp import ISP
# from users import UserType, User
#
#
# def main():
#     total_bandwidth = 1000  # in Mbps
#
#     users = [
#         User(UserType.REGULAR, demand=100, start_time=0, end_time=10),
#         User(UserType.PREMIUM, demand=250, start_time=5, end_time=15),
#         User(UserType.ENTERPRISE, demand=500, min_bandwidth=50, start_time=10, end_time=20),
#         User(UserType.REGULAR, demand=400, start_time=0, end_time=10),
#         User(UserType.PREMIUM, demand=300, start_time=5, end_time=15),
#         User(UserType.ENTERPRISE, demand=700, min_bandwidth=50, start_time=10, end_time=20),
#         User(UserType.REGULAR, demand=50, start_time=0, end_time=10),
#         User(UserType.PREMIUM, demand=300, start_time=5, end_time=15),
#         User(UserType.ENTERPRISE, demand=900, min_bandwidth=50, start_time=10, end_time=20),
#     ]
#
#     isp = ISP(users, total_bandwidth)
#
#     for time_window in range(0, 25, 5):
#         print(f"Time window: {time_window}")
#         isp.allocate_bandwidth(time_window)
#         isp.display_bandwidth_allocation()
#         print("\n")

import random
from collections import deque

from task import Task, TaskPriority
from taskmatrix import DEFAULT_END_TIME
from executor import Executor


def generate_random_tasks(num_tasks, max_bandwidth, start_time=0, end_time=DEFAULT_END_TIME):
    ret = deque()
    for i in range(num_tasks):
        task_bandwidth = random.randint(0, max_bandwidth)
        priority = random.randrange(TaskPriority.REGULAR, TaskPriority.ENTERPRISE + 10, 10)
        task_start_time = random.randint(start_time, end_time-1)
        duration = random.randint(1, end_time/2)
        if task_start_time + duration > end_time:
            duration = duration - ((task_start_time + duration) - end_time)
        new_task = Task(bandwidth=task_bandwidth, start_time=task_start_time,
                        duration=duration, priority=priority)
        ret.append(new_task)
    return ret


def main():
    max_bandwidth = 1000
    start_time = 0
    num_tasks = 100
    task_exec = Executor(max_bandwidth, start_time)
    task_generated_queue = generate_random_tasks(num_tasks=num_tasks, max_bandwidth=max_bandwidth)
    while task_generated_queue:
        task = task_generated_queue.popleft()
        task_exec.add_tasks(task)
    task_exec.execute_tasks()

if __name__ == "__main__":
    main()

