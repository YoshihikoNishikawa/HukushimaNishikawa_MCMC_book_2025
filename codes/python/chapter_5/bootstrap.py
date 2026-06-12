###################################################################################
# PROGRAM: bootstrap.py
# DATE: 2026-06-12
# NOTICE: This program accompanies the book "マルコフ連鎖モンテカルロ法入門"
#                     by Koji Hukushima and Yoshihiko Nishikawa
###################################################################################

import numpy as np


def Bootstrap(data, func, num_samples):
    """
    アルゴリズム23
    Bootstrap resampling on a dataset.

    Parameters:
    data: The original dataset to resample from.
    func: The function to apply to each bootstrap sample.
    num_samples: The number of bootstrap samples.

    Returns:
    list: A list of bootstrap samples
    """

    n = len(data)
    bsamples = [func(data[np.random.randint(0, n, n)])
                for _ in range(num_samples)]

    return np.array(bsamples)


def StdErrorBootstrap(data, func, num_samples):
    """
    アルゴリズム24
    Calculate the standard error from bootstrap samples.

    Parameters:
    data: The original dataset to resample from.
    func: The function to apply to each bootstrap sample.
    num_samples: The number of bootstrap samples to generate.

    Returns:
    float: The standard error of the statistic calculated from the bootstrap samples.
    """

    bsamples = Bootstrap(data, func, num_samples)
    bmean = np.mean(bsamples)
    stderror = (np.sum((bsamples - bmean) ** 2) / (num_samples - 1))**.5
    return stderror


def Percentile(data, func, num_samples, alpha):
    """
    アルゴリズム25
    Calculate the specified percentile of a statistic using bootstrap resampling.

    Parameters:
    data: The original dataset to resample from.
    func: The function to apply to each bootstrap sample.
    num_samples: The number of bootstrap samples to generate.
    alpha: Confidence level (e.g., 0.68 for a 68% confidence interval).

    Returns:
    float: The specified percentile of the statistic calculated from the bootstrap samples.
    """
    bsamples = Bootstrap(data, func, num_samples)
    bsamples.sort()
    lower_index = int((1 - alpha) * 0.5 * num_samples)
    upper_index = int((1 - (1 - alpha) * 0.5) * num_samples)
    return [bsamples[lower_index], bsamples[upper_index]]


def Bootstrap_t(data, func, num_samples, alpha):
    """
    アルゴリズム26
    Perform bootstrap resampling and calculate the t-statistic for each sample.

    Parameters:
    data: The original dataset to resample from.
    func: The function to apply to each bootstrap sample.
    num_samples: The number of bootstrap samples to generate.
    alpha: Confidence level (e.g., 0.68 for a 68% confidence interval).

    Returns:
    list: A list of t-statistics calculated from the bootstrap samples.
    """
    btsamples = []
    n = len(data)
    mean = func(data)
    stderror = StdErrorBootstrap(data, func, num_samples)

    for _ in range(num_samples):
        # Generate a bootstrap sample by randomly sampling with replacement
        sample = np.random.choice(data, size=n, replace=True)
        statistic = func(sample)
        b_stderror = StdErrorBootstrap(sample, func, 100)
        t = (statistic - mean) / b_stderror
        btsamples.append(t)

    btsamples.sort()
    lower_index = int((1 - alpha) * 0.5 * num_samples)
    upper_index = int((1 - (1 - alpha) * 0.5) * num_samples)

    return [mean - stderror * btsamples[upper_index], mean - stderror * btsamples[lower_index]]


def main():
    # Example usage of the bootstrap functions
    # Sample data from a normal distribution
    data = np.array(np.random.normal(loc=0, scale=1, size=100))
    num_samples = 1000

    # Example usage of the bootstrap functions
    bsamples = Bootstrap(data, np.var, num_samples)
    std_error = StdErrorBootstrap(data, np.var, num_samples)
    percentile_conf_int = Percentile(data, np.var, num_samples, 0.68)
    t_conf_int = Bootstrap_t(data, np.var, num_samples, 0.68)

    print("Variance of the data:", np.var(data))
    print("Bootstrap samples (variance):", bsamples)
    print("Standard error of variance:", std_error)
    print("68% percentile confidence interval for variance:", percentile_conf_int)
    print("Bootstrap t-confidence interval for variance:", t_conf_int)


if __name__ == "__main__":
    main()
