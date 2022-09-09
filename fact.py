import pandas as pd
import warnings
import numpy as np
import cvxopt as opt
from cvxopt import blas, solvers
from pypfopt import EfficientFrontier
from sklearn.decomposition import PCA
import os

warnings.filterwarnings("ignore")
os.chdir("/home/sahil/Downloads")

k = pd.read_csv("spnrf.csv")
k1 = pd.read_csv("price.csv")

print(k)
