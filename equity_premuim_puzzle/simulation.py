import math
import matplotlib

def utility(wealth):
    return math.sqrt(wealth)

def get_exp_utility(starting_wealth, prob_win, mag_win, mag_loss, num_repetitions):
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

starting_wealth = 10000
print("starting utility: " + str(utility(starting_wealth)) + "\nexpexted ending utility:" + str(get_exp_utility(starting_wealth, .5, 10, -8, 500)))
