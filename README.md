# Final Project - resource distribution algorithm

Resource allocation is the process of distributing available resources among various entities, such as bandwidth or computational resources, to optimize the overall performance of an Internet Service Provider (ISP). An ISP must allocate resources to its customers while maintaining fairness, minimizing latency, and ensuring efficient resource utilization.

Here, we will implement a resource allocation algorithm for an ISP that manages bandwidth distribution among its customers.

### Problem Definition:
Let N be the number of customers, and B be the total bandwidth available. Each customer i has a demand for bandwidth, represented as D_i. The goal is to allocate bandwidth A_i to each customer i such that the following conditions are met:

1) A_i >= 0 for all i (bandwidth allocation must be non-negative).
2) The total allocated bandwidth should not exceed the available bandwidth: Σ A_i <= B.
3) Fairness: Bandwidth should be allocated fairly among the customers.
4) Efficiency: The algorithm should minimize the overall latency and maximize resource utilization.

