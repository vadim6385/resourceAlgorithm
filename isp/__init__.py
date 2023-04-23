MIN_REMAINING_BANDWIDTH = 0.01 # allow 0.01 mpbs tolerance to speed up the process and avoid endless loops

class ISP:
    def __init__(self, users, total_bandwidth):
        """
        Initialize a new ISP object with the specified users and total bandwidth.

        :param users: list of User objects
        :param total_bandwidth: float
        """
        self.users = users
        self.total_bandwidth = total_bandwidth
        self.remaining_bandwidth = self.total_bandwidth

    def allocate_bandwidth(self, time_window, users=None):
        if users is None:
            users = self.users

        active_users = [user for user in users if user.start_time <= time_window <= user.end_time]

        if not active_users:
            print(f"No active users during time window: {time_window}")
            return

        # Normalize weights for active users
        weight_sum = sum(u.weight for u in active_users)
        for user in active_users:
            user.weight /= weight_sum

        # Calculate ideal bandwidth allocations for active users
        for user in active_users:
            user.ideal_bandwidth = min(user.weight * self.total_bandwidth, user.demand)

        # Sort users by descending ideal bandwidth
        active_users.sort(key=lambda u: u.ideal_bandwidth, reverse=True)

        for user in active_users:
            if user.demand <= user.ideal_bandwidth:
                user.bandwidth_allocation = max(user.demand, user.min_bandwidth)
            else:
                user.bandwidth_allocation = max(min(user.ideal_bandwidth, self.remaining_bandwidth), user.min_bandwidth)

            self.remaining_bandwidth -= user.bandwidth_allocation

        if self.remaining_bandwidth <= MIN_REMAINING_BANDWIDTH:
            return

        # check if all users got their demand, if yes, quit:
        if self.check_demand_satisfied(active_users):
            return

        # If there are unsatisfied users, distribute remaining bandwidth between them
        while self.remaining_bandwidth > MIN_REMAINING_BANDWIDTH:
            unsatisfied_users = [user for user in active_users if user.demand > user.bandwidth_allocation]
            if not unsatisfied_users:
                break
            self.allocate_bandwidth(time_window=time_window, users=unsatisfied_users)

        # Redistribute remaining bandwidth between existing users
        sum_extra = 0
        while self.remaining_bandwidth > MIN_REMAINING_BANDWIDTH:
            if self.check_demand_satisfied(active_users):
                break
            for user in active_users:
                if user.bandwidth_allocation >= user.demand:
                    continue
                extra_allocation = user.weight * self.remaining_bandwidth
                sum_extra += extra_allocation
                user.bandwidth_allocation += extra_allocation
            self.remaining_bandwidth -= sum_extra

    def display_bandwidth_allocation(self):
        for user in self.users:
            print(user)

    def check_demand_satisfied(self, users):
        for user in users:
            if user.demand > user.bandwidth_allocation:
                return False
        return True