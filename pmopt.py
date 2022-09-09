import datetime
import os
import warnings

import numpy as np
import pandas as pd
import statsmodels.api as sm
import yfinance as yf
from pypfopt import EfficientFrontier, objective_functions
from pypfopt.expected_returns import capm_return
from pypfopt.risk_models import exp_cov
from scipy.stats import zscore
from sklearn.decomposition import PCA

warnings.filterwarnings("ignore")
os.chdir("/home/sahil/Downloads")


def pred_reg(stname, st):
    st = st.fillna(0)
    k1 = pd.merge(k, st, how="inner", on="Date")
    retcol = f"{stname}_perret"
    k1[retcol] = k1[retcol].shift(-1)
    k1 = k1[[stname, retcol]].dropna()
    y = k1[retcol]
    x = np.log(k1[stname].astype(float))
    x = sm.add_constant(x)
    x = x.astype(float)
    print(sm.OLS(y, x).fit().summary())


k = pd.read_excel("Combined_Alphas_SPX.xlsx", header=0)
# k = k.iloc[1:]
# k.columns = ["Date"] + k.columns[1:].tolist()
ind = pd.date_range("1/1/2010", "1/7/2022", freq="M")
ind = ind.to_period("M")
k = k[
    [k.columns[0]]
    + [i for i in k.columns if "Combined Alpha Model Country Rank" in i]
]
cols = k.iloc[0]
k = k.iloc[1:]
cols = cols.tolist()
k.columns = [cols[0]] + [i.split(".", 1)[0] for i in cols[1:]]
k["Date"] = pd.to_datetime(k.Date.apply(lambda x: x[:-5])).dt.to_period("M")
k.index = k.Date
k = k.reindex(ind, method="ffill")
k = k.iloc[2:]
stocks = k.dropna(axis=1).columns[1:].tolist()
# Code for downloading the data which has been saved

st = yf.download(stocks, start="2010-01-01", end="2022-09-01")
st.index = pd.to_datetime(st.index)
stm = st.resample("M").agg("last")
stm.index = stm.index.to_period("M")
stm = stm["Adj Close"]
stm = stm.iloc[1:].dropna(axis=1)
for i in stm.columns:
    stm[f"{i}_perret"] = stm[i] / stm[i].shift(1) - 1

k = k.dropna(axis=1)
stname = k.columns[49]
# st = yf.download(stname, start="2010-01-01", end="2022-09-01", interval="1mo")
# st = pd.DataFrame(st["Adj Close"])
# st["ret"] = st / st.shift(1) - 1
# st["Date"] = st.index.to_period("M")
# k.index = k.Date
k = k.drop("Date", 1)
k = k.astype(float)
k.index.name = "Date"
# stm = pd.read_pickle("monthdata.pkl")
stm = stm.iloc[1:]
dat = []
for i in k.columns:
    df = pd.DataFrame()
    if i not in stm.columns:
        continue
    retcol = f"{i}_perret"
    logretcol = f"{i}_logret"
    stm[logretcol] = np.log(stm[retcol] + 1)
    lret = stm[logretcol]
    stm[f"{i}_quarter"] = np.exp(lret + lret.shift(1) + lret.shift(2)) - 1
    df = pd.merge(k, stm, how="inner", on="Date")
    # df["x"] = df[f"{i}_x"]
    df["x"] = zscore(df[f"{i}_x"])
    # df["x"] = k[i]
    df["y"] = df[f"{i}_quarter"].shift(-2) * 100
    # df["y"] = df[retcol].shift(-1) * 100
    # df = df.dropna()
    # df["y"] = zscore(df["y"])
    # For tetsing quarterly sampling
    #
    # df["y"] = stm[logretcol] * 100
    # df = df.resample("Q").agg({"x": "first", "y": "sum"})
    # df["y"] = (np.exp(df["y"] / 100) - 1) * 100
    df = df.dropna()
    dat.append(df)
dat = pd.concat(dat)
x = dat["x"].astype(float)
x = sm.add_constant(x)
y = dat["y"]
x = x[0 : int(len(x) / 2)]
y = y[0 : int(len(y) / 2)]
res = sm.OLS(y, x.astype(float)).fit()

# st.index = st.Date
# st = st.drop("Date", 1)
# pred_reg(stname, stm[f"{stname}_perret"])
