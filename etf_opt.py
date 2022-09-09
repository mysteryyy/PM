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

warnings.filterwarnings("ignore")
os.chdir("/home/sahil/PM")

etfs = pd.read_excel("isharesetf.xlsx")
vanguard_etfs_plusextra = {
    "Vanguard 500 Index Fund": "VFIAX",
    "Vanguard Total Stock Market index Fund": "VTSAX",
    "Vanguard Total Bond Market Index Fund": "VBTLX",
    "Vanguard Balanced Index Fund": "VBIAX",
    "Vanguard Growth Index Fund": "VIGAX",
    "Vanguard Small Cap Index Funds": "VSMAX",
    "Corn Futures": "ZC=F",
    "Natural Gas Futures": "NG=F",
    "Platinium Futures": "PL=F",
    "Palladium Futures": "PA=F",
    "Rough Rice Fut": "ZR=F",
}
tech_stock = pd.ExcelFile("/home/sahil/Downloads/Equities.xlsx")
tech_stock = pd.read_excel(tech_stock, "Sheet1")
health_stock = pd.read_excel("/home/sahil/Downloads/HEALTHCARE.xlsx")
stock = pd.ExcelFile("/home/sahil/Downloads/PM.xlsx")
# materials = pd.read_excel(stock, "Materials")
etfs_choice = ["IYK"]
# industrials = pd.read_excel(stock, "Industrial")
# telcom = pd.read_excel(stock, "Telecommunication")
cons = pd.read_excel(stock, "Consumer Discretionary")
fin = pd.read_excel(stock, "Financial Sector")
total_stocks = pd.concat([tech_stock, health_stock, cons, fin], axis=0)
for tick, name in zip(total_stocks.Ticker, total_stocks.Name):
    # name = " ".join(yf.Ticker(i).info["longBusinessSummary"].split()[:2])
    vanguard_etfs_plusextra[name] = tick


#
# for index, row in medical_stock.iterrows():
#    vanguard_etfs_plusextra[row["Name"]] = row["Ticker"]
def new_assets():
    etf = pd.read_excel("/home/sahil/Downloads/Portfolio_Holdings.xlsx")
    etf["ratio"] = etf["Morningstar ratio"].apply(
        lambda x: x if isinstance(x, int) else 0
    )
    etf = etf[etf.ratio >= 3]
    eq_fi = list(etf["Asset Symbol"])
    comm = ["ZC=F", "NG=F", "PA=F", "PL=F", "ZR=F"]
    symbols = eq_fi + comm
    assets = []
    for idx, i in enumerate(symbols):
        etf = yf.download(i, start="2016-01-01", end="2022-04-12")
        etf = pd.DataFrame(etf["Adj Close"])
        # Calculating daily log returns
        etf[f"{i}_perret"] = np.log(etf.pct_change() + 1)

        assets.append(etf)
    assets = pd.concat(assets, axis=1)
    assets = assets.drop("Adj Close", axis=1)
    assets = assets.dropna(how="all", axis=1)
    assets.to_pickle("high_rated_assets_returns.pkl")
    return assets


def save_returns(etfs):
    # Below two lines filter out etfs that invest in developed markets and invest only in
    # Fixed Income and Equity asset classes
    etfs = etfs[(etfs["Market"] == "Developed")]
    etfs = etfs[etfs["Asset Class"].isin(["Fixed Income"])]
    assets = []
    # van_funds = ["VFIAX", "VTSAX", "VBTLX", "VBIAX", "VIGAX", "VSMAX"]
    van_funds = ["VBTLX"]
    comm = ["ZC=F", "NG=F", "PA=F", "PL=F", "ZR=F"]
    symbols = (
        list(etfs["Ticker"].iloc[1:]) + list(total_stocks.Ticker) + comm + etfs_choice
    )
    for idx, i in enumerate(symbols):
        if idx < len(etfs.Ticker) - 1:
            etf_asset = etfs[etfs["Ticker"] == i]
            etf_asset["Date"] = etf_asset["Incept. Date"].apply(lambda x: x.date())
            # The line below rejects assets which did not exist before 2016
            if etf_asset["Date"].iloc[0] > datetime.date(2016, 1, 1):
                continue
        etf = yf.download(i, start="2016-01-01", end="2022-04-12")
        etf = pd.DataFrame(etf["Adj Close"])
        # Calculating daily log returns
        if i == "VBTLX":
            # Return times -1 since we are trying to short VBTLX
            etf[f"{i}_perret"] = np.log(etf.pct_change() + 1) * -1
        # elif i == "SOXX" or i == "IHI":
        #    continue
        else:
            etf[f"{i}_perret"] = np.log(etf.pct_change() + 1)

        assets.append(etf)
    assets = pd.concat(assets, axis=1)
    assets = assets.drop("Adj Close", axis=1)
    assets = assets.dropna(how="all", axis=1)
    assets.to_pickle("etfs_developed_returns.pkl")


# save_returns(etfs)
assets = pd.read_pickle("etfs_developed_returns.pkl")
# assets = new_assets()
# Drop columns with all blank values
assets = assets.dropna(how="all", axis=1)
# Download benchmark return
benchmark = yf.download("SPY", start="2016-01-01", end="2022-04-12")
# benchmark log returns calculation
benchmark["mkt"] = np.log(benchmark["Adj Close"].pct_change() + 1)
mu_target = (
    benchmark.mkt.mean() * 252
)  # benchmark annualized average returns calculation
target_risk = 0.145  # Setting target volatility of 14.5%
mu = assets.mean() * 252  # Annualized mean of all the assets considered
# S = exp_cov(assets, returns_data=True, span=500)
S = assets.cov() * 252  # Annualized covariance of all the assets considered
ef = EfficientFrontier(mu, S, weight_bounds=(0, 1))  # Initializing optimizer object
gamma = 0.5
constraints = [
    {
        "type": "eq",
        "fun": lambda w: target_risk ** 2 - np.dot(w.T, np.dot(ef.cov_matrix, w)),
    },
]  # Setting constraint function to meet the target volatility
ef.nonconvex_objective(
    lambda w, mu: -(w.T.dot(mu) - mu_target) + gamma * w.T.dot(w),
    objective_args=(ef.expected_returns,),
    weights_sum_to_one=True,
    constraints=constraints,
)  # Objective function which will maximize returns over sp500 and at the same time not allocate very high weights to one asset


print(ef.portfolio_performance(verbose=True))
w = ef.clean_weights()  # Getting weights from the optimizer
w = pd.Series(w)
# Remove all weights that are 0
asset_type = lambda x: yf.Ticker(x).info["quoteType"]
asset_sector = lambda x: yf.Ticker(x).info["sector"]


def symbol_name(symb):
    etf_name = etfs[etfs.Ticker == symb].Name.values

    if len(etf_name) == 0:
        return list(vanguard_etfs_plusextra.keys())[
            list(vanguard_etfs_plusextra.values()).index(symb)
        ]
    else:
        return etf_name[0]


w = w[w != 0]  # Eliminate all assets with 0 weight
# The lines below are just concerned with
w = w.sort_values(ascending=False)
holdings = pd.DataFrame()
holdings["Asset Symbol"] = pd.Series(w.index).apply(lambda x: x.replace("_perret", ""))
holdings["Asset Weight(%)"] = w.values * 100
holdings["Asset Name"] = holdings["Asset Symbol"].apply(lambda x: symbol_name(x))
holdings = holdings.reindex()
holdings["class"] = holdings["Asset Symbol"].apply(lambda x: asset_type(x))
holdings_eq = holdings[holdings["class"] == "EQUITY"]
holdings_eq["sector"] = holdings_eq["Asset Symbol"].apply(lambda x: asset_sector(x))
print("Equity Holdings ")
print(holdings_eq)
print(holdings)
print(ef.portfolio_performance(verbose=True))
print(
    "Commodity Weightings Percentage = ",
    holdings[holdings["Asset Symbol"].str.contains("=")]["Asset Weight(%)"].sum(),
)
