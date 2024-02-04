import numpy as np
import multiprocessing as mps
from datetime import datetime

import task
import task_gen
from algorithms import greedy_compression_algorithm, preemptive_scheduling_algorithm, simple_greedy_algorithm
from heatmap_plot import TaskHeatmap
from utils import DEBUG_HALT


class AlgoTester:
    def __init__(self, task_list_file, total_bandwidth):
        # Initialize the task matrix, total bandwidth, and task list from a JSON file
        self.task_matrix = None
        self.total_bandwidth = total_bandwidth
        self.task_list = task_gen.from_json_file(task_list_file)
        self.completed_tasks = []
        self.scores_dict = {}
        self.time_start = 0
        self.time_end = 0

    def test(self, algo_fp):
        """
        Test the given algorithm function pointer.
        :param algo_fp: Algorithm function pointer to be tested.
        """
        # Run the algorithm and store the completed tasks
        self.completed_tasks = algo_fp(self.task_list, self.total_bandwidth)
        # Determine the earliest task start time and the latest task end time
        self.time_start = min(one_task.created_time for one_task in self.completed_tasks)
        self.time_end = max(one_task.actual_end_time for one_task in self.completed_tasks)
        self.rate_tasks()  # Calculate the score for each task

    def rate_tasks(self):
        """
        Rate the tasks based on their start time and priority.
        """
        # Get all priority names
        priority_names = [name for name, member in task.TaskPriority.__members__.items()]
        # Initialize scores dictionary with priorities
        self.scores_dict = {priority: [0, 0, 0] for priority in priority_names}
        for one_task in self.completed_tasks:
            # Calculate the score for each task based on start times
            one_task.rate()
            # Update the scores dictionary
            task_priority = one_task.priority.name
            self.scores_dict[task_priority][0] += 1
            self.scores_dict[task_priority][1] += one_task.score
        # Calculate the average score for each priority
        for one_prio in self.scores_dict:
            tasks_num = self.scores_dict[one_prio][0]
            total_score = self.scores_dict[one_prio][1]
            try:
                avg_score = int(total_score / tasks_num)
            except ZeroDivisionError:
                avg_score = "N/A"
            self.scores_dict[one_prio][2] = avg_score
        return self.scores_dict

    def avg_score_per_priority_str(self):
        """
        Return a string representation of the average score per priority.
        """
        ret = "Average Score per priority: "
        for one_prio in self.scores_dict.keys():
            ret += "{}:{} ".format(one_prio, self.scores_dict[one_prio][2])
        ret += ". Total Start Time: {}, Total End Time: {}".format(self.time_start, self.time_end)
        return ret

    def create_task_matrix(self):
        """
        Create a task matrix representing the allocation of tasks over time and bandwidth.
        """
        self.task_matrix = np.zeros((self.total_bandwidth, self.time_end + 1), dtype=int)
        for one_task in self.completed_tasks:

            for time in range(one_task.actual_start_time, one_task.actual_end_time + 1):
                if one_task.is_preempted:
                    for one_tup in one_task.preempted_times_list:
                        if one_tup[0] <= time <= one_tup[1]:
                            if all(self.task_matrix[bw:bw + one_task.bandwidth, time] == 0):
                                self.task_matrix[bw:bw + one_task.bandwidth, time] = one_task.id
                                break
                allocated = False
                for bw in range(self.total_bandwidth):
                    # Check if the bandwidth is available for the task at the given time
                    if all(self.task_matrix[bw:bw + one_task.bandwidth, time] == 0):
                        self.task_matrix[bw:bw + one_task.bandwidth, time] = one_task.id
                        allocated = True
                        break
                if not allocated:
                    DEBUG_HALT()
        # Sort the matrix for each time unit
        for time in range(self.time_end + 1):
            self.task_matrix[:, time] = np.sort(self.task_matrix[:, time])

    def show_heatmap_plot(self):
        """
        Show a heatmap plot of the task matrix.
        """
        self.create_task_matrix()  # Create the task matrix
        heatmap_plot = TaskHeatmap(task_matrix=self.task_matrix)
        heatmap_plot.show_plot()


def algo_worker(l, algo_fp, algo_name, task_list_type, value_tuple, max_bandwidth, log_file=None):
    """
    Worker function that runs algorithms in multiple processes.
    :param log_file: log file to write to, default no log file
    :param l: multiprocessing Lock object
    :param algo_fp: Function pointer to the algorithm.
    :param algo_name: Name of the algorithm for display purposes.
    :param task_list_type: Type or identifier of the task list being processed.
    :param value_tuple: Tuple containing the task list file and its description.
    :param max_bandwidth: Maximum bandwidth per task.
    :return: None.
    """
    task_list_file = value_tuple[0]  # Extract the task list file from the tuple
    explanation_string = value_tuple[1]  # Extract the explanation string from the tuple
    tester = AlgoTester(task_list_file, max_bandwidth)  # Initialize the AlgoTester with the task list and bandwidth
    tester.test(algo_fp)  # Run the algorithm function on the tester
    # Output the results
    now = datetime.now()
    date_time = f"Run Time: {now.strftime("%m/%d/%Y, %H:%M:%S")}"
    task_list_str = f"{task_list_type}: {explanation_string}"
    algo_score_str = f"{algo_name} average score for Task List \"{task_list_type}\": {tester.avg_score_per_priority_str()}\n"
    l.acquire()  # acquire lock for printing
    # if given log file name, write to log
    if log_file:
        with open(log_file, "a+") as f:
            f.write(date_time + "\n")
            f.write(task_list_str + "\n")
            f.write(algo_score_str + "\n")
    print(date_time)
    print(task_list_str)
    print(algo_score_str)
    # Uncomment the next line to show heatmap plots if needed
    # tester.show_heatmap_plot()
    l.release()  # release lock for printing


def main(log_file=None, clear_log=True):
    if log_file and clear_log:
        open(log_file, "w").close()
    max_bandwidth = 50  # Define the maximum bandwidth
    # List of algorithms and their names
    algo_functions = [(simple_greedy_algorithm, "Simple greedy algorithm"),
                      (greedy_compression_algorithm, "Greedy compression algorithm"),
                      (preemptive_scheduling_algorithm, "Preemptive scheduling algorithm")]
    # Dictionary mapping task list types to their respective files and descriptions
    task_lists_dict = {"Random": ("task_list_random.json", "Generated queue of random tasks"),
                       "A": ("task_list_a.json",
                             "Created tasks as: lowest priority first, premium priority second, enterprise priority third"),
                       "B": ("task_list_b.json",
                             "Created tasks as: lowest and premium priority first, enterprise priority second"),
                       "C": ("task_list_c.json",
                             "Created chunks of three tasks of same priority, first will be 0.6 of max bandwidth, two more will be exactly half bandwidth")}

    procs = []  # List to keep track of process objects
    lock = mps.Lock()
    # Create a process for each algorithm on each task list
    for algo_fp, algo_name in algo_functions:
        for key, value_tuple in task_lists_dict.items():
            p = mps.Process(target=algo_worker, args=(lock, algo_fp, algo_name, key, value_tuple, max_bandwidth, log_file,))
            procs.append(p)  # Add the process to the list
    # Start each process
    for p in procs:
        p.start()
    # Wait for all processes to finish
    for p in procs:
        p.join()


if __name__ == "__main__":
    main("log.txt", clear_log=True)  # Run the main function
