import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats

df = pd.read_csv('SP500_percent_changes.csv')
sp500_pch = df['SP500_PCH'].values
#sp500_pch2 = sp500_pch_1[sp500_pch_1 != '.']
#sp500_pch = pd.to_numeric(sp500_pch2)

plt.figure(figsize=(12, 6))

plt.subplot(1, 2, 1)
fig, (n, bins, patches) = sns.histplot(sp500_pch, bins=20, kde=True)
for b in bins:
    for b1 in b:
        print(b1)
plt.title('Histogram of SP500_PCH')
plt.xlabel('SP500_PCH')
plt.ylabel('Frequency')


# plt.subplot(1, 2, 2)
# sns.kdeplot(sp500_pch, fill=True)
# plt.title('Density Plot of SP500_PCH')
# plt.xlabel('SP500_PCH')
# plt.ylabel('Density')

# plt.tight_layout()
# plt.show()

mean = np.mean(sp500_pch)
median = np.median(sp500_pch)
std_dev = np.std(sp500_pch)
skewness = stats.skew(sp500_pch)
kurtosis = stats.kurtosis(sp500_pch)

print(f"Mean: {mean:.4f}")
print(f"Median: {median:.4f}")
print(f"Standard Deviation: {std_dev:.4f}")
print(f"Skewness: {skewness:.4f}")
print(f"Kurtosis: {kurtosis:.4f}")

plt.show()

# df = pd.read_csv('Bond_Yield.csv')
# bond_pch1 = df['DGS10'].values
# bond_pch2 = bond_pch1[bond_pch1 != '.']
# bond_pch = pd.to_numeric(bond_pch2)
# 
#
# plt.subplot(1, 2, 2)
# sns.histplot(bond_pch, bins=6, kde=True)
# plt.title('Histogram of bond_PCH')
# plt.xlabel('bond_PCH')
# plt.ylabel('Frequency')
#
#
# # plt.subplot(1, 2, 2)
# # sns.kdeplot(bond_pch, fill=True)
# # plt.title('Density Plot of bond_PCH')
# # plt.xlabel('bond_PCH')
# # plt.ylabel('Density')
#
# plt.tight_layout()
# plt.show()
#
# mean = np.mean(bond_pch)
# median = np.median(bond_pch)
# std_dev = np.std(bond_pch)
# skewness = stats.skew(bond_pch)
# kurtosis = stats.kurtosis(bond_pch)
#
# print(f"Mean: {mean:.4f}")
# print(f"Median: {median:.4f}")
# print(f"Standard Deviation: {std_dev:.4f}")
# print(f"Skewness: {skewness:.4f}")
# print(f"Kurtosis: {kurtosis:.4f}")
