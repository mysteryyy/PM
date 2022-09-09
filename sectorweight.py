import pandas as pd
import warnings
import numpy as np
import yfinance as yf
import datetime
from pypfopt import EfficientFrontier, objective_functions
from pypfopt.expected_returns import capm_return
from pypfopt.risk_models import exp_cov
from sklearn.decomposition import PCA
import os

k = pd.read_excel("/home/sahil/PM/Portfolio_New_equity.xlsx")
k["sector"] = k.sector.apply(lambda x: "Consumer" if "Consumer" in x else x)
k["equity_weight"] = k["Asset Weight(%)"] / k["Asset Weight(%)"].sum()
sector_sums = {}
sector_sums["Technology"] = k[k.sector == "Technology"].equity_weight.sum()
sector_sums["Healthcare"] = k[k.sector == "Healthcare"].equity_weight.sum()
sector_sums["Financial Services"] = k[
    k.sector == "Financial Services"
].equity_weight.sum()
sector_sums["Consumer"] = k[k.sector == "Consumer"].equity_weight.sum()
k["sector_weight"] = k.apply(
    lambda row: row["equity_weight"] / sector_sums[row["sector"]],
    axis=1,
)
k["equity_weight"] = k.equity_weight * 100
k["sector_weight"] = k.sector_weight * 100
print(k)
