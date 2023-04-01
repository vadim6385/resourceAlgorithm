# Final Project - resource distribution algorithm

Resource allocation is the process of distributing available resources among various entities, such as bandwidth or computational resources, to optimize the overall performance of an Internet Service Provider (ISP). An ISP must allocate resources to its customers while maintaining fairness, minimizing latency, and ensuring efficient resource utilization.

Here, we will formalize a resource allocation algorithm for an ISP that manages bandwidth distribution among its customers.

### Problem Definition:
Let N be the number of customers, and B be the total bandwidth available. Each customer i has a demand for bandwidth, represented as D_i. The goal is to allocate bandwidth A_i to each customer i such that the following conditions are met:

1) A_i >= 0 for all i (bandwidth allocation must be non-negative).
2) The total allocated bandwidth should not exceed the available bandwidth: Σ A_i <= B.
3) Fairness: Bandwidth should be allocated fairly among the customers.
4) Efficiency: The algorithm should minimize the overall latency and maximize resource utilization.

### Algorithm: Weighted Fair Sharing (WFS)

1) Assign each customer i a weight W_i based on their subscription plan or service level agreement (SLA). Higher weights represent higher priority or more expensive plans. Normalize the weights such that Σ W_i = 1.

2) Calculate the ideal bandwidth allocation for each customer i as follows:
I_i = W_i * B

3) Sort the customers in descending order based on their ideal bandwidth allocation I_i.

4) Initialize the remaining bandwidth R = B.

5) For each customer i in the sorted list, do the following:
a) If D_i <= I_i:
  - Allocate A_i = D_i.
  - Update R = R - A_i.
b) Else:
  - Allocate A_i = min(I_i, R).
  - Update R = R - A_i.
6) If there is remaining bandwidth (R > 0), redistribute it among the customers with unsatisfied demands by repeating steps 4-5.

The Weighted Fair Sharing (WFS) algorithm ensures fairness by considering each customer's weight in the allocation process. It also promotes efficiency by prioritizing customers with higher bandwidth demands and making sure that the available bandwidth is fully utilized. By adapting the weights, the ISP can offer different service levels or prioritize specific customers, ensuring flexibility and control over resource allocation.
