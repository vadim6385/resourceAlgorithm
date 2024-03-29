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
        self.__actual_start_time = created_time
        self.__total_duration = duration
        self.__remaining_duration = duration
        self.priority = priority
        self.__score = 0
        self.__actual_end_time = self.__actual_start_time + self.__total_duration
        self.__duration_changed = False
        self.__preempted_time = self.__actual_start_time
        self.__task_status = TaskStatus.PENDING
        self.__is_preempted = False
        self.__end_time_changed = False

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
        return self.__actual_start_time

    # preempted time
    @property
    def preempted_time(self):
        return self.__preempted_time

    # set preempted time
    @preempted_time.setter
    def preempted_time(self, val):
        self.__preempted_time = val

    @actual_start_time.setter
    def actual_start_time(self, val):
        self.__actual_start_time = val
        self.__preempted_time = self.__actual_start_time

    # Get duration of the task
    @property
    def total_duration(self):
        return self.__total_duration

    # Get remaining duration of the task
    @property
    def remaining_duration(self):
        return self.__remaining_duration

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
            return self.__actual_start_time + self.__total_duration
        return self.__actual_end_time

    # set actual end time
    @actual_end_time.setter
    def actual_end_time(self, val):
        self.__end_time_changed = True
        self.__actual_end_time = val

    # compress the task to minimal bandwidth
    def compress(self):
        self.__bandwidth = self.__min_bandwidth

    # decompress bandwidth
    def decompress(self):
        self.__bandwidth = self.__original_bandwidth

    def preempt(self, current_time):
        self.__is_preempted = True
        self.__preempted_time = current_time + 1
        self.__task_status = TaskStatus.PENDING

    # String representation of the Task object
    def __repr__(self):
        return (
            f"Task("
            f"id={self.id}, "
            f"bandwidth={self.bandwidth}, "
            f"min_bandwidth={self.min_bandwidth}, "
            f"original_bandwidth={self.original_bandwidth}, "
            f"created_time={self.created_time}, "
            f"actual_start_time={self.actual_start_time}, "
            f"total_duration={self.total_duration}, "
            f"remaining_duration={self.remaining_duration}, "
            f"actual_end_time={self.actual_end_time}, "
            f"priority={self.priority.name}, "
            f"status={self.status.name}, "
            f"preempted_time={self.preempted_time}, "
            f"score={self.score}, "
            f"is_compressed={self.is_compressed}, "
            f"bandwidth_diff={self.bandwidth_diff}"
            f")"
        )

    def to_dict(self):
        return {
            'id': self.__id,
            'bandwidth': self.__bandwidth,
            'min_bandwidth': self.__min_bandwidth,
            'original_bandwidth': self.__original_bandwidth,
            'created_time': self.__created_time,
            'actual_start_time': self.__actual_start_time,
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
        self.__actual_start_time = src_dict['actual_start_time']
        self.__preempted_time = src_dict['actual_start_time']
        self.__total_duration = self.__remaining_duration = src_dict['duration']
        self.priority = src_dict['priority']
        self.__actual_end_time = self.__actual_start_time + self.__total_duration
