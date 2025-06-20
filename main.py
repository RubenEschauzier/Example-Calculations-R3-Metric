import json

import numpy as np
from typing import List, Dict
import matplotlib
import matplotlib.pyplot as plt


def plot_answer_distribution(lin_space, answer_dist):
    plt.figure(figsize=(10, 4))

    # Use a thin line and remove large dots
    plt.plot(lin_space, answer_dist, linewidth=1.2, color='black')

    # Add light grid
    plt.grid(True, linestyle='--', alpha=0.5)

    # Add axis labels and title with a clean style
    plt.xlabel('Time', fontsize=11)
    plt.ylabel('Cumulative Results', fontsize=11)
    plt.title('Query Relevant Documents For Results Found in Time', fontsize=13)

    # Clean up tick label size
    plt.tick_params(axis='both', which='major', labelsize=9)

    # Make layout tight
    plt.tight_layout()
    plt.show()


def plot_answer_distribution_with_integral(lin_space, answer_dist, fig_location):
    plt.figure(figsize=(10, 4))

    # Plot the answer distribution in black
    plt.plot(lin_space, answer_dist, color='black', linewidth=1.5)

    # Add Riemann sum rectangles in gray
    for i in range(len(lin_space) - 1):
        x_left = lin_space[i]
        width = lin_space[i+1] - lin_space[i]
        height = answer_dist[i]
        plt.gca().add_patch(plt.Rectangle(
            (x_left, 0), width, height,
            facecolor='gray', alpha=0.4, edgecolor='none'
        ))

    # Compute integral with trapezoidal rule for reference
    integral = np.trapezoid(answer_dist, lin_space)
    plt.title('Distribution Function for Results with All Documents Found in Time', fontsize=15)
    # plt.title(f'Answer Distribution with Riemann Sum (∫ ≈ {integral:.2f})', fontsize=12)

    # Axis labels and styling
    plt.xlabel('Time (s)', fontsize=12)
    plt.ylabel('Cumulative # of Results \n with All Documents Found', fontsize=12)
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.tight_layout()
    plt.legend()
    plt.savefig(fig_location)

    return integral


if __name__ == "__main__":
    with open('data/answer_dist_bad_2.json') as f_bad:
        data_bad = json.load(f_bad)
    with open('data/answer_dist_optimal_2.json') as f_optimal:
        data_optimal = json.load(f_optimal)

    plot_answer_distribution(data_bad['linSpace'], data_bad['answerDist'])
    plot_answer_distribution(data_optimal['linSpace'], data_optimal['answerDist'])
    cont_r3_bad = plot_answer_distribution_with_integral(data_bad['linSpace'], data_bad['answerDist'],
                                                         "bad_answer_dist.pdf")
    cont_r3_optimal = plot_answer_distribution_with_integral(data_optimal['linSpace'], data_optimal['answerDist'],
                                                             "optimal_answer_dist.pdf")

    print("Continuous R3 for optimal traversal order {}".format(cont_r3_optimal))
    print("Continuous R3 for bad traversal order {}".format(cont_r3_bad))
