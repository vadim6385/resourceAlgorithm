"""
Driver code
"""

import random
from collections import deque
import seaborn as sns
import matplotlib.pylab as plt

from task import Task, TaskPriority
from taskmatrix import DEFAULT_END_TIME
from executor import Executor
from utils import DEBUG_HALT


def generate_random_tasks(num_tasks, max_bandwidth, start_time=0, end_time=DEFAULT_END_TIME):
    ret = deque()
    for i in range(num_tasks):
        task_bandwidth = random.randint(0, int(max_bandwidth/2))
        priority = random.randrange(TaskPriority.REGULAR, TaskPriority.ENTERPRISE + 10, 10)
        task_created_time = random.randint(start_time, int(end_time-1))
        max_duration = end_time - task_created_time
        duration = random.randint(1, max_duration)  # Use max_duration as the upper limit
        if (task_created_time + duration) > end_time:
            DEBUG_HALT()
        new_task = Task(bandwidth=task_bandwidth, created_time=task_created_time,
                        duration=duration, priority=priority)
        ret.append(new_task)
    return ret


def show_plot(task_matrix):
    ax = sns.heatmap(task_matrix, cmap="YlGnBu")
    plt.title("Task allocation graph", fontsize=20)
    plt.xlabel("t(sec)")
    plt.ylabel("Bandwith(Mbps")
    plt.show()


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
    show_plot(task_exec.task_matrix.data)


if __name__ == "__main__":
    main()

