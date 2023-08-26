import task


class AlgoTester:
    def __init__(self, task_list_file, total_bandwith):
        self.total_bandwidth = total_bandwith
        self.task_list = task.from_json_file(task_list_file)
        self.completed_tasks = []
        self.avg_score = 0

    def test(self, algo_fp):
        # run the algorithm from given algorithm function
        self.completed_tasks = algo_fp(self.task_list, self.total_bandwidth)
        self.rate_tasks() # calculate score for each task

    def rate_tasks(self):
        total_score = 0
        for one_task in self.task_list:
            orig_start_time = one_task.created_time
            actual_start_time = one_task.actual_start_time
            task_priority = int(one_task.priority)
            old_score = one_task.score # default 100
            new_score = old_score - ((actual_start_time - orig_start_time) * task_priority) # formula for calculating task score
            one_task.score = new_score
            total_score += new_score
        self.avg_score = total_score / len(self.task_list)

if __name__ == "__main__":
    from algorithms import simple_greedy_algorithm
    task_list = "output.json"
    tester = AlgoTester(task_list, 50)
    tester.test(simple_greedy_algorithm)
    print(f"Average score: {tester.avg_score}")