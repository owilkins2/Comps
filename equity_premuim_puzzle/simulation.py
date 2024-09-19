# For standard theory: utility function is fixed, find the minimum E.P. such that investment is chosen, i.e. such that starting utility = exp_utility
#                   **(manipulate E.P. by chaning mean of distribution, other attributes the same)
# For behavioral considerations: utility function is variable w/ bracketing and loss aversion, E.P. is fixed by emperical data


import math
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import itertools


def utility(wealth):
    A = 2
    return 10000 * (wealth ** float((1 - A))) / (1 - A)


def get_exp_utility(starting_wealth, bin_values, bin_counts, num_repetitions, num_samples=100000):
    probabilities = bin_counts / np.sum(bin_counts)
    expected_utility = 0

    # Use Monte Carlo sampling to approximate the expected utility
    for _ in range(num_samples):
        sampled_combination = np.random.choice(bin_values, size=num_repetitions, p=probabilities)
        resulting_wealth = starting_wealth * np.prod(sampled_combination)
        util = utility(resulting_wealth)
        expected_utility += util
    expected_utility /= num_samples

    return expected_utility

def get_behavioral_utility(starting_wealth, bin_values, bin_counts, num_repetitions, bracket_size, loss_aversion_coefficient, num_samples=10000):
    probabilities = bin_counts / np.sum(bin_counts)
    expected_utility = 0

    for _ in range(num_samples):
        index = 0
        while(index < num_repetitions):
            sampled_combination = None
            full_bracket= True
            if(num_repetitions - index) > bracket_size:
                sampled_combination = np.random.choice(bin_values, size=bracket_size, p=probabilities)
            else:
                sampled_combination = np.random.choice(bin_values, size=num_repetitions - index, p=probabilities)
                full_bracket = False
            resulting_wealth = starting_wealth * np.prod(sampled_combination)
            util = 0
            if (resulting_wealth >= starting_wealth):
                util = utility(resulting_wealth)
            else:
                loss = starting_wealth - resulting_wealth
                util = utility(starting_wealth - (loss * loss_aversion_coefficient))
            if full_bracket:
                expected_utility += util * (bracket_size / num_repetitions)
            else:
                expected_utility += util * ((num_repetitions - index) / num_repetitions)
            index += bracket_size
    expected_utility /= num_samples

    return expected_utility


def generate_bins(num_bins):
    df = pd.read_csv('SP500_percent_changes.csv')
    percent_changes = df['SP500_PCH'].values
    returns = [1 + (.01 * percent_change) for percent_change in percent_changes]

    min = np.min(returns)
    max = np.max(returns)
    spread = max - min
    bin_width = spread / num_bins
    values = []
    counts = []
    for i in range(0, num_bins):
        values.append(min + (.5 * bin_width) + (i * bin_width))
        count = 0
        for value in returns:
            if ((value >= min + (i * bin_width)) and (value < min + ((i + 1) * bin_width))):
                count += 1
        counts.append(count)
    # for i in range(0, num_bins):
    #     print ('bin avg: ' + str(values[i]) + ', bin count: ' + str(counts[i]))
    return (values, counts)


def get_bond_mean():
    df = pd.read_csv('Bond_Yield.csv')
    annual_returns = df['DGS10'].values
    return np.mean(annual_returns)


def get_total_bond_return(num_months):
    return (1 + (get_bond_mean() * .01)) ** (num_months / 12)


def get_distribution_mean(bin_values, bin_counts):
    sum = 0
    count = 0
    for i in range(len(bin_values)):
        sum += bin_values[i] * bin_counts[i]
        count += bin_counts[i]
    return sum / count


def shift_distribution_mean(bin_values, annualized_amount):
    shifted_bin_values = [value + (1/12 * annualized_amount) for value in bin_values]
    return shifted_bin_values


def standard_calibration():
    starting_wealth = 100
    num_months = 120
    num_bins = 20
    (bin_values, bin_counts) = generate_bins(num_bins)
    shift_amount = -.1
    equity_premiums = []
    utility_differentials = []
    while(shift_amount <= 0):
        new_bin_values = shift_distribution_mean(bin_values, shift_amount)
        equity_premiums.append((((get_distribution_mean(new_bin_values, bin_counts)** 12) -1) * 100) - get_bond_mean())
        utility_differentials.append(get_exp_utility(starting_wealth, new_bin_values, bin_counts, num_months, 1000)
            - utility(get_total_bond_return(num_months) * starting_wealth))
        shift_amount += .001
    plt.scatter(equity_premiums, utility_differentials)
    plt.show()

def behavioral_calibration():
    starting_wealth = 100
    num_months = 120
    num_bins = 20
    bracket_size = 1
    loss_aversion_coefficient = 2
    (bin_values, bin_counts) = generate_bins(num_bins)
    bracket_sizes = []
    utilities = []
    while bracket_size <= num_months:
        bracket_sizes.append(bracket_size)
        utilities.append(get_behavioral_utility(starting_wealth, bin_values, bin_counts, num_months, bracket_size, loss_aversion_coefficient, 10))
        bracket_size += 1
    print("Bond Utility: " + str(utility(get_total_bond_return(num_months) * starting_wealth)))
    plt.scatter(bracket_sizes, utilities)
    plt.show()

standard_calibration()