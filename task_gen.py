import json
import random
from _operator import attrgetter

from task import TaskPriority, Task
from utils import DEFAULT_END_TIME, DEBUG_HALT


def generate_random_tasks(num_tasks, max_bandwidth, start_time=0, end_time=DEFAULT_END_TIME, priority=None, sort_tasks=True):
    """
    generate queue of random tasks
    :param sort_tasks: sort tasks by created time, default True
    :param priority: set priority, by default priority is set at random
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
        if not priority:
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
    return sorted(ret, key=attrgetter('created_time')) if sort_tasks else ret


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


def gen_tasks_lowest_priority_first(num_tasks, max_bandwidth, start_time=0, end_time=DEFAULT_END_TIME):
    """
    generate tasks as:
    lowest priority first, premium priority second, enterprise priority third
    :param num_tasks: number of tasks to generate
    :param max_bandwidth: maximum bandwidth for the task
    :param start_time: global task start time
    :param end_time: global task end time
    :return: combined list of tasks, starting with the lowest priority (regular) to the highest (enterprise)
    """
    # Divide the number of tasks equally among the three priority levels.
    num_tasks_ent_prio = num_tasks_prem_prio = int(num_tasks / len(TaskPriority))
    num_tasks_reg_prio = num_tasks - num_tasks_ent_prio - num_tasks_prem_prio  # Remainder goes to regular priority

    # Define time intervals for each priority level tasks. The day is divided into three equal parts.
    start_time_reg_prio = start_time
    end_time_reg_prio = int(end_time / len(TaskPriority))  # End time for regular priority tasks
    start_time_prem_prio = end_time_reg_prio  # Start time for premium priority tasks right after regular tasks
    end_time_prem_prio = start_time_prem_prio + end_time_reg_prio  # End time for premium priority tasks
    start_time_ent_prio = end_time_prem_prio  # Start time for enterprise priority tasks after premium tasks
    end_time_ent_prio = end_time  # End time for enterprise priority is the end of the period

    # Generate a list of random tasks for each priority type
    # Each list is sorted by some criterion within generate_random_tasks function
    reg_tasks_list = generate_random_tasks(num_tasks=num_tasks_reg_prio, max_bandwidth=max_bandwidth,
                                           start_time=start_time_reg_prio, end_time=end_time_reg_prio,
                                           priority=TaskPriority.REGULAR, sort_tasks=True)
    prem_tasks_list = generate_random_tasks(num_tasks=num_tasks_prem_prio, max_bandwidth=max_bandwidth,
                                            start_time=start_time_prem_prio, end_time=end_time_prem_prio,
                                            priority=TaskPriority.PREMIUM, sort_tasks=True)
    ent_tasks_list = generate_random_tasks(num_tasks=num_tasks_ent_prio, max_bandwidth=max_bandwidth,
                                           start_time=start_time_ent_prio, end_time=end_time_ent_prio,
                                           priority=TaskPriority.ENTERPRISE, sort_tasks=True)

    # Return a combined list of tasks, starting with the lowest priority (regular) to the highest (enterprise)
    return sorted(reg_tasks_list + prem_tasks_list + ent_tasks_list, key=attrgetter('created_time'))


def gen_tasks_reg_and_prem_first_ent_last(num_tasks, max_bandwidth, start_time=0, end_time=DEFAULT_END_TIME):
    """
    generate tasks as:
    lowest and premium priority first, enterprise priority second
    :param num_tasks: number of tasks to generate
    :param max_bandwidth: maximum bandwidth for the task
    :param start_time: global task start time
    :param end_time: global task end time
    :return: combined list of tasks, starting with the lowest priority (regular) to the highest (enterprise)
    """
    # Divide the number of tasks equally among the three priority levels.
    num_tasks_ent_prio = num_tasks_prem_prio = int(num_tasks / len(TaskPriority))
    num_tasks_reg_prio = num_tasks - num_tasks_ent_prio - num_tasks_prem_prio  # Remainder goes to regular priority

    # Define time intervals for each priority level tasks.
    start_time_reg_prem_prio = start_time # Start time for regular and premium priority tasks
    end_time_reg_prem_prio = int(end_time * (2/len(TaskPriority))) # End time for regular and premium priority tasks
    start_time_ent_prio = end_time_reg_prem_prio # Start time for enterprise priority tasks after regular and premium tasks
    end_time_ent_prio = end_time # End time for enterprise priority tasks after regular and premium tasks

    # Generate a list of random tasks for each priority type
    # Each list is sorted by some criterion within generate_random_tasks function

    reg_tasks_list = generate_random_tasks(num_tasks=num_tasks_reg_prio, max_bandwidth=max_bandwidth,
                                           start_time=start_time_reg_prem_prio, end_time=end_time_reg_prem_prio,
                                           priority=TaskPriority.REGULAR, sort_tasks=True)
    prem_tasks_list = generate_random_tasks(num_tasks=num_tasks_prem_prio, max_bandwidth=max_bandwidth,
                                            start_time=start_time_reg_prem_prio, end_time=end_time_reg_prem_prio,
                                            priority=TaskPriority.PREMIUM, sort_tasks=True)
    ent_tasks_list = generate_random_tasks(num_tasks=num_tasks_ent_prio, max_bandwidth=max_bandwidth,
                                           start_time=start_time_ent_prio, end_time=end_time_ent_prio,
                                           priority=TaskPriority.ENTERPRISE, sort_tasks=True)

    # Return a combined list of tasks, starting with the lowest priority (regular) to the highest (enterprise)
    return sorted(reg_tasks_list + prem_tasks_list + ent_tasks_list, key=attrgetter('created_time'))


def gen_tasks_high_bandwidth_usage(num_tasks, max_bandwidth, start_time=0,
                                   max_duration=10, end_time=DEFAULT_END_TIME, priority=TaskPriority.ENTERPRISE):
    """
    create chunks of three tasks of same priority, first will be 0.6 of max bandwidth, two more will be exactly half bandwidth
    :param max_duration: maximum duration per task
    :param priority: set priority, by default priority is set at random
    :param num_tasks: number of tasks to generate
    :param max_bandwidth: maximum bandwidth for the task
    :param start_time: global task start time
    :param end_time: global task end time
    :return: list of generated tasks
    """
    # Initialize an empty list to store the tasks
    retlist = []
    # Initialize task start time
    task_start_time = start_time
    # Iterate over the tasks in steps of 3 to group them for bandwidth allocation
    for i in range(0, num_tasks, 3):
        # Set high bandwidth usage for tasks (60% of max, then dividing the rest equally among two tasks)
        task_bandwidths = [int(max_bandwidth * 0.6), int(max_bandwidth / 2), int(max_bandwidth / 2)]
        # Initialize minimum bandwidths and durations for each task as 0
        task_min_bandwidths = [0, 0, 0]
        task_durations = [0, 0, 0]
        # Randomly assign duration and minimum bandwidth for each task
        for i in range(len(task_durations)):
            task_durations[i] = random.randint(1, max_duration)  # Random duration between 1 and max_duration
            task_min_bandwidths[i] = random.randint(0, task_bandwidths[i])  # Random min bandwidth up to the task's bandwidth
        # Create and append each task to the return list with the specified attributes
        for i in range(len(task_durations)):
            new_task = Task(bandwidth=task_bandwidths[i], created_time=task_start_time,
                            duration=task_durations[i], min_bandwidth=task_min_bandwidths[i], priority=priority)
            retlist.append(new_task)
        # Increment the start time for the next set of tasks
        task_start_time += max_duration
    # Return the list of tasks
    return retlist


if __name__ == "__main__":
    num_tasks = 1000
    max_bandwidth = 50
    start_time = 0
    max_duration = 20
    end_time = DEFAULT_END_TIME

    # generate lots of tasks with regular+premium priority first, then enterprise
    task_list_a = gen_tasks_reg_and_prem_first_ent_last(num_tasks=num_tasks, max_bandwidth=max_bandwidth,
                                                        start_time=start_time, end_time=end_time)
    to_json_file(task_list_a, "task_list_a.json")

    # generate lots of tasks with regular priority first, premium priority second, then enterprise
    task_list_b = gen_tasks_lowest_priority_first(num_tasks=num_tasks, max_bandwidth=max_bandwidth,
                                                        start_time=start_time, end_time=end_time)
    to_json_file(task_list_b, "task_list_b.json")

    # create chunks of three tasks of same priority, first will be 0.6 of max bandwidth, two more will be exactly half bandwidth
    task_list_c = gen_tasks_high_bandwidth_usage(num_tasks=num_tasks, max_bandwidth=max_bandwidth,
                                                        start_time=start_time, end_time=end_time, max_duration=max_duration)
    to_json_file(task_list_c, "task_list_c.json")