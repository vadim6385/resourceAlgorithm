"""
Driver code
"""

from heatmap_plot import show_plot
from task import generate_random_tasks, reset_task_start_time_bandwidth
from executor import Executor
from utils import DEFAULT_END_TIME


def run_task_list(task_generated_list, compress, max_bandwidth=None, start_time=None,
                  display_plot=True, print_dropped_tasks=False):
    task_exec = Executor(max_bandwidth, start_time, compress=compress)
    for task in task_generated_list:
        task_exec.add_task(task)
    task_exec.execute_tasks()
    # print dropped tasks
    num_dropped_tasks = len(task_exec.dropped_tasks)
    if print_dropped_tasks:
        print("Number of dropped tasks: {}".format(num_dropped_tasks))
        print("Dropped task list:")
        [print(i) for i in task_exec.dropped_tasks]
    dropped_tasks_ratio = float(num_dropped_tasks / len(task_generated_list))
    if display_plot:
        show_plot(task_exec.task_matrix, num_dropped_tasks, dropped_tasks_ratio)
    return dropped_tasks_ratio


# run N simulations with generating new data each time, return average of dropped tasks ratio
def run_n_simulations(num_runs, max_bandwidth, start_time, end_time, num_tasks, is_compressed):
    sum_dropped_tasks_ratios = float(0)
    for _ in range(num_runs):
        task_gen_list = generate_random_tasks(num_tasks=num_tasks, max_bandwidth=max_bandwidth, start_time=start_time,
                                              end_time=end_time)
        one_ratio = run_task_list(task_gen_list, compress=is_compressed, display_plot=False,
                                  max_bandwidth=max_bandwidth, start_time=start_time)
        print("Run {:d} of {:d}, ratio - {:.2f}".format(_ + 1, num_runs, one_ratio))
        sum_dropped_tasks_ratios += one_ratio
    return sum_dropped_tasks_ratios / float(num_runs)


def single_run_w_plot(max_bandwidth, start_time, end_time, num_tasks, is_compressed, pre_gen_task_list=None):
    if pre_gen_task_list is None:
        task_gen_list = generate_random_tasks(num_tasks=num_tasks, max_bandwidth=max_bandwidth, start_time=start_time,
                                              end_time=end_time)
    else:
        task_gen_list = pre_gen_task_list
    run_task_list(task_gen_list, compress=is_compressed, display_plot=True,
                  max_bandwidth=max_bandwidth, start_time=start_time)


def main():
    max_bandwidth = 100
    start_time = 0
    end_time = DEFAULT_END_TIME
    num_tasks = 50
    num_of_runs = 100
    # display sample plot for uncompressed and compressed run on the same data set
    task_gen_list = generate_random_tasks(num_tasks=num_tasks, max_bandwidth=max_bandwidth, start_time=start_time,
                                          end_time=end_time)
    single_run_w_plot(max_bandwidth, start_time, end_time, num_tasks,
                      is_compressed=False, pre_gen_task_list=task_gen_list)
    reset_task_start_time_bandwidth(task_gen_list)
    single_run_w_plot(max_bandwidth, start_time, end_time, num_tasks,
                      is_compressed=True, pre_gen_task_list=task_gen_list)
    # run n simulations with randomly generated data
    uncompressed_ratio = run_n_simulations(num_runs=num_of_runs, max_bandwidth=max_bandwidth, start_time=start_time,
                                           end_time=end_time, num_tasks=num_tasks, is_compressed=False)
    print("Uncompressed runs average ratio for {:d} runs: {:.2f}".format(num_of_runs, uncompressed_ratio))
    compressed_ratio = run_n_simulations(num_runs=num_of_runs, max_bandwidth=max_bandwidth, start_time=start_time,
                                         end_time=end_time, num_tasks=num_tasks, is_compressed=True)
    print("Compressed runs average ratio for {:d} runs: {:.2f}".format(num_of_runs, compressed_ratio))





if __name__ == "__main__":
    main()
