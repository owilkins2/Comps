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


def gain_loss_utility(change_in_wealth, loss_aversion_coefficient):
    if change_in_wealth >= 0:
        return change_in_wealth
    else:
        return change_in_wealth * loss_aversion_coefficient


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
    shifted_bin_values = [value + (1 / 12 * annualized_amount) for value in bin_values]
    return shifted_bin_values


def get_behavioral_utility_differential(starting_wealth, bin_values, bin_counts, num_repetitions, bracket_size,
                                        loss_aversion_coefficient, num_samples=10000):
    probabilities = bin_counts / np.sum(bin_counts)
    utility_differential = 0
    monthly_bond_return = (1 + (.01 * get_bond_mean())) ** (1 / 12)

    for _ in range(num_samples):
        index = 0
        utility_differential_local = 0

        while (index < num_repetitions):
            sampled_combination = None
            full_bracket = True
            if (num_repetitions - index) > bracket_size:
                sampled_combination = np.random.choice(bin_values, size=bracket_size, p=probabilities)
            else:
                sampled_combination = np.random.choice(bin_values, size=num_repetitions - index, p=probabilities)
                full_bracket = False
            resulting_wealth_stock = starting_wealth * np.prod(sampled_combination)
            resulting_wealth_bond = starting_wealth * (monthly_bond_return ** bracket_size)
            util_bond = utility(resulting_wealth_bond)
            util_stock = 0

            if (resulting_wealth_stock >= starting_wealth):
                util_stock = utility(resulting_wealth_stock)
            else:
                loss = starting_wealth - resulting_wealth_stock
                util_stock = utility(starting_wealth - (loss * loss_aversion_coefficient))

            utility_differential_local += (util_stock - util_bond)
            # print("Resulting Wealth S: " + str(resulting_wealth_stock) + ", Resulting Wealth B: " + str(resulting_wealth_bond)
            #       + ", Utility D: " + str(utility_differential))

            # if full_bracket:
            #     utility_differential += (abs(util_stock) - abs(util_bond)) * (bracket_size / num_repetitions)
            # else:
            #     utility_differential += (util_stock - util_bond) * ((num_repetitions - index) / num_repetitions)
            index += bracket_size
        utility_differential += utility_differential_local
    utility_differential /= num_samples

    return utility_differential


def standard_calibration():
    starting_wealth = 100
    num_months = 120
    num_bins = 20
    (bin_values, bin_counts) = generate_bins(num_bins)
    shift_amount = -.1
    equity_premiums = []
    utility_differentials = []
    while shift_amount <= 0:
        new_bin_values = shift_distribution_mean(bin_values, shift_amount)
        equity_premiums.append(
            (((get_distribution_mean(new_bin_values, bin_counts) ** 12) - 1) * 100) - get_bond_mean())
        utility_differentials.append(get_exp_utility(starting_wealth, new_bin_values, bin_counts, num_months, 1000)
                                     - utility(get_total_bond_return(num_months) * starting_wealth))
        shift_amount += .001
    plt.scatter(equity_premiums, utility_differentials)
    plt.xlabel("Equity Premium (%)")
    plt.ylabel("Utility Differential (Stocks - Bonds)")
    plt.axline((0, 0), slope=0)
    plt.savefig("Equity Premiums Graph")
    plt.show()


def behavioral_calibration():
    starting_wealth = 100
    num_months = 120
    num_bins = 20
    bracket_size = 1
    loss_aversion_coefficient = 2
    (bin_values, bin_counts) = generate_bins(num_bins)
    bracket_sizes = []
    utility_differentials = []
    while bracket_size <= num_months:
        bracket_sizes.append(bracket_size)
        utility_differentials.append(
            get_behavioral_utility_differential(starting_wealth, bin_values, bin_counts, num_months, bracket_size,
                                                loss_aversion_coefficient, 1000))
        bracket_size += 1
    bond_utility = utility(get_total_bond_return(num_months) * starting_wealth)
    print("Bond Utility: " + str(bond_utility))
    plt.scatter(bracket_sizes, utility_differentials)
    plt.xlabel("Bracket Size (months)")
    plt.ylabel("Utility Differential")
    plt.savefig("Bracket Sizes Graph")
    plt.show()


def create_heatmap():
    data = []
    (bin_values, bin_counts) = generate_bins(20)
    for loss_aversion_x10 in range(10, 40, 1):
        loss_aversion = loss_aversion_x10 / 10
        for bracketing in range(1, 50, 1):
            utility_differential = get_behavioral_utility_differential(100, bin_values, bin_counts, 120, bracketing,
                                                                       loss_aversion, 100000)
            data.append([loss_aversion, bracketing, abs(utility_differential)])

    df = pd.DataFrame(data, columns=['Loss Aversion', 'Bracket Size', 'Utility Differential'])

    pivot_table = df.pivot(index='Loss Aversion', columns='Bracket Size', values='Utility Differential')

    plt.figure(figsize=(8, 6))
    sns.heatmap(pivot_table, annot=False, cmap="Blues_r", cbar=True, vmax=100, vmin=0)

    plt.title('Utility Differential Heatmap')
    plt.xlabel('Bracket Size (months)')
    plt.ylabel('Loss Aversion Coefficient')

    plt.savefig("heatmap")
    plt.show()


create_heatmap()
# standard_calibration()
# behavioral_calibration()
