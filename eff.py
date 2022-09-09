import pandas as pd
import datetime
import warnings
import numpy as np
import cvxopt as opt
from cvxopt import blas, solvers
from pypfopt import EfficientFrontier
from sklearn.decomposition import PCA
import os

warnings.filterwarnings("ignore")
os.chdir("/home/sahil/Downloads")

k = pd.read_csv("bench_rf105.csv", delimiter=";")
k1 = pd.read_csv("prices105.csv", delimiter=";")

# Function creates a columns of log returns and percentage returns for each asset in the DataFrame
def gen_ret(k1):
    assets = [
        i for i in k1.columns if i != "DATE"
    ]  # Extracting Column names of all assets

    for asset in assets:
        k1[asset + "_logret"] = (
            np.log(k1[asset] / k1[asset].shift(1)) * 100
        )  # Calculating log returns for an asset
        k1[asset + "_perret"] = (
            k1[asset].pct_change() * 100
        )  # Calculating percentage Returns for an asset
    return k1


k1 = gen_ret(k1)
k1["DATE"] = pd.to_datetime(k1.DATE).apply(lambda x: x.date())
k11 = k1[k1.DATE < datetime.date(2020, 6, 1)]
k12 = k1[k1.DATE > datetime.date(2020, 6, 1)]

assets_returns = [i for i in k11.columns if "_perret" in i]

mu = k11[assets_returns].mean() * 252  # Calculating mean for each asset
S = k11[assets_returns].cov() * 252  # Calculating covariance matrix for all assets
ef = EfficientFrontier(
    mu, S, weight_bounds=(0, 1)
)  # Initializing object with mean and covariance parameter and allowing short selling by setting weight bounds from -1 to 1
# ef.efficient_risk(
#    12.5
# )  # Creating Portfolio with target risk of 11%(Maximize return for target risk)

ef.max_sharpe(
    risk_free_rate=k[k.columns[2]].mean()
)  # finding maximum sharpe ratio portfolio

print(" Sharpe Ratio  ")
print("\n")
print(f"Mean for maximum sharpe ratio portfolio:{ef.portfolio_performance()[0]}")
print(f"Volatility for maximum sharpe ratio portfolio:{ef.portfolio_performance()[1]}")
print(
    f"Sharpe Ratio for maximum sharpe ratio portfolio:{ef.portfolio_performance()[2]}"
)
w = ef.clean_weights()
w = pd.Series(w)
w = w[w > 0.0001]
w = w.sort_values(ascending=False)
print(w)
print("out of sample")
mu = k12[assets_returns].mean() * 252  # Calculating mean for each asset
S = k12[assets_returns].cov() * 252  # Calculating covariance matrix for all assets
w = pd.Series(ef.clean_weights()).values
print("mean out of sample:", w.dot(mu))
print("Volatiility out of sample:", (w.T.dot(S)).dot(w) ** 0.5)


# print("\n")
# ef = EfficientFrontier(
#    mu, S, weight_bounds=(0, 1)
# )  # Weight bounds such that short selling allowed for portfolio
# ef.min_volatility()  # Creating a minimum volatility portfolio
# print(" Minimum Volatility  ")
# print("\n")
# print(f"Mean for minimum volatility portfolio:{ef.portfolio_performance()[0]}")
# print(f"Volatility for minimum volatility portfolio:{ef.portfolio_performance()[1]}")
# print(f"Sharpe Ratio for minimum volatility portfolio:{ef.portfolio_performance()[2]}")
# print("\n")
# ef = EfficientFrontier(
#    mu, S, weight_bounds=(0, 1)
# )  # Weight bounds such that short selling allowed for portfolio
# ef.efficient_risk(
#    14
# )  # Creating Portfolio with target risk of 14%(Maximize return for target risk)
# print(" Target Risk  ")
# print("\n")
# print(f"Mean for 14% target risk portfolio:{ef.portfolio_performance()[0]}")
# print(f"Volatility for 14% target risk portfolio:{ef.portfolio_performance()[1]}")
# print(f"Sharpe Ratio for 14% target portfolio:{ef.portfolio_performance()[2]}")
