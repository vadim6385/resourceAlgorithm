# algorithms.py

# Simple Greedy Algorithm
def simple_greedy(tasks):
    tasks.sort(key=lambda x: x['arrival_time'])
    return tasks

# Greedy Algorithm with Compression
def greedy_with_compression(tasks):
    tasks.sort(key=lambda x: x['arrival_time'])
    # Compression logic here
    return tasks

# Preemptive Scheduling Algorithm
def preemptive_scheduling(tasks):
    tasks.sort(key=lambda x: x['priority'])
    # Preemption logic here
    return tasks
