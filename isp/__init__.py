
class ISP:
    def __init__(self, total_bandwidth, users):
        """
        Initialize a new ISP object with the specified total bandwidth and list of User objects.

        :param total_bandwidth: float
        :param users: list of User objects
        """
        self.total_bandwidth = total_bandwidth
        self.users = users

    def allocate_bandwidth(self):
        """
        Allocate bandwidth to all users based on their demand and the total demand from all users.
        If the total allocated bandwidth exceeds the total available bandwidth, reduce the allocation for each user
        by the same factor to meet the total bandwidth limit.
        """
        for user in self.users:
            user.allocate_bandwidth(self.total_bandwidth, self.users)

        allocated_bandwidth = sum(user.bandwidth_allocation for user in self.users)

