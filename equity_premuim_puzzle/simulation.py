#For standard theory: utility function is fixed, find the minimum E.P. such that investment is chosen, i.e. such that starting utility = exp_utility
#                   **(manipulate E.P. by chaning mean of distribution, other attributes the same)
#For behavioral considerations: utility function is variable w/ bracketing and loss aversion, E.P. is fixed by emperical data


import math
import seaborn as sns
import pandas as pd
import matplotlib
import numpy as np
import itertools

def utility(wealth):
    A = 2
    return 10000 * (wealth ** (1-A)) / (1-A)

def get_exp_utility(starting_wealth, bin_values, bin_counts, num_repetitions):
        # Normalize bin_counts to get probabilities
    probabilities = bin_counts / np.sum(bin_counts)

        # Generate all possible combinations of bin_values over num_repetitions
    all_combinations = list(itertools.product(bin_values, repeat=num_repetitions))

    expected_utility = 0

        # Iterate over each combination
    for combination in all_combinations:
            # Calculate the probability of this combination (product of individual probabilities)
        combination_prob = np.prod([probabilities[bin_values.index(value)] for value in combination])

            # Calculate the resulting wealth for this combination
        resulting_wealth = starting_wealth * np.prod(combination)

            # Apply the utility function to the resulting wealth
        util = utility(resulting_wealth)

            # Add the weighted utility to the expected utility
        expected_utility += combination_prob * util
    return expected_utility

def generate_bins(num_bins):
    df = pd.read_csv('SP500_percent_changes.csv')
    percent_changes = df['SP500_PCH'].values
    returns = [1 + (.01 * percent_change) for percent_change in percent_changes]
    min = np.min(returns)
    max = np.max(returns)
    spread = max-min
    bin_width = spread/num_bins
    values = []
    counts = []
    for i in range(0, num_bins):
        values.append(min + (.5 * bin_width) + (i * bin_width))
        count = 0
        for value in returns:
            if ( (value >= min + (i * bin_width)) and (value < min + ((i +1) * bin_width)) ):
                count += 1
        counts.append(count)
    # for i in range(0, num_bins):
    #     print ('bin avg: ' + str(values[i]) + ', bin count: ' + str(counts[i]))
    return(values, counts)


starting_wealth = 100
num_bins = 10
# (bin_values, bin_counts) = generate_bins(num_bins)
# for i in range(0, num_bins):
#         print ('bin avg: ' + str(bin_values[i]) + ', bin count: ' + str(bin_counts[i]))
bin_values = [-1, 1, 2]
bin_counts = [1, 2, 1]
print("starting utility: " + str(utility(starting_wealth)) + "\nexpexted ending utility: " + str(get_exp_utility(starting_wealth, bin_values, bin_counts, 10)))
