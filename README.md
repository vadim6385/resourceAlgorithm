# Final Project - resource distribution algorithm

Resource allocation is the process of distributing available resources among various entities, such as bandwidth or computational resources, to optimize the overall performance of an Internet Service Provider (ISP). An ISP must allocate resources to its customers while maintaining fairness, minimizing latency, and ensuring efficient resource utilization.

Here, we will formalize a resource allocation algorithm for an ISP that manages bandwidth distribution among its customers.

### Problem Definition:
Let N be the number of customers, and B be the total bandwidth available. Each customer i has a demand for bandwidth, represented as D_i. The goal is to allocate bandwidth A_i to each customer i such that the following conditions are met:

1) A_i >= 0 for all i (bandwidth allocation must be non-negative).
2) The total allocated bandwidth should not exceed the available bandwidth: Σ A_i <= B.
3) Fairness: Bandwidth should be allocated fairly among the customers.
4) Efficiency: The algorithm should minimize the overall latency and maximize resource utilization.

### Algorithm: box allocation in frames model

Initialize the ISP with a list of users and the total bandwidth available.
For each time window, allocate the bandwidth as follows:
2.1. Filter the users to get the active users in the given time window.
2.2. If there are no active users, print a message and return.
2.3. Sort the active users in descending order based on their UserType and demand.
2.4. Set the remaining bandwidth to the total bandwidth.
2.5. Calculate the sum of minimum bandwidths for all active users.
2.6. If the sum of minimum bandwidths is greater than or equal to the remaining bandwidth, allocate the minimum bandwidth to each user and return.
2.7. For each active user, do the following:
2.7.1. Calculate the ideal bandwidth for the user based on their demand and the remaining bandwidth.
2.7.2. Allocate the bandwidth to the user, ensuring it is between their minimum bandwidth and their demand.
2.7.3. Update the remaining bandwidth.
2.8. If the remaining bandwidth is less than or equal to the minimum remaining bandwidth tolerance, return.
2.9. Filter the active users to get the unsatisfied users.
2.10. If there are unsatisfied users, repeat the allocation process (steps 2.7-2.9) using only the unsatisfied users.
Display the final bandwidth allocation for each user.