"""
The class represents a task with attributes for bandwidth, start time, duration, and priority.
It includes getter and setter methods to access and modify these attributes.
"""
import json
import random
from enum import IntEnum
from itertools import count
from operator import attrgetter

from utils import DEBUG_HALT, DEFAULT_END_TIME


class TaskPriority(IntEnum):
    REGULAR = 1
    PREMIUM = 2
    ENTERPRISE = 3


class InsufficientBandwidthException(Exception):
    def __init__(self, task_id):
        super().__init__("Insufficient bandwidth for task: {}".format(task_id))


class Task:
    # create counter object for generating task id
    id_iter = count(start=1, step=1)

    # Initialize Task object with bandwidth, created_time, duration, and priority
    def __init__(self, bandwidth=0, created_time=0, duration=0, priority=TaskPriority.REGULAR, min_bandwidth=0):
        self.__id = next(self.id_iter)
        self.__bandwidth = bandwidth
        self.__original_bandwidth = bandwidth
        self.__min_bandwidth = min_bandwidth
        self.__created_time = created_time
        self.__actual_start_time = created_time
        self.__duration = duration
        self.priority = priority
        self.__score = 0

    # get task score
    @property
    def score(self) -> int:
        return self.__score

    # set task score
    @score.setter
    def score(self, val: int) -> None:
        self.__score = val

    # get unique task Id
    @property
    def id(self):
        return self.__id

    # Get bandwidth of the task
    @property
    def bandwidth(self):
        return self.__bandwidth

    # Get original bandwidth for the task
    @property
    def original_bandwidth(self):
        return self.__original_bandwidth

    # get minimum bandwidth required for the task
    @property
    def min_bandwidth(self):
        return self.__min_bandwidth

    # set task bandwidth, but not below min bandwidth
    @bandwidth.setter
    def bandwidth(self, val):
        if val < self.__min_bandwidth:
            raise InsufficientBandwidthException(self.__id)
        self.__bandwidth = val

    # Is the task already compressed?
    @property
    def is_compressed(self):
        return self.__bandwidth == self.__min_bandwidth

    @property
    def bandwidth_diff(self):
        return self.__original_bandwidth - self.__bandwidth

    # Get created time of the task
    @property
    def created_time(self):
        return self.__created_time

    @property
    def actual_start_time(self):
        return self.__actual_start_time

    @actual_start_time.setter
    def actual_start_time(self, val):
        self.__actual_start_time = val

    # Get duration of the task
    @property
    def duration(self):
        return self.__duration

    # Get priority of the task
    @property
    def priority(self) -> TaskPriority:
        return self.__priority

    # Set new priority for the task
    @priority.setter
    def priority(self, val):
        if type(val) == TaskPriority:
            self.__priority = val
        elif type(val) == int:
            self.__priority = TaskPriority(val)
        elif type(val) == str:
            try:
                self.__priority = TaskPriority[val.upper()]
            except KeyError:
                DEBUG_HALT()
        else:
            raise Exception("Task priority accepts only int, string or TaskPriority")

    @property
    def actual_end_time(self):
        return self.__actual_start_time + self.__duration

    # reset task start time to original task start time
    def reset_start_time(self):
        self.__actual_start_time = self.__created_time

    # compress the task to minimal bandwidth
    def compress(self):
        self.__bandwidth = self.__min_bandwidth

    # decompress bandwidth
    def decompress(self):
        self.__bandwidth = self.__original_bandwidth

    def __lt__(self, other):
        if self.priority == other.priority:
            return self.created_time < other.created_time
        return self.priority < other.priority

    # String representation of the Task object
    def __repr__(self):
        return "Task(id={} bandwidth={}, minimum bandwidth={}, original bandwidth={}, created_time={}, actual start " \
               "time={}, duration={}, actual end time={}, priority={})".format(
            self.id,
            self.bandwidth,
            self.min_bandwidth,
            self.original_bandwidth,
            self.created_time,
            self.actual_start_time,
            self.duration,
            self.actual_end_time,
            self.priority.name)

    def to_dict(self):
        return {
            'id': self.__id,
            'bandwidth': self.__bandwidth,
            'min_bandwidth': self.__min_bandwidth,
            'original_bandwidth': self.__original_bandwidth,
            'created_time': self.__created_time,
            'actual_start_time': self.__actual_start_time,
            'duration': self.__duration,
            'actual_end_time': self.actual_end_time,
            'priority': self.__priority.name,  # Assuming TaskPriority is an Enum
        }

    def from_dict(self, src_dict):
        """update task parameters from dictionary"""
        self.__id = src_dict['id']
        self.__bandwidth = src_dict['bandwidth']
        self.__min_bandwidth = src_dict['min_bandwidth']
        self.__original_bandwidth = src_dict['original_bandwidth']
        self.__created_time = src_dict['created_time']
        self.__actual_start_time = src_dict['actual_start_time']
        self.__duration = src_dict['duration']
        self.priority = src_dict['priority']


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


def reset_task_start_time_bandwidth(tasks_list):
    """
    reset start time and bandwidth for tasks
    :param tasks: tasks to reset
    :return: None
    """
    for task in tasks_list:
        task.reset_start_time()
        task.reset_bandwidth()


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


if __name__ == "__main__":
    task_list = generate_random_tasks(100, 50)
    json_file = "output.json"
    to_json_file(task_list, json_file)
    output_list = from_json_file(json_file)
    print(output_list)
    compare_lists(task_list, output_list)
    # for task in task_list:
    #     print(task.to_dict())
