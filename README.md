# Final Project - resource distribution algorithm

Resource allocation is the process of distributing available resources among various entities, such as bandwidth or computational resources, to optimize the overall performance of an Internet Service Provider (ISP). An ISP must allocate resources to its customers while maintaining fairness, minimizing latency, and ensuring efficient resource utilization.

Here, we will formalize a resource allocation algorithm for an ISP that manages bandwidth distribution among its customers.

### Problem Definition:
Let N be the number of customers, and B be the total bandwidth available. Each customer i has a demand for bandwidth, represented as D_i. The goal is to allocate bandwidth A_i to each customer i such that the following conditions are met:

1) A_i >= 0 for all i (bandwidth allocation must be non-negative).
2) The total allocated bandwidth should not exceed the available bandwidth: Σ A_i <= B.
3) Fairness: Bandwidth should be allocated fairly among the customers.
4) Efficiency: The algorithm should minimize the overall latency and maximize resource utilization.

### Algorithm:

1) Define the Task class

    1.1 Initialize Task object with bandwidth, start_time, duration, and priority

    1.2 Implement getter and setter methods for the task attributes

2) Main algorithm loop 

   2.1 While True (or until a stopping condition is met)
 
   2.1.1 Generate tasks with random attributes

   2.1.2 Add generated tasks to the task queue

   2.1.3 Sort the task queue based on priority and start_time

   2.1.4 Initialize available bandwidth with the total bandwidth capacity

   2.1.5 Create an empty separate queue

   2.1.6 While the task queue is not empty

   2.1.6.1 Pop a task from the task queue

   2.1.6.2 Check if the task can be executed (its bandwidth requirement is smaller or equal to the available bandwidth)

   2.1.6.2.1 If yes, execute the task and reduce the available bandwidth

   2.1.6.2.2 If no, add the task to the separate queue

   2.1.7 Merge the separate queue back into the task queue

   2.1.8 Increment the time unit
