"""
Driver code
"""

import seaborn as sns
import matplotlib.pylab as plt

from task import generate_random_tasks
from executor import Executor


def show_plot(task_matrix, dropped_tasks):
    ax = sns.heatmap(task_matrix, cmap="YlGnBu")
    plt.title("Task allocation graph, dropped tasks: {}".format(dropped_tasks), fontsize=20)
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
        task_exec.add_task(task)
    task_exec.execute_tasks()
    # print dropped tasks
    num_dropped_tasks = len(task_exec.starved_tasks)
    print("Number of dropped tasks: {}".format(num_dropped_tasks))
    print("Dropped task list:")
    [print(i) for i in task_exec.starved_tasks]
    show_plot(task_exec.task_matrix.data, num_dropped_tasks)


if __name__ == "__main__":
    main()

