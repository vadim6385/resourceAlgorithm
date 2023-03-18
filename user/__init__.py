from enum import Enum


class UserType(Enum):
    REGULAR = 0
    PREMIUM = 1
    ENTERPRISE = 2


class User:
    def __init__(self, user_type: UserType, max_bandwidth: int, demand: int = 1, min_bandwidth: int = 0) -> None:
        """
        Initialize a User object with the given user type, maximum bandwidth, demand, and minimum bandwidth.

        Args:
            user_type (UserType): The type of the user (regular, premium, or enterprise).
            max_bandwidth (int): The maximum bandwidth that the user is eligible to receive.
            demand (int, optional): The user's demand for bandwidth. Defaults to 1.
            min_bandwidth (int, optional): The minimum bandwidth that the user must be allocated. Defaults to 0.
        """
        self.__user_type = user_type
        self.__max_bandwidth = max_bandwidth
        self.__demand = demand
        self.__min_bandwidth = min_bandwidth
        self.__allocated_bandwidth = 0

    def __str__(self) -> str:
        """
        Returns a string representation of the User object.

        Returns:
            str: A string representation of the User object.
        """
        return f"User: Type={self.__user_type}, Demand={self.__demand}, Max Bandwidth={self.__max_bandwidth}, Allocated Bandwidth={self.__allocated_bandwidth}"

    @property
    def user_type(self) -> UserType:
        """
        Returns the user's type.

        Returns:
            UserType: The user's type.
        """
        return self.__user_type

    @property
    def max_bandwidth(self) -> int:
        """
        Returns the user's maximum bandwidth.

        Returns:
            int: The user's maximum bandwidth.
        """
        return self.__max_bandwidth

    @property
    def demand(self) -> int:
        """
        Returns the user's demand for bandwidth.

        Returns:
            int: The user's demand for bandwidth.
        """
        return self.__demand

    @property
    def min_bandwidth(self) -> int:
        """
        Returns the user's minimum bandwidth.

        Returns:
            int: The user's minimum bandwidth.
        """
        return self.__min_bandwidth

    @property
    def allocated_bandwidth(self) -> int:
        """
        Returns the user's allocated bandwidth.

        Returns:
            int: The user's allocated bandwidth.
        """
        return self.__allocated_bandwidth

    def set_allocated_bandwidth(self, bandwidth: int) -> None:
        """
        Sets the user's allocated bandwidth to the given value.

        If the user has a minimum bandwidth defined, this method ensures that they are not allocated less than that amount.

        Args:
            bandwidth (int): The bandwidth to allocate to the user.
        """
        if self.__min_bandwidth and bandwidth < self.__min_bandwidth:
            bandwidth = self.__min_bandwidth
        self.__allocated_bandwidth = bandwidth
