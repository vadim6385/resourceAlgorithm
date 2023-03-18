from typing import List
from user import User

class ISP:
    def __init__(self, bandwidth: int) -> None:
        """
        Initialize an ISP object with the given total bandwidth.

        Args:
            bandwidth (int): The total bandwidth available to the ISP.
        """
        self.__bandwidth = bandwidth
        self.__users = []

    def __str__(self) -> str:
        """
        Returns a string representation of the ISP object.

        Returns:
            str: A string representation of the ISP object.
        """
        user_list = "\n".join([f"\t{user}" for user in self.__users])
        return f"ISP: Total Bandwidth={self.__bandwidth}\nUsers:\n{user_list}"

    def add_user(self, user: User) -> None:
        """
        Adds a user to the ISP's list of users.

        Args:
            user (User): The user to add to the ISP's list of users.
        """
        self.__users.append(user)

    def allocate_bandwidth(self) -> None:
        """
        Allocates bandwidth to each user in the ISP's list of users based on user priority and demand.
        """
        # Sort users based on user type, with enterprise users getting top priority
        # and regular users getting the lowest priority
        self.__users.sort(key=lambda x: x.user_type.value)

        total_demand = sum([user.demand for user in self.__users])
        total_allocated_bandwidth = 0

        for user in self.__users:
            # Calculate the user's allocated bandwidth based on their demand and the total demand
            allocated_bandwidth = int((user.demand / total_demand) * self.__bandwidth)

            # If the allocated bandwidth is less than the user's minimum bandwidth, allocate the minimum instead
            if user.min_bandwidth and allocated_bandwidth < user.min_bandwidth:
                allocated_bandwidth = user.min_bandwidth

            # If the allocated bandwidth exceeds the user's maximum bandwidth, allocate the maximum instead
            if allocated_bandwidth > user.max_bandwidth:
                allocated_bandwidth = user.max_bandwidth

            # Set the user's allocated bandwidth to the calculated value and update the total allocated bandwidth
            user.set_allocated_bandwidth(allocated_bandwidth)
            total_allocated_bandwidth += allocated_bandwidth

        # If the total allocated bandwidth exceeds the ISP's total bandwidth, adjust the allocation to ensure that
        # the total allocated bandwidth does not exceed the total bandwidth
        if total_allocated_bandwidth > self.__bandwidth:
            adjustment_factor = self.__bandwidth / total_allocated_bandwidth
            for user in self.__users:
                allocated_bandwidth = int(user.allocated_bandwidth * adjustment_factor)
                user.set_allocated_bandwidth(allocated_bandwidth)

    def get_users(self) -> List[User]:
        return self.__users