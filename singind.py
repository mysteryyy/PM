import pandas as pd
import numpy as np
import statsmodels.api as sm
import os
import warnings

warnings.filterwarnings("ignore")
from pypfopt.risk_models import CovarianceShrinkage
from pypfopt import risk_models
from pypfopt.efficient_frontier import EfficientFrontier
from pypfopt import HRPOpt

os.chdir("/home/sahil/Downloads")
k1 = pd.read_csv("train.csv")
k2 = pd.read_csv("test.csv")

k1 = k1.dropna(axis=1)
k2 = k2.dropna(axis=1)


def gen_ret(df):
    assets = [
        i for i in df.columns if i != "Date"
    ]  # Extracting Column names of all assets

    for asset in assets:
        df[asset + "_logret"] = (
            np.log(df[asset] / df[asset].shift(1)) * 100
        )  # Calculating log returns for an asset
        # df[asset + "_perret"] = (
        #    df[asset].pct_change() * 100
        # )  # Calculating percentage Returns for an asset
    # perret_cols = [i for i in df.columns if "_perret" in i]
    return df


# Store names of log returns columns
k_train = gen_ret(k1.copy())
# Store list of column names for log returns
lret = [i for i in k_train.columns if "_logret" in i]
k_test = gen_ret(k2.copy())
k_train = k_train.dropna()
k_test = k_test.dropna()
# Calculate Covariance matrix using Ledoit Wolf single factor method
#cov = risk_models.risk_matrix(
    k_train[lret], method="ledoit_wolf_single_factor", returns_data=True
)
# Function for calculationg Sharpe ratio given daily returns
def sharpe(port):
    return port.mean() * 252 / (port.var() * 252) ** 0.5


# Set up optimization objective assuming daily average returns as 0
# When we dont have an accurate method for forecasting returns, it is better to assume the avergae as 0
ef = EfficientFrontier(cov_matrix=cov, verbose=False, expected_returns=None)
# Calculate weights optimizing for minimum volatility
ef.min_volatility()
# Extract weights
w = np.matrix(pd.Series(ef.clean_weights()))
# Extract matrix of test and train set returns
train_rets = np.matrix(k_train[lret])
test_rets = np.matrix(k_test[lret])
# calculate minimum volatility portoflio returns on test and train set
port_train = train_rets * w.T
port_test = test_rets * w.T
# test and Set portfolio sharpe for minimum volatility optimizer
print(
    "Minimum Volatility Optimizer Train Set sharpe ratio performance(Sharpe Ratio) ",
    sharpe(port_train),
)
print(
    "Minimum Volatility Optimizer Test Set sharpe ratio performance(Sharpe Ratio)",
    sharpe(port_test),
)

# Use HRP on train set
hrp = HRPOpt(k_train[lret])
hrp_weights = np.matrix(pd.Series(hrp.optimize()))
# HRP portfolio train and test returns
port_train = train_rets * hrp_weights.T
port_test = test_rets * hrp_weights.T
print("HRP Performance on Train set(Sharpe Ratio)", sharpe(port_train))
print(
    "HRP Performance on Test set(Sharpe Ratio)",
    sharpe(port_test),
)
