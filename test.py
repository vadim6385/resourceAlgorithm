from isp import ISP
from user import UserType, User

# Create some User objects
user1 = User(UserType.REGULAR, 2, demand=1)
user2 = User(UserType.PREMIUM, 10, demand=2)
user3 = User(UserType.ENTERPRISE, 50, min_bandwidth=10, demand=10)
user4 = User(UserType.REGULAR, 5, demand=5)

# Create an ISP object and add the users to it
isp = ISP(100, [user1, user2, user3, user4])

# Allocate bandwidth to the users
isp.allocate_bandwidth()

# Print the allocated bandwidth for each user
for user in isp.users:
    print(user)