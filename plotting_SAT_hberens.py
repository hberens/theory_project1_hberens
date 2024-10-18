#!/usr/bin/env python3 

import matplotlib.pyplot as plt
import csv
import numpy as np


# Plot results function
def plot_results(csv_file):

    num_vars_list = []
    elapsed_time_list = []
    satisfiable_list = []

    # Read the CSV file
    with open(csv_file, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            num_vars_list.append(int(row['Number of Variables']))
            elapsed_time_list.append(float(row['Execution Time (s)']))
            satisfiable_list.append('green' if row['Satisfiability'] == 'S' else 'red')

    # start plotting 
    plt.figure(figsize=(8, 7))
    for i in range(len(num_vars_list)):
        if satisfiable_list[i] == 'green':
            plt.scatter(num_vars_list[i], elapsed_time_list[i], c='green', label='Satisfiable' if 'Satisfiable' not in plt.gca().get_legend_handles_labels()[1] else "")
        else:
            plt.scatter(num_vars_list[i], elapsed_time_list[i], c='red', marker='x', label='Unsatisfiable' if 'Unsatisfiable' not in plt.gca().get_legend_handles_labels()[1] else "")

    # Fit an exponential curve to the UNSAT points using polyfit
    plt.xlabel('Number of Variables')
    plt.ylabel('Time (seconds)')
    plt.title('DPLL Algorithm Execution Time vs. Number of Variables')
    plt.legend(loc='upper center')
    
    plt.xticks(range(0, max(num_vars_list)+1, 2))
    plt.yticks([0, 0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5, 0.55, 0.6, 0.65, 0.7])
    plt.ylim(0, max(elapsed_time_list) * 1.1)
    
    plt.grid()
    plt.savefig('plots_hberens.png')


# Main execution
if __name__ == '__main__':
    csv_file = 'output_hberens.csv'  # Specify the CSV file with the results
    plot_results(csv_file)
