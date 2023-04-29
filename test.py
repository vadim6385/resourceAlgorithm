"""
Driver code
"""

from heatmap_plot import show_plot
from task import generate_random_tasks, reset_task_start_time_bandwidth
from executor import Executor


def main(task_generated_list, compress):
    task_exec = Executor(max_bandwidth, start_time, compress=compress)
    for task in task_generated_list:
        task_exec.add_task(task)
    task_exec.execute_tasks()
    # print dropped tasks
    num_dropped_tasks = len(task_exec.starved_tasks)
    print("Number of dropped tasks: {}".format(num_dropped_tasks))
    print("Dropped task list:")
    [print(i) for i in task_exec.starved_tasks]
    show_plot(task_exec.task_matrix, num_dropped_tasks)


if __name__ == "__main__":
    max_bandwidth = 100
    start_time = 0
    num_tasks = 50
    task_gen_list = generate_random_tasks(num_tasks=num_tasks, max_bandwidth=max_bandwidth)
    main(task_gen_list, compress=False)
    reset_task_start_time_bandwidth(task_gen_list)
    main(task_gen_list, compress=True)

