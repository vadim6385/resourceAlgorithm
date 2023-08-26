import task


class AlgoTester:
    def __init__(self, task_list_file, total_bandwith):
        self.total_bandwidth = total_bandwith
        self.task_list = task.from_json_file(task_list_file)

    def test(self, algo_fp):
        # run the algorithm from given algorithm function
        completed_tasks = algo_fp(self.task_list, self.total_bandwidth)
        