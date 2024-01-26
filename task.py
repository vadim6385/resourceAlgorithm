"""
The class represents a task with attributes for bandwidth, start time, duration, and priority.
It includes getter and setter methods to access and modify these attributes.
"""
from enum import IntEnum
from itertools import count


from utils import DEBUG_HALT


class TaskPriority(IntEnum):
    REGULAR = 1
    PREMIUM = 2
    ENTERPRISE = 3


class TaskStatus(IntEnum):
    PENDING = 0
    IN_PROGRESS = 1
    FINISHED = 2
    SUSPENDED = 3
    DROPPED = 4


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
        self.__total_duration = duration
        self.__remaining_duration = duration
        self.priority = priority
        self.__score = 0
        self.__duration_changed = False
        self.__task_status = TaskStatus.PENDING
        self.__is_preempted = False
        self.__end_time_changed = False
        self.__start_end_times_list = []

    # get task score
    @property
    def score(self) -> int:
        return self.__score

    # set task score
    def rate(self):
        self.__score = self.actual_start_time - self.created_time
        if self.__duration_changed:
            actual_duration = self.actual_end_time - self.actual_start_time
            self.__score += actual_duration - self.total_duration

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

    @property
    def bandwidth_diff(self):
        return self.__original_bandwidth - self.__bandwidth

    # Get created time of the task
    @property
    def created_time(self):
        return self.__created_time

    @property
    def actual_start_time(self):
        return self.__find_start_time(latest=False)

    @actual_start_time.setter
    def actual_start_time(self, val):
        self.__start_end_times_list.append([val,-1])

    def __find_start_time(self, latest=False):
        if self.__start_end_times_list == []:
            if self.status == TaskStatus.PENDING:
                return self.created_time
            raise Exception("Task never started")
        # start_times = [i[0] for i in self.__start_end_times_list]
        idx = -1 if latest else 0
        return self.__start_end_times_list[idx][0]

    # Get duration of the task
    @property
    def total_duration(self):
        return self.__total_duration

    # Get remaining duration of the task
    @property
    def remaining_duration(self):
        return self.__remaining_duration

    @property
    def start_end_times_list(self):
        return self.__start_end_times_list

    # Set remaining duration
    @remaining_duration.setter
    def remaining_duration(self, val):
        if val < 0:
            DEBUG_HALT()
        self.__duration_changed = True
        self.__remaining_duration = val

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

    # get task actual end time
    @property
    def actual_end_time(self):
        if not self.__end_time_changed:
            self.__start_end_times_list[-1][1] = self.actual_start_time + self.__total_duration
        return self.__start_end_times_list[-1][1]

    # set actual end time
    @actual_end_time.setter
    def actual_end_time(self, val):
        self.__end_time_changed = True
        self.__start_end_times_list[-1][1] = val

    # compress the task to minimal bandwidth
    def compress(self):
        self.__bandwidth = self.__min_bandwidth

    # decompress bandwidth
    def decompress(self):
        self.__bandwidth = self.__original_bandwidth

    def preempt(self, current_time):
        self.__is_preempted = True
        self.actual_end_time(current_time)
        self.__task_status = TaskStatus.PENDING

    def to_dict(self):
        return {
            'id': self.__id,
            'bandwidth': self.__bandwidth,
            'min_bandwidth': self.__min_bandwidth,
            'original_bandwidth': self.__original_bandwidth,
            'created_time': self.__created_time,
            'duration': self.__total_duration,
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
        self.__total_duration = self.__remaining_duration = src_dict['duration']
        self.priority = src_dict['priority']
