from isp import ISP
from user import UserType, User

# Create some User objects
user1 = User(UserType.REGULAR, 2, demand=1)
user2 = User(UserType.PREMIUM, 10, demand=2)
user3 = User(UserType.ENTERPRISE, 20, demand=3)

# Create an ISP object and add the users to it
isp = ISP(30, [user1, user2, user3])

# Allocate bandwidth to the users
isp.allocate_bandwidth()

# Print the allocated bandwidth for each user
for user in isp.users:
    print(user)