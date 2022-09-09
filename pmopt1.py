import datetime
import os
import warnings

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import statsmodels.api as sm
import yfinance as yf
from pypfopt import EfficientFrontier, objective_functions
from pypfopt.black_litterman import BlackLittermanModel
from pypfopt.expected_returns import capm_return
from pypfopt.risk_models import CovarianceShrinkage, exp_cov
from scipy.stats import zscore
from sklearn.decomposition import PCA

warnings.filterwarnings("ignore")
os.chdir("/home/sahil/Downloads")
res = pd.read_pickle("regres.pkl")
k = pd.read_pickle("monthdata1.pkl")


def get_monthly_rets(stock):
    st = yf.download(stock, start="2010-01-01", end="2022-09-01")
    st.index = pd.to_datetime(st.index)
    stm = st.resample("M").agg("last")
    stm.index = stm.index.to_period("M")
    stm = pd.DataFrame(stm["Adj Close"])
    stm = stm.iloc[1:].dropna(axis=1)
    stm[f"{stock}_perret"] = stm["Adj Close"] / stm["Adj Close"].shift(1) - 1
    return stm


perret = [i for i in k.columns if "_perret" in i]


def portf(stm):
    mean = dict()
    error = dict()
    beta = res.params["x"]
    alpha = res.params["const"]
    nonret = [i for i in stm.columns if "_" not in i]

    for i in perret:
        mean[i] = (
            (beta * zscore(stm[i.replace("_perret", "")]) + alpha) / 100
        )[-1]
        mean[i] = (1 + mean[i]) ** 4 - 1
        error[i] = res.resid.var() * 4 / 100
    p = np.diag(np.ones(len(perret)))
    q = np.array([i for i in mean.values()])
    omega = np.diag([i for i in error.values()])
    pi = capm_return(stm[perret], returns_data=True)
    covshrink = CovarianceShrinkage(stm[perret], returns_data=True)
    cov = covshrink.ledoit_wolf(shrinkage_target="single_factor")
    bl = BlackLittermanModel(cov, pi=pi, P=p, Q=q, omega=omega)
    mu = bl.bl_returns()
    cov = bl.bl_cov()
    ef = EfficientFrontier(mu, cov, weight_bounds=(0, 1))
    ef.max_sharpe()
    print(ef.portfolio_performance())
    w = pd.Series(ef.clean_weights())
    return w


k["portret"] = None
k["weights"] = None
for i in range(len(k) - 60):
    oos = k.iloc[i + 60].name
    ktemp = k.iloc[i : i + 60]
    w = portf(ktemp)
    w = np.matrix(w)
    koos = k.iloc[i + 60]
    ret = np.matrix(koos[perret])
    k["portret"].loc[oos] = ret * w.T
    k["weights"].loc[oos] = w
    print(f"{i} done")
k = k.dropna()
tu_series = (
    np.abs(k["weights"].apply(lambda x: np.array(x)).diff())
    .dropna()
    .apply(lambda x: x.sum())
)
tsercost = 1 - 0.001 * tu_series
grate = tsercost * (1 + k.portret.dropna())
print((1 + k.portret.mean()) ** 12 - 1)
print(k.portret.std())
# print(k.portret.mean())
# print(k.portret.std())
