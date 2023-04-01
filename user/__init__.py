from enum import IntEnum


class UserType(IntEnum):
    REGULAR = 1
    PREMIUM = 2
    ENTERPRISE = 4


class User:
    def __init__(self, user_type, demand, min_bandwidth=None):
        """
        Initialize a new User object with the specified type, demand, and minimum bandwidth.

        :param user_type: UserType
        :param demand: float
        :param min_bandwidth: float
        """
        self.user_type = user_type
        self.demand = demand
        self.weight = int(self.user_type)
        self.min_bandwidth = min_bandwidth if user_type == UserType.ENTERPRISE and min_bandwidth is not None else 0
        self.bandwidth_allocation = 0

    def __str__(self):
        """
        Return a string representation of the User object.

        :return: str
        """
        return f"User: type={self.user_type}, demand={self.demand}, weight={self.weight}, allocated bandwidth={self.bandwidth_allocation}"
