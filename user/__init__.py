from enum import Enum


class UserType(Enum):
    REGULAR = 0
    PREMIUM = 1
    ENTERPRISE = 2


class User:
    def __init__(self, type, max_bandwidth, min_bandwidth=0.01, demand=0):
        """
        Initialize a new User object with the specified type, maximum bandwidth, minimum bandwidth, and demand.
        By default, the minimum bandwidth is set to 0.01 Mbps and the demand is set to 0.

        :param type: UserType
        :param max_bandwidth: float
        :param min_bandwidth: float
        :param demand: float
        """
        self.__type = type
        self.__min_bandwidth = min_bandwidth
        self.__max_bandwidth = max_bandwidth
        self.demand = demand
        self.bandwidth_allocation = 0

    @property
    def type(self) -> UserType:
        """
        Get the type of the User.

        :return: UserType
        """
        return self.__type

    @property
    def min_bandwidth(self) -> float:
        """
        Get the minimum bandwidth required by the User.

        :return: float
        """
        return self.__min_bandwidth

    @min_bandwidth.setter
    def min_bandwidth(self, val: float) -> None:
        """
        Set the minimum bandwidth required by the User.

        :param val: float
        """
        self.__min_bandwidth = val

    @property
    def max_bandwidth(self) -> int:
        """
        Get the maximum bandwidth that can be allocated to the User.

        :return: int
        """
        return self.__max_bandwidth

    def allocate_bandwidth(self, available_bandwidth, users):
        """
        Allocate bandwidth to the user based on their demand and the total demand from all users.

        :param available_bandwidth: float
        :param users: list of User objects
        """
        if self.demand == 0:
            self.bandwidth_allocation = 0
        else:
            demand_sum = sum(u.demand for u in users)
            if demand_sum == 0:
                self.bandwidth_allocation = self.__min_bandwidth
            else:
                allocated_bandwidth = available_bandwidth * (self.demand / demand_sum)
                self.bandwidth_allocation = max(min(allocated_bandwidth, self.__max_bandwidth), self.__min_bandwidth)

    def __str__(self):
        """
        Return a string representation of the User object.

        :return: str
        """
        return f"User: type={self.__type}, min bandwidth={self.__min_bandwidth}, max bandwidth={self.__max_bandwidth}, demand={self.demand}, allocated bandwidth={self.bandwidth_allocation}"


