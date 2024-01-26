import numpy as np
import seaborn as sns
from matplotlib import pylab as plt


class TaskHeatmap:
    # Initialize the class with task_matrix, dropped_tasks_num, and dropped_tasks_ratio
    def __init__(self, task_matrix):
        self.task_matrix = task_matrix

    # Function to find the center of rectangles in the heatmap
    def find_rectangles_center(self):
        rectangles = {}  # Dictionary to store the center of rectangles
        visited = np.zeros_like(self.task_matrix, dtype=bool)  # Matrix to keep track of visited cells

        # Loop through each cell in the task_matrix
        for y in range(self.task_matrix.shape[0]):
            for x in range(self.task_matrix.shape[1]):
                # If the cell is not visited
                if not visited[y, x]:
                    value = self.task_matrix[y, x]
                    y_min, y_max, x_min, x_max = y, y, x, x

                    # Expand the rectangle horizontally
                    for x2 in range(x + 1, self.task_matrix.shape[1]):
                        if self.task_matrix[y, x2] == value and not visited[y, x2]:
                            x_max = x2
                            visited[y, x2] = True
                        else:
                            break

                    # Expand the rectangle vertically
                    for y2 in range(y + 1, self.task_matrix.shape[0]):
                        if (self.task_matrix[y2, x:x_max + 1] == value).all() and not visited[y2, x:x_max + 1].any():
                            y_max = y2
                            visited[y2, x:x_max + 1] = True
                        else:
                            break

                    # Store the center of the rectangle
                    rectangles[value] = ((y_min + y_max) / 2, (x_min + x_max) / 2)
                    visited[y:y_max + 1, x:x_max + 1] = True

        return rectangles

    # Function to display the heatmap
    def show_plot(self):
        fig, ax = plt.subplots()
        heatmap = sns.heatmap(self.task_matrix, cmap='Greens', ax=ax)
        plt.title("Task allocation graph",
                  fontsize=20)
        plt.xlabel("t(sec)")
        plt.ylabel("Bandwidth(Mbps)")

        centers = self.find_rectangles_center()  # Get the centers of rectangles

        # Define the color and font size ranges
        min_value, max_value = self.task_matrix.min(), self.task_matrix.max()
        min_font_size, max_font_size = 10, 20
        color_map = plt.cm.get_cmap('Greys')

        # Annotate each rectangle with its value
        for value, (y_center, x_center) in centers.items():
            # Normalize the value to a range between 0 and 1
            normalized_value = (value - min_value) / (max_value - min_value)

            # Calculate font size based on normalized value
            font_size = min_font_size + normalized_value * (max_font_size - min_font_size)

            # Calculate text color based on the value
            text_color = color_map(1 - normalized_value)

            # Add text annotation to the heatmap
            heatmap.text(x_center + 0.5, y_center + 0.5, value, horizontalalignment='center',
                         verticalalignment='center', color=text_color, fontsize=font_size, fontweight='bold')

        plt.show()  # Display the heatmap


# Example usage
if __name__ == "__main__":
    from algo_tester import algo_worker
    from algorithms import greedy_compression_algorithm, simple_greedy_algorithm, preemptive_scheduling_algorithm
    value_tuple = ("task_list_random.json", "Generated queue of random tasks")
    key = ""
    max_bandwidth = 50
    algo_worker(algo_fp=simple_greedy_algorithm, algo_name="", task_list_type="", value_tuple=value_tuple, max_bandwidth=max_bandwidth)


