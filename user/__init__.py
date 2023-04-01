from enum import Enum


class UserType(Enum):
    REGULAR = 0
    PREMIUM = 1
    ENTERPRISE = 2


class User:
    def __init__(self, user_type, demand, weight):
        """
        Initialize a new User object with the specified type, demand, and weight.

        :param user_type: UserType
        :param demand: float
        :param weight: float
        """
        self.user_type = user_type
        self.demand = demand
        self.weight = weight
        self.bandwidth_allocation = 0

    def __str__(self):
        """
        Return a string representation of the User object.

        :return: str
        """
        return f"User: type={self.user_type}, demand={self.demand}, weight={self.weight}, allocated bandwidth={self.bandwidth_allocation}"

