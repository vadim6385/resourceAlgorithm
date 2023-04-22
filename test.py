from isp import ISP
from users import UserType, User


def main():
    total_bandwidth = 1000  # in Mbps

    users = [
        User(UserType.REGULAR, demand=100, start_time=0, end_time=10),
        User(UserType.PREMIUM, demand=250, start_time=5, end_time=15),
        User(UserType.ENTERPRISE, demand=500, min_bandwidth=50, start_time=10, end_time=20),
        User(UserType.REGULAR, demand=400, start_time=0, end_time=10),
        User(UserType.PREMIUM, demand=300, start_time=5, end_time=15),
        User(UserType.ENTERPRISE, demand=700, min_bandwidth=50, start_time=10, end_time=20),
        User(UserType.REGULAR, demand=50, start_time=0, end_time=10),
        User(UserType.PREMIUM, demand=300, start_time=5, end_time=15),
        User(UserType.ENTERPRISE, demand=900, min_bandwidth=50, start_time=10, end_time=20),
    ]

    isp = ISP(users, total_bandwidth)

    for time_window in range(0, 25, 5):
        print(f"Time window: {time_window}")
        isp.allocate_bandwidth(time_window)
        isp.display_bandwidth_allocation()
        print("\n")

if __name__ == "__main__":
    main()

