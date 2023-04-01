class ISP:
    def __init__(self, users, total_bandwidth):
        """
        Initialize a new ISP object with the specified users and total bandwidth.

        :param users: list of User objects
        :param total_bandwidth: float
        """
        self.users = users
        self.total_bandwidth = total_bandwidth

    def allocate_bandwidth(self, users=None):
        if users is None:
            users = self.users

        # Normalize weights
        weight_sum = sum(u.weight for u in users)
        for user in users:
            user.weight /= weight_sum

        # Calculate ideal bandwidth allocations
        for user in users:
            user.ideal_bandwidth = user.weight * self.total_bandwidth

        # Sort users by descending ideal bandwidth
        users.sort(key=lambda u: u.ideal_bandwidth, reverse=True)

        remaining_bandwidth = self.total_bandwidth

        for user in users:
            if user.demand <= user.ideal_bandwidth:
                user.bandwidth_allocation = user.demand
            else:
                user.bandwidth_allocation = min(user.ideal_bandwidth, remaining_bandwidth)

            remaining_bandwidth -= user.bandwidth_allocation

        # Redistribute remaining bandwidth if any
        if remaining_bandwidth > 0:
            unsatisfied_users = [user for user in users if user.demand > user.bandwidth_allocation]
            if not unsatisfied_users:
                return
            self.allocate_bandwidth(unsatisfied_users)

    def display_bandwidth_allocation(self):
        for user in self.users:
            print(user)
