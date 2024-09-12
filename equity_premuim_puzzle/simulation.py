#For standard theory: utility function is fixed, find the minimum E.P. such that investment is chosen, i.e. such that starting utility = exp_utility
#                   **(manipulate E.P. by chaning mean of distribution, other attributes the same)
#For behavioral considerations: utility function is variable w/ bracketing and loss aversion, E.P. is fixed by emperical data


import math
import seaborn as sns
import pandas as pd
import matplotlib
import numpy as np

def utility(wealth):
    A = 2
    return 10000 * (wealth ** (1-A)) / (1-A)

def get_exp_utility(starting_wealth, bin_values, bin_counts, num_repetitions):
    probabilities = []
    for i in range (0, num_repetitions + 1, 1):
        m = math.comb(num_repetitions, i)
        n = prob_win ** num_repetitions
        prob = m * n
        probabilities.append(prob)
    exp_utility = 0
    for i in range (0, num_repetitions + 1, 1):
        net_gain = i * mag_win + (num_repetitions - i) * mag_loss
        exp_utility += utility(starting_wealth + net_gain) * probabilities[i]
    return (exp_utility)

def generate_bins(num_bins):
    df = pd.read_csv('SP500_percent_changes.csv')
    returns = df['SP500_PCH'].values
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


starting_wealth = 1
num_bins = 10
(bin_values, bin_counts) = generate_bins(num_bins)
for i in range(0, num_bins):
        print ('bin avg: ' + str(bin_values[i]) + ', bin count: ' + str(bin_counts[i]))
#print("starting utility: " + str(utility(starting_wealth)) + "\nexpexted ending utility:" + str(get_exp_utility(starting_wealth, .5, 10, -8, 500)))
