# algorithm_tester.py

import matplotlib.pyplot as plt
import importlib.util

# Import algorithms from algorithms.py
spec = importlib.util.spec_from_file_location("algorithms", "./algorithms.py")
algorithms = importlib.util.module_from_spec(spec)
spec.loader.exec_module(algorithms)

# Test data
tasks = [
    {'id': 1, 'arrival_time': 1, 'priority': 3},
    {'id': 2, 'arrival_time': 4, 'priority': 1},
    {'id': 3, 'arrival_time': 2, 'priority': 4},
]


# Run tests
def run_tests():
    for algo in [algorithms.simple_greedy, algorithms.greedy_with_compression, algorithms.preemptive_scheduling]:
        result = algo(tasks)
        display_results(result, algo.__name__)


# Display results
def display_results(result, algo_name):
    print(f"Results for {algo_name}:")
    print(result)

    # Display graph (for demonstration, using arrival_time)
    arrival_times = [task['arrival_time'] for task in result]
    plt.plot(arrival_times, label=algo_name)
    plt.legend()
    plt.show()


if __name__ == "__main__":
    run_tests()
