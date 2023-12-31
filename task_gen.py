import json
import random
from _operator import attrgetter

from task import TaskPriority, Task
from utils import DEFAULT_END_TIME, DEBUG_HALT


def generate_random_tasks(num_tasks, max_bandwidth, start_time=0, end_time=DEFAULT_END_TIME):
    """
    generate queue of random tasks
    :param num_tasks: number of tasks to generate
    :param max_bandwidth: maximum bandwidth for the task
    :param start_time: global task start time
    :param end_time: global task end time
    :return: list of generated tasks
    """
    ret = []
    for i in range(num_tasks):
        task_bandwidth = random.randint(0, int(max_bandwidth / 2))
        task_min_bandwidth = random.randint(0, task_bandwidth)
        priority = random.randrange(TaskPriority.REGULAR, TaskPriority.ENTERPRISE + 1, 1)
        task_created_time = random.randint(start_time, int(end_time - 1))
        max_duration = end_time - task_created_time
        duration = random.randint(1, max_duration)  # Use max_duration as the upper limit
        if (task_created_time + duration) > end_time:
            DEBUG_HALT()
        new_task = Task(bandwidth=task_bandwidth, created_time=task_created_time,
                        duration=duration, min_bandwidth=task_min_bandwidth)
        new_task.priority = priority
        ret.append(new_task)
    return sorted(ret, key=attrgetter('created_time'))


def to_json_file(task_list, out_file):
    """
    get task list, save it in JSON format
    :param task_list: task input
    :param out_file: output file name
    :return: None
    """
    target_list = []
    for task in task_list:
        task_dict = task.to_dict()
        target_list.append(task_dict)
    with open(out_file, "w") as fout:
        json.dump(target_list, fout, indent=4)


def from_json_file(in_file: str) -> list:
    """
    get task list from JSON file (list of dicts
    :param in_file: JSON file with list of dicts
    :return: list of Task objects
    """
    ret = []
    with open(in_file, "r") as fin:
        list_dicts = json.load(fin)
    for one_dict in list_dicts:
        new_task = Task()
        new_task.from_dict(one_dict)
        ret.append(new_task)
    return ret


def compare_lists(src_list, target_list):
    zipped = list(zip(src_list, target_list))
    for (i, j) in zipped:
        if i.to_dict() != j.to_dict():
            DEBUG_HALT()
