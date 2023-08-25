"""
The class represents a task with attributes for bandwidth, start time, duration, and priority.
It includes getter and setter methods to access and modify these attributes.
"""
import random
from itertools import count
from operator import attrgetter
import json

from taskinprogressmatrix import DEFAULT_END_TIME
from utils import DEBUG_HALT, TaskPriority, TaskStatus


class InsufficientBandwidthException(Exception):
    def __init__(self, task_id):
        super().__init__("Insufficient bandwidth for task: {}".format(task_id))


class Task:
    # create counter object for generating task id
    id_iter = count(start=1, step=1)

    # Initialize Task object with bandwidth, created_time, duration, and priority
    def __init__(self, bandwidth, created_time, duration, priority, min_bandwidth=0):
        self.__id = next(self.id_iter)
        self.__bandwidth = bandwidth
        self.__original_bandwidth = bandwidth
        self.__min_bandwidth = min_bandwidth
        self.__created_time = created_time
        self.__actual_start_time = created_time
        self.__duration = duration
        self.__priority = priority
        self.__task_status = TaskStatus.PENDING

    # get unique task Id
    @property
    def id(self):
        return self.__id

    # Get task status
    @property
    def status(self) -> TaskStatus:
        return self.__task_status

    # Set task status
    @status.setter
    def status(self, val: TaskStatus):
        self.__task_status = val

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
    def priority(self):
        return self.__priority

    # Set new priority for the task
    @priority.setter
    def priority(self, val):
        self.__priority = val

    @property
    def actual_end_time(self):
        return self.__actual_start_time + self.__duration

    # reset task start time to original task start time
    def reset_start_time(self):
        self.__actual_start_time = self.__created_time

    # reset task bandwidth to original task bandwidth
    def reset_bandwidth(self):
        self.__bandwidth = self.__original_bandwidth

    # compress the task to minimal bandwidth
    def compress(self):
        self.__bandwidth = self.__min_bandwidth

    # decompress bandwidth
    def decompress(self):
        self.reset_bandwidth()

    # String representation of the Task object
    def __repr__(self):
        return "Task(id={} bandwidth={}, minimum bandwidth={}, original bandwidth={}, created_time={}, actual start " \
               "time={}, duration={}, actual end time={}, priority={})".format(
                self.__id,
                self.__bandwidth,
                self.__min_bandwidth,
                self.__original_bandwidth,
                self.__created_time,
                self.__actual_start_time,
                self.__duration,
                self.actual_end_time,
                self.__priority)

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
            'priority': self.__priority,
            'status': self.__task_status.name  # Assuming TaskStatus is an Enum
        }



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
        priority = random.randrange(TaskPriority.REGULAR, TaskPriority.ENTERPRISE + 10, 10)
        task_created_time = random.randint(start_time, int(end_time - 1))
        max_duration = end_time - task_created_time
        duration = random.randint(1, max_duration)  # Use max_duration as the upper limit
        if (task_created_time + duration) > end_time:
            DEBUG_HALT()
        new_task = Task(bandwidth=task_bandwidth, created_time=task_created_time,
                        duration=duration, priority=priority, min_bandwidth=task_min_bandwidth)
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


if __name__ == "__main__":
    task_list = generate_random_tasks(5, 50)
    json_file = "output.json"
    to_json_file(task_list, json_file)
    # for task in task_list:
    #     print(task.to_dict())