from isp import ISP
from user import UserType, User


def main():
    total_bandwidth = 1000  # in Mbps

    users = [
        User(UserType.REGULAR, demand=100, weight=1),
        User(UserType.PREMIUM, demand=250, weight=2),
        User(UserType.ENTERPRISE, demand=500, weight=4),
    ]

    isp = ISP(users, total_bandwidth)
    isp.allocate_bandwidth()
    isp.display_bandwidth_allocation()


if __name__ == "__main__":
    main()
