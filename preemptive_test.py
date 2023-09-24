import heapq
from typing import List


class Item:
    def __init__(self, priority, time_created, time_start, duration, weight):
        self.priority = priority
        self.time_created = time_created
        self.time_start = time_start
        self.duration = duration
        self.weight = weight

    def __lt__(self, other):
        if self.priority == other.priority:
            return self.time_created < other.time_created
        return self.priority < other.priority


def execute_tasks(task_list: List[Item], max_weight: int) -> List[Item]:
    pq = []
    for task in task_list:
        heapq.heappush(pq, task)
    task_stack = []
    container = []
    completed_tasks = []
    current_weight = 0
    time = 1

    while time < 10 or pq or task_stack:
        # Update container and move completed tasks to completedTasks list
        i = len(container) - 1
        while i >= 0:
            task = container[i]
            if task.time_start + task.duration == time:
                current_weight -= task.weight
                completed_tasks.append(task)
                container.pop(i)
            i -= 1

        # Preempt tasks from priority queue
        while pq:
            task = heapq.heappop(pq)
            if task.weight <= max_weight - current_weight:
                task.time_start = time
                container.append(task)
                current_weight += task.weight
            else:
                task_stack.append(task)

        # Execute tasks from stack
        while task_stack:
            task = task_stack.pop()
            if task.weight <= max_weight - current_weight:
                task.time_start = time
                container.append(task)
                current_weight += task.weight
            else:
                break

        time += 1

    return completed_tasks


# Main function to test the code
def main():
    # Initialize a list of tasks (this could be generated randomly)
    tasks = [
        Item(1, 0, 0, 2, 10),
        Item(2, 1, 0, 1, 5),
        Item(3, 2, 0, 4, 15),
        # Add more tasks here
    ]

    completed_tasks = execute_tasks(tasks, 50)

    # Print out the completed tasks
    for task in completed_tasks:
        print(f"Priority: {task.priority}, Time Created: {task.time_created}, "
              f"Time Start: {task.time_start}, Duration: {task.duration}, Weight: {task.weight}")


# Run the main function
if __name__ == '__main__':
    main()
