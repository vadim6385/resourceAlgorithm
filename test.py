# Create some users with different demands and priorities
from isp import ISP
from user import User, UserType

user1 = User(UserType.REGULAR, 10)
user2 = User(UserType.PREMIUM, 20)
user3 = User(UserType.ENTERPRISE, 30)

# Set minimum bandwidths for users 1 and 2
# user1.min_bandwidth = 2
# user2.min_bandwidth = 5

# Add the users to an ISP object
isp = ISP(100)
isp.add_user(user1)
isp.add_user(user2)
isp.add_user(user3)

# Allocate bandwidth to the users
isp.allocate_bandwidth()

# Print the allocated bandwidth for each user
print(f"User 1: Allocated Bandwidth={user1.allocated_bandwidth}")
print(f"User 2: Allocated Bandwidth={user2.allocated_bandwidth}")
print(f"User 3: Allocated Bandwidth={user3.allocated_bandwidth}")

# Allocate more bandwidth to the ISP and reallocate the bandwidth to the users
isp = ISP(150)
isp.add_user(user1)
isp.add_user(user2)
isp.add_user(user3)
isp.allocate_bandwidth()

# Print the allocated bandwidth for each user again
print(f"User 1: Allocated Bandwidth={user1.allocated_bandwidth}")
print(f"User 2: Allocated Bandwidth={user2.allocated_bandwidth}")
print(f"User 3: Allocated Bandwidth={user3.allocated_bandwidth}")
