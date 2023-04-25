MIN_REMAINING_BANDWIDTH = 0.01  # allow 0.01 Mbps tolerance to speed up the process and avoid endless loops


class ISP:
    def __init__(self, users, total_bandwidth):
        self.users = users
        self.total_bandwidth = total_bandwidth

    def allocate_bandwidth(self, time_window, users=None, remaining_bandwidth=-1):
        if users is None:
            users = self.users

        active_users = [user for user in users if user.start_time <= time_window <= user.end_time]

        if not active_users:
            print(f"No active users during time window: {time_window}")
            return

        # Sort users by descending UserType and demand
        active_users.sort(key=lambda u: (int(u.user_type), u.demand), reverse=True)

        remaining_bandwidth = self.total_bandwidth if remaining_bandwidth == -1 else remaining_bandwidth
        min_bandwidth_sum = sum(u.min_bandwidth for u in active_users)

        if min_bandwidth_sum >= remaining_bandwidth:
            for user in active_users:
                user.bandwidth_allocation = user.min_bandwidth
            return

        for user in active_users:
            ideal_bandwidth = remaining_bandwidth * user.demand / sum(u.demand for u in active_users)
            user.bandwidth_allocation += max(min(ideal_bandwidth, user.demand), user.min_bandwidth)
            remaining_bandwidth -= user.bandwidth_allocation

        # check if all users got their demand, if yes, quit:
        if self.check_demand_satisfied(active_users):
            return

        if remaining_bandwidth <= MIN_REMAINING_BANDWIDTH:
            return

        unsatisfied_users = [user for user in active_users if user.demand > user.bandwidth_allocation]
        if unsatisfied_users:
            self.allocate_bandwidth(time_window, users=unsatisfied_users, remaining_bandwidth=remaining_bandwidth)

    def display_bandwidth_allocation(self):
        for user in self.users:
            print(user)

    def check_demand_satisfied(self, users):
        for user in users:
            if user.demand > user.bandwidth_allocation:
                return False
        return True