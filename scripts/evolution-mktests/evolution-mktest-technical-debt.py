import os
import csv
import numpy as np
import pandas as pd
from scipy.stats import norm as nrm, mstats

def perform_mk_test(x: list, alpha: float = 0.01):  
    """
    Mann-Kendall Test For Monotonic Trend
    https://vsp.pnnl.gov/help/vsample/design_trend_mann_kendall.htm
    
    Input:
        x:     a vector of data in the order in which it was collected over time
        alpha: significance level (0.05 default)
    Output:
        trend: tells the trend (increasing, decreasing, or no trend)
        h:     True (if trend is present) or False (if trend is absent)
        p:     p-value of the significance test
        z:     normalized test statistics 
    """
    n = len(x)

    # Compute S: the number of positive differences minus the number of negative differences
    s = 0
    for k in range(n - 1):
        for j in range(k + 1, n):
            s += np.sign(x[j] - x[k])

    # Calculate the unique data
    unique_x = np.unique(x)
    g = len(unique_x)

    # Compute VAR(S): the variance of S
    if n == g: # there are no tied groups
        var_s = (n * (n - 1) * (2 * n + 5)) / 18
    else: # there are some tied groups
        tp = np.zeros(unique_x.shape)
        for i in range(len(unique_x)):
            tp[i] = sum(unique_x[i] == x)
        var_s = (n * (n - 1) * (2 * n + 5) + np.sum(tp * (tp - 1) * (2 * tp + 5))) / 18

    # Compute Z: the MK test statistic
    # A positive (negative) value of Z indicates that the data tend to increase (decrease) with time
    if s > 0:
        z = (s - 1) / np.sqrt(var_s)
    elif s == 0:
        z = 0
    else:
        z = (s + 1) / np.sqrt(var_s)

    # Compute the p-value
    p = 2 * (1 - nrm.cdf(abs(z))) # two tail test
    h = abs(z) > nrm.ppf(1 - alpha / 2)

    if (z < 0) and h:
        trend = "Downward"
    elif (z > 0) and h:
        trend = "Upward"
    else:
        trend = "No trend"

    return h, trend, p, z

def analyze_td_evolution(column_name: str):
    df = pd.read_csv(os.path.join(os.path.dirname(__file__), "..\evolution-data-collection\data.csv"))[
        ["Project", "Language", column_name]
    ]

    df = df.groupby(["Project", "Language"]).agg(lambda x: list(x)).reset_index()

    df_grouped = df.groupby("Language")

    header = [
        "Project Name", 
        "Project Language", 
        "Monotonic Trend is Present", 
        ("TD" if column_name == "Technical Debt" else "Normalized TD") + " Trend Type", 
        "p-value", 
        "Z-value"
    ]
    
    with open(os.path.join(
        os.path.dirname(__file__), 
        ("td" if column_name == "Technical Debt" else "normalized_td") + '_data.csv'
    ), 'w', newline='') as file:

        writer = csv.writer(file)
        writer.writerow(header)

        for group_name, df_group in df_grouped:
            for row_index, row in df_group.iterrows():
                h, trend, p, z = perform_mk_test(row[column_name])
                writer.writerow([row["Project"], row["Language"], h, trend, p, z])

if __name__ == "__main__":
    analyze_td_evolution("Technical Debt")
    analyze_td_evolution("Size Normalized Technical Debt")
