#!/usr/bin/env python3 

import csv 
import time

# Function to parse the CNF file
def parse_cnf_file(filename):
    all_clauses = []
    current_clauses = []
    num_vars = None
    num_clauses = None

    with open(filename, 'r') as f:
        for line in f:
            line = line.strip()
            if line.startswith('p cnf'):
                parts = line.split()
                num_vars = int(parts[2])
                num_clauses = int(parts[3])
            elif line.startswith('c'):
                if current_clauses:
                    all_clauses.append((num_vars, num_clauses, current_clauses))
                    current_clauses = []  # Reset for next wff
            elif line:
                clause = [int(x) for x in line.split(',') if x.strip() != '0']
                current_clauses.append(clause)
        
        # Append the last wff if it exists
        if current_clauses:
            all_clauses.append((num_vars, num_clauses, current_clauses))

    return all_clauses

# DPLL algorithm function
def dpll(clauses, assignment):
    if not clauses:
        return True, assignment
    for clause in clauses:
        if not clause:
            return False, assignment
    variable = abs(clauses[0][0])
    new_clauses = [clause for clause in clauses if variable not in clause]
    new_clauses = [[lit for lit in clause if lit != -variable] for clause in new_clauses]
    satisfiable, new_assignment = dpll(new_clauses, assignment + [variable])
    if satisfiable:
        return True, new_assignment
    new_clauses = [clause for clause in clauses if -variable not in clause]
    new_clauses = [[lit for lit in clause if lit != variable] for clause in new_clauses]
    return dpll(new_clauses, assignment + [-variable])

# Timing function
def run_dpll_and_time(wff):
    num_vars, num_clauses, clauses = wff
    start_time = time.time()
    satisfiable, assignment = dpll(clauses, [])
    elapsed_time = time.time() - start_time
    return elapsed_time, satisfiable, num_vars

# Save results to CSV function
def save_results_to_csv(results, output_file):
    with open(output_file, mode='w', newline='') as csvfile:
        fieldnames = ['Filename', 'Execution Time (s)', 'Number of Variables', 'Satisfiability']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for filename, elapsed_time, num_vars, satisfiable in results:
            writer.writerow({
                'Filename': filename,
                'Execution Time (s)': elapsed_time,
                'Number of Variables': num_vars,
                'Satisfiability': 'S' if satisfiable else 'U'
            })

# Main execution
if __name__ == '__main__':
    cnf_file = 'data_kSAT_hberens.cnf'  # Specify your CNF file here
    output_file = 'output_hberens.csv'  # Specify the output CSV file

    # Parse CNF file for all wffs
    all_wffs = parse_cnf_file(cnf_file)

    # Store results for each wff
    results = []

    for index, wff in enumerate(all_wffs):
        elapsed_time, satisfiable, num_vars = run_dpll_and_time(wff)
        results.append((cnf_file, elapsed_time, num_vars, satisfiable))

    # Save results to CSV
    save_results_to_csv(results, output_file)
