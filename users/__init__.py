from enum import IntEnum


class UserType(IntEnum):
    REGULAR = 1
    PREMIUM = 2
    ENTERPRISE = 4


class User:
    def __init__(self, user_type, demand, start_time, end_time, min_bandwidth=0):
        """
        Initialize a new User object with the specified type, demand, start time, end time, and minimum bandwidth.

        :param user_type: UserType
        :param demand: float
        :param start_time: int
        :param end_time: int
        :param min_bandwidth: float
        """
        self.user_type = user_type
        self.demand = demand
        self.weight = int(user_type)
        self.start_time = start_time
        self.end_time = end_time
        self.min_bandwidth = min_bandwidth if user_type == UserType.ENTERPRISE and min_bandwidth != 0 else 0
        self.bandwidth_allocation = 0

    def __str__(self):
        """
        Return a string representation of the User object.

        :return: str
        """
        return "User: type={0}, demand={1}, weight={2}, " \
               "allocated bandwidth={3}".format(str(self.user_type), str(self.demand),
                                                str(self.weight), str(self.bandwidth_allocation))
