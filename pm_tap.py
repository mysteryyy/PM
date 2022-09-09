import pandas as pd
import warnings
import numpy as np
from pypfopt import EfficientFrontier
import statsmodels.api as sm
import os

warnings.filterwarnings("ignore")
os.chdir("/home/sahil/Downloads")

k = pd.read_excel("TAP-excel.xlsx")

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


# k1 = gen_ret(k1)
expected = {}
mu = {}
var = {}
beta = {}
resid_var = {}
alpha = {}
k["index_ret"] = k["Index Return "]
k = k.drop(columns=["Index Return "])
assets_returns_cols = [i for i in k.columns[1:]]
for i in assets_returns_cols:
    ret_col_name = f"{i}_ret"
    if i != "index_ret":
        k[f"{i}_ret"] = np.log(k[i] / k[i].shift(1))
        y = k[ret_col_name].dropna()
    else:
        y = k["index_ret"].dropna()
    y = y - 0.02 / 252
    x = k["index_ret"].dropna()
    x = x - 0.02 / 252
    x = sm.add_constant(x)
    model = sm.OLS(y, x)
    res = model.fit()
    alpha[f"{i}_alpha"] = res.params["const"]
    resid_var[f"{i}_resid_var"] = res.resid.var()
    beta_asset = res.params["index_ret"]
    beta[f"{i}_beta"] = beta_asset
cov = pd.DataFrame(index=assets_returns_cols, columns=assets_returns_cols)
bprem = k.index_ret.mean() - 0.02 / 252
alpha = np.matrix(pd.Series(alpha))
beta = np.matrix(pd.Series(beta))
mu = (alpha + bprem * beta + 0.02 / 252) * 252
resid = np.diag(list(pd.Series(resid_var)))
covar = (beta.T * beta * k["index_ret"].var() + resid) * 252
ef = EfficientFrontier(np.array(mu.T), covar, weight_bounds=(-1, 1))
ef.max_sharpe(risk_free_rate=0.02)
print(ef.weights)
print(ef.portfolio_performance(verbose=True))
