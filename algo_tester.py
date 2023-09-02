import task
import numpy as np

from heatmap_plot import TaskHeatmap
from utils import DEBUG_HALT


class AlgoTester:
    def __init__(self, task_list_file, total_bandwith):
        self.task_matrix = None
        self.total_bandwidth = total_bandwith
        self.task_list = task.from_json_file(task_list_file)
        self.completed_tasks = []
        self.scores_dict = {}
        self.time_start = 0
        self.time_end = 0

    def test(self, algo_fp):
        # run the algorithm from given algorithm function
        self.completed_tasks = algo_fp(self.task_list, self.total_bandwidth)
        # get earliest task scheduled start time and latest task completion time
        self.time_start = min(one_task.created_time for one_task in self.completed_tasks)
        self.time_end = max(one_task.actual_end_time for one_task in self.completed_tasks)
        self.rate_tasks()  # calculate score for each task
        self.create_task_matrix()

    def rate_tasks(self):
        priority_names = [name for name, member in task.TaskPriority.__members__.items()]
        self.scores_dict = {priority: [0, 0, 0] for priority in
                            priority_names}  # { "PRIORITY" : [num_tasks, total_score, avg_score] }
        for one_task in self.completed_tasks:
            orig_start_time = one_task.created_time
            actual_start_time = one_task.actual_start_time
            task_priority = one_task.priority.name
            new_score = actual_start_time - orig_start_time
            one_task.score = new_score
            self.scores_dict[task_priority][0] += 1
            self.scores_dict[task_priority][1] += new_score
        for one_prio in self.scores_dict:
            tasks_num = self.scores_dict[one_prio][0]
            total_score = self.scores_dict[one_prio][1]
            avg_score = total_score / tasks_num
            self.scores_dict[one_prio][2] = int(avg_score)
        return self.scores_dict

    def avg_score_per_priority_str(self):
        ret = "Average Score per priority: "
        for one_prio in self.scores_dict.keys():
            ret += "{}:{} ".format(one_prio, self.scores_dict[one_prio][2])
        ret += ". "
        ret += f"Total Start Time: {self.time_start}, Total End Time: {self.time_end}"
        return ret

    def create_task_matrix(self):
        self.task_matrix = np.zeros((self.total_bandwidth, self.time_end + 1), dtype=int)
        for one_task in self.completed_tasks:
            for time in range(one_task.actual_start_time, one_task.actual_end_time + 1):
                allocated = False
                for bw in range(self.total_bandwidth):
                    if all(self.task_matrix[bw:bw + one_task.bandwidth, time] == 0):
                        self.task_matrix[bw:bw + one_task.bandwidth, time] = one_task.id
                        allocated = True
                        break
                if not allocated:
                    DEBUG_HALT()
        # sort the matrix
        for time in range(self.time_end + 1):
            self.task_matrix[:, time] = np.sort(self.task_matrix[:, time])

    def show_heatmap_plot(self):
        if self.task_matrix is None:
            raise Exception("Plot can be shown only after tasks have been ran")
        heatmap_plot = TaskHeatmap(task_matrix=self.task_matrix)
        heatmap_plot.show_plot()


if __name__ == "__main__":
    from algorithms import simple_greedy_algorithm
    task_list = "output.json"
    tester = AlgoTester(task_list, 50)
    tester.test(simple_greedy_algorithm)
    print(f"Greedy algorithm average score: {tester.avg_score_per_priority_str()}")
    tester.show_heatmap_plot()
    del (tester)
    from algorithms import greedy_compression_algorithm
    tester = AlgoTester(task_list, 50)
    tester.test(greedy_compression_algorithm)
    print(f"Greedy compression algorithm average score: {tester.avg_score_per_priority_str()}")
    tester.show_heatmap_plot()
