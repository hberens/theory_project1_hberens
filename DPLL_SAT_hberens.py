#!/usr/bin/env python3 

import csv 
import time

# Function to parse the CNF file
def parse_cnf_file(filename):
    # initialize lists 
    all_clauses = []
    current_clauses = []
    num_vars = None
    num_clauses = None

    # open up cnf file and go through lines 
    with open(filename, 'r') as f:
        for line in f:
            line = line.strip() 
            # check if the line is p cnf and split it 
            if line.startswith('p cnf'):
                parts = line.split()
                num_vars = int(parts[2])
                num_clauses = int(parts[3])
            # check for lines starting with c  and add the full current clause to the all clauses list
            elif line.startswith('c'):
                if current_clauses:
                    all_clauses.append((num_vars, num_clauses, current_clauses))
                    current_clauses = []  # Reset for next wff
            # otherwise split the line and get all the numbers as ints  
            elif line:
                clause = [int(x) for x in line.split(',') if x.strip() != '0']
                current_clauses.append(clause)
        
        # Append the last wff if it exists
        if current_clauses:
            all_clauses.append((num_vars, num_clauses, current_clauses))

    return all_clauses

# DPLL algorithm function
def dpll(clauses, assignment):
    # Base case: If there are no clauses left, the formula is satisfied
    # with the current assignment, return True and the assignment.
    if not clauses:
        return True, assignment
    
    # Base case 2: If any clause is empty, it means it cannot be satisfied
    # (because a clause with no literals means no possible true assignment).
    for clause in clauses:
        if not clause:
            return False, assignment
        
    # Pick a variable to assign: take the absolute value of the first literal in the first clause (since we're dealing with literals, 
    # they can be positive or negative, so abs() helps us get the variable itself).
    variable = abs(clauses[0][0])

    # Try assigning the variable to True by removing any clause where 'variable'
    # is satisfied (i.e., where 'variable' appears) and removing '-variable' (negation) from the remaining clauses.
    new_clauses = [clause for clause in clauses if variable not in clause]
    new_clauses = [[lit for lit in clause if lit != -variable] for clause in new_clauses]
    
    # Recursively call DPLL with the modified clauses and assignment including 'variable = True'
    satisfiable, new_assignment = dpll(new_clauses, assignment + [variable])
    if satisfiable:
        return True, new_assignment
    
    # try assigning it to False if it didn't work with True 
    new_clauses = [clause for clause in clauses if -variable not in clause]
    new_clauses = [[lit for lit in clause if lit != variable] for clause in new_clauses]
    
    # recursively call function 
    return dpll(new_clauses, assignment + [-variable])

# Timing function
def run_dpll_and_time(wff):
    # unpack the cnf formula 
    num_vars, num_clauses, clauses = wff

    # start timer 
    start_time = time.time()

    # call dpll function 
    satisfiable, assignment = dpll(clauses, [])
    
    # calculate time 
    elapsed_time = time.time() - start_time
    return elapsed_time, satisfiable, num_vars

# Save results to CSV function
def save_results_to_csv(results, output_file):
    # open csv file to write 
    with open(output_file, mode='w', newline='') as csvfile:
        # add top line for labels 
        fieldnames = ['Filename', 'Execution Time (s)', 'Number of Variables', 'Satisfiability']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        # iterate over the list of results, where each result is a tuple containing: ('filename', 'elapsed_time', 'num_vars', 'satisfiable')
        for filename, elapsed_time, num_vars, satisfiable in results:
            writer.writerow({
                'Filename': filename,
                'Execution Time (s)': elapsed_time,
                'Number of Variables': num_vars,
                'Satisfiability': 'S' if satisfiable else 'U'
            })

# Main execution
if __name__ == '__main__':
    cnf_file = 'data_kSAT_hberens.cnf' 
    output_file = 'output_hberens.csv'

    # parse CNF file for all wffs
    all_wffs = parse_cnf_file(cnf_file)

    # store results for each wff
    results = []

    # run timing function 
    for index, wff in enumerate(all_wffs):
        elapsed_time, satisfiable, num_vars = run_dpll_and_time(wff)
        results.append((cnf_file, elapsed_time, num_vars, satisfiable))

    # Save results to CSV
    save_results_to_csv(results, output_file)
