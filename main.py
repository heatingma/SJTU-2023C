from data_process import get_data, read_data
from models import histogram, ratio, cca, corr, xgboost_shap
import pandas as pd
import numpy as np


# GRT DATA
def pre_work():
    read_data('data/附件2 慢性病及相关因素流调数据.xlsx')
    data = get_data()
    data.get_dataframe()


# PROBLEM-1-DRAW PICS
def problem_1():
    # ratio pic
    data = get_data()
    ratio(data.evaluate_ratio)
    # histogram pics
    df = pd.read_csv("docs/processed_data.csv")
    histogram(df, "qty_f_veg", [x for x in range(0, 30, 2)], "pics/fresh_vegtables.png", standard=[6, 30])
    histogram(df, "num_day_foods", [x for x in range(0, 20, 2)], "pics/num_day_foods.png", standard=[12, 20])
    histogram(df, "qty_f_fruits", [x for x in np.arange(0, 8, 0.5)], "pics/quantity_fresh_fruits.png", standard=[4, 7])
    histogram(df, "qty_d_prods", [x for x in np.arange(0, 8, 0.5)], "pics/dairy_products.png", standard=[4, 10])
    histogram(df, "qty_cereal", [x for x in np.arange(0, 5, 0.5)], "pics/quantity_cereal.png", standard=[1, 3])
    histogram(df, "qty_lpfem", [x for x in range(0, 15, 1)], "pics/quantity_lpfem.png", standard=[2.4, 4])
    histogram(df, "qty_oil", [x for x in range(0, 150, 10)], "pics/quantity_oil.png", standard=[25, 30])
    histogram(df, "qty_beans", [x for x in np.arange(0, 1.2, 0.05)], "pics/quantity_beans.png", standard=[0.6, 1])
    histogram(df, "qty_salt", [x for x in range(0, 30, 2)], "pics/quantity_salt.png", standard=[0, 5])
    histogram(df, "qty_wine", [x for x in np.arange(0, 50, 5)], "pics/quantity_wine.png", standard=[0, 15])
    histogram(df, "qty_beverage", [x for x in np.arange(0, 1.2, 0.05)], "pics/quantity_beverage.png", standard=[0, 1])
    histogram(df, "ratio_at_home", [x for x in np.arange(0, 1, 0.1)], "pics/ratio_at_home.png", standard=[0.5, 1])

# PROBLEM-2-CCA
def problem_2():
    df = pd.read_csv("docs/processed_data.csv")
    df = df.fillna(0)
    data = df.iloc[:,np.r_[1,16:36]]
    data.iloc[0] = False
    data = data.replace({'True': 1, 'False': 0}) 
    data = data.astype("int")
    X1 = data.iloc[:, np.r_[0:13]]
    X2 = data.iloc[:, np.r_[14:16]]
    Y = data.iloc[:, np.r_[16:21]]
    corr(data.iloc[:, np.r_[0:13, 16:21]], "pics/corr_analysis_1.png")
    corr(data.iloc[:, np.r_[14:16, 16:21]], "pics/corr_analysis_2.png")
    cca(X1, Y, "pics/CCA_1.png")
    cca(X2, Y, "pics/CCA_2.png", figsize=(12,6))


# PROBLEM-3-XGBOOST-SHAP
def problem_3():
    # read data
    df = pd.read_csv("docs/processed_data.csv")
    df = df.fillna(0)
    X = df.iloc[:,np.r_[1, 16:28, 29:31]]
    Y = df.iloc[:,np.r_[40:45]]
    # cca
    cca(X, Y, "pics/CCA_3.png", figsize=(12, 18))
    # corr
    corr(Y, "pics/coor_diseases.png", figsize=(12, 12))
    # # xgboost-shap
    for i in range(Y.shape[1]):
        y = Y.iloc[:,np.r_[i]]
        xgboost_shap(X, y, "pics/"+y.columns.item())
    
if __name__ == '__main__':
    # pre_work()
    # problem_1()
    # problem_2()
    problem_3()
    

