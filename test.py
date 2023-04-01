from isp import ISP
from user import UserType, User


def main():
    total_bandwidth = 1000  # in Mbps

    users = [
        User(UserType.REGULAR, demand=100),
        User(UserType.PREMIUM, demand=250),
        User(UserType.ENTERPRISE, demand=500, min_bandwidth=50),
    ]

    isp = ISP(users, total_bandwidth)
    isp.allocate_bandwidth()
    isp.display_bandwidth_allocation()


if __name__ == "__main__":
    main()

