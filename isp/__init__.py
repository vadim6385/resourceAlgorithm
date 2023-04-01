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
                user.bandwidth_allocation = max(user.demand, user.min_bandwidth)
            else:
                user.bandwidth_allocation = max(min(user.ideal_bandwidth, remaining_bandwidth), user.min_bandwidth)

            remaining_bandwidth -= user.bandwidth_allocation

        if remaining_bandwidth <= 0:
            return

        # If there are unsatisfied users, distribute remaining bandwidth between them
        while remaining_bandwidth > 0:
            unsatisfied_users = [user for user in users if user.demand > user.bandwidth_allocation]
            if not unsatisfied_users:
                break
            self.allocate_bandwidth(unsatisfied_users)


        # Redistribute remaining bandwidth between existing users
        sum_extra = 0
        while remaining_bandwidth > 0.01: # allow 0.01 mpbs tolerance to speed up the process
            for user in users:
                extra_allocation = user.weight * remaining_bandwidth
                sum_extra += extra_allocation
                user.bandwidth_allocation += extra_allocation
            remaining_bandwidth -= sum_extra

    def display_bandwidth_allocation(self):
        for user in self.users:
            print(user)
