from data_process import get_data, read_data
from models import histogram, ratio, cca, corr, xgboost_shap, chi_square_test
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
    ratio(data.evaluate_ratio, save_path="pics/problem1/evaluate_ratio.png")
    # histogram pics
    df = pd.read_csv("docs/processed_data.csv")
    histogram(df, "qty_f_veg", [x for x in range(0, 30, 2)], 
              "pics/problem1/fresh_vegtables.png", standard=[6, 30])
    histogram(df, "num_day_foods", [x for x in range(0, 20, 2)], 
              "pics/problem1/num_day_foods.png", standard=[12, 20])
    histogram(df, "qty_f_fruits", [x for x in np.arange(0, 8, 0.5)], 
              "pics/problem1/quantity_fresh_fruits.png", standard=[4, 7])
    histogram(df, "qty_d_prods", [x for x in np.arange(0, 8, 0.5)], 
              "pics/problem1/dairy_products.png", standard=[4, 10])
    histogram(df, "qty_cereal", [x for x in np.arange(0, 5, 0.5)], 
              "pics/problem1/quantity_cereal.png", standard=[1, 3])
    histogram(df, "qty_lpfem", [x for x in range(0, 15, 1)], 
              "pics/problem1/quantity_lpfem.png", standard=[2.4, 4])
    histogram(df, "qty_oil", [x for x in range(0, 150, 10)], 
              "pics/problem1/quantity_oil.png", standard=[25, 30])
    histogram(df, "qty_beans", [x for x in np.arange(0, 1.2, 0.05)], 
              "pics/problem1/quantity_beans.png", standard=[0.6, 1])
    histogram(df, "qty_salt", [x for x in range(0, 30, 2)], 
              "pics/problem1/quantity_salt.png", standard=[0, 5])
    histogram(df, "qty_wine", [x for x in np.arange(0, 50, 5)], 
              "pics/problem1/quantity_wine.png", standard=[0, 15])
    histogram(df, "qty_beverage", [x for x in np.arange(0, 1.2, 0.05)], 
              "pics/problem1/quantity_beverage.png", standard=[0, 1])
    histogram(df, "ratio_at_home", [x for x in np.arange(0, 1, 0.1)], 
              "pics/problem1/ratio_at_home.png", standard=[0.5, 1])

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
    corr(data.iloc[:, np.r_[0:13, 16:21]], "pics/problem2/corr_analysis_1.png", 
         symmetry=False, x=np.r_[0:13], y=np.r_[13:18])
    # corr(data.iloc[:, np.r_[14:16, 16:21]], "pics/problem2/corr_analysis_2.png",figsize=(12, 6)) 
    corr(data.iloc[:, np.r_[14:16, 16:21]], "pics/problem2/corr_analysis_2.png", 
         figsize=(12, 6), symmetry=False, x=np.r_[0:2], y=np.r_[2:7])
    cca(X1, Y, "pics/problem2/CCA_1.png")
    cca(Y, X2, "pics/problem2/CCA_2.png", figsize=(15, 5))


# PROBLEM-3-XGBOOST-SHAP
def problem_3():
    # read data
    df = pd.read_csv("docs/processed_data.csv")
    df = df.fillna(0)
    X = df.iloc[:,np.r_[1, 16:28, 29:31]]
    Y = df.iloc[:,np.r_[40:45, 46]]
    # cca
    cca(X, Y,"pics/problem3/CCA_3.png", figsize=(30, 10))
    # corr
    # corr(Y, "pics/problem3/coor_diseases.png", figsize=(12, 12))
    # # # xgboost-shap
    # for i in range(Y.shape[1]):
    #     y = Y.iloc[:,np.r_[i]]
    #     xgboost_shap(X, y, "pics/problem3/"+y.columns.item())
        

def problem_4():
    # chi_square_test
    df = pd.read_csv("docs/processed_data.csv")
    df = df.fillna(0)
    data = df.iloc[:,-2:]
    chi_square_test(data)
    # read data
    df = pd.read_csv("docs/processed_data_young.csv")
    df = df.fillna(0)
    X = df.iloc[:,np.r_[1, 16:28, 29:31]]
    Y = df.iloc[:,np.r_[40:45, 46]]
    # cca
    cca(X, Y, "pics/problem4/young/CCA_young.png", figsize=(25, 12))
    # corr
    corr(Y, "pics/problem4/young/coor_diseases_young.png", figsize=(12, 12))
    # # xgboost-shap
    for i in range(Y.shape[1]):
        y = Y.iloc[:,np.r_[i]]
        xgboost_shap(X, y, "pics/problem4/young/"+y.columns.item()+"_young")
        
    # read data
    df = pd.read_csv("docs/processed_data_mid.csv")
    df = df.fillna(0)
    X = df.iloc[:,np.r_[1, 16:28, 29:31]]
    Y = df.iloc[:,np.r_[40:45, 46]]
    # cca
    cca(X, Y, "pics/problem4/mid/CCA_mid.png", figsize=(25, 12))
    # corr
    corr(Y, "pics/problem4/mid/coor_diseases_mid.png", figsize=(12, 12))
    # # xgboost-shap
    for i in range(Y.shape[1]):
        y = Y.iloc[:,np.r_[i]]
        xgboost_shap(X, y, "pics/problem4/mid/"+y.columns.item()+"_mid")
        
    # read data
    df = pd.read_csv("docs/processed_data_old.csv")
    df = df.fillna(0)
    X = df.iloc[:,np.r_[1, 16:28, 29:31]]
    Y = df.iloc[:,np.r_[40:46, 46]]
    # cca
    cca(X, Y, "pics/problem4/old/CCA_old.png", figsize=(25, 12))
    # corr
    corr(Y, "pics/problem4/old/coor_diseases_old.png", figsize=(12, 12))
    # # xgboost-shap
    for i in range(Y.shape[1]):
        y = Y.iloc[:,np.r_[i]]
        xgboost_shap(X, y, "pics/problem4/old/"+y.columns.item()+"_old")


if __name__ == '__main__':
    # pre_work()
    # problem_1()
    # problem_2()
    problem_3()
    # problem_4()
