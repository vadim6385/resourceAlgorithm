import numpy as np
import seaborn as sns
from matplotlib import pylab as plt


def find_rectangles_center(data):
    rectangles = {}
    visited = np.zeros_like(data, dtype=bool)

    for y in range(data.shape[0]):
        for x in range(data.shape[1]):
            if not visited[y, x]:
                value = data[y, x]
                y_min, y_max, x_min, x_max = y, y, x, x

                # Expand the rectangle horizontally
                for x2 in range(x + 1, data.shape[1]):
                    if data[y, x2] == value and not visited[y, x2]:
                        x_max = x2
                        visited[y, x2] = True
                    else:
                        break

                # Expand the rectangle vertically
                for y2 in range(y + 1, data.shape[0]):
                    if (data[y2, x:x_max + 1] == value).all() and not visited[y2, x:x_max + 1].any():
                        y_max = y2
                        visited[y2, x:x_max + 1] = True
                    else:
                        break

                rectangles[value] = ((y_min + y_max) / 2, (x_min + x_max) / 2)
                visited[y:y_max + 1, x:x_max + 1] = True

    return rectangles


def show_plot(task_matrix, dropped_tasks):
    fig, ax = plt.subplots()
    heatmap = sns.heatmap(task_matrix, cmap='Greens', ax=ax)
    plt.title("Task allocation graph, dropped tasks: {}".format(dropped_tasks), fontsize=20)
    plt.xlabel("t(sec)")
    plt.ylabel("Bandwidth(Mbps)")

    centers = find_rectangles_center(task_matrix)

    # Define the color and font size ranges
    min_value, max_value = task_matrix.min(), task_matrix.max()
    min_font_size, max_font_size = 10, 20
    color_map = plt.cm.get_cmap('Greys')

    for value, (y_center, x_center) in centers.items():
        # Normalize the value to a range between 0 and 1
        normalized_value = (value - min_value) / (max_value - min_value)

        # Calculate font size based on normalized value
        font_size = min_font_size + normalized_value * (max_font_size - min_font_size)

        # Calculate text color based on the value
        text_color = color_map(1 - normalized_value)

        heatmap.text(x_center + 0.5, y_center + 0.5, value, horizontalalignment='center', verticalalignment='center', color=text_color, fontsize=font_size, fontweight='bold')

    plt.show()

