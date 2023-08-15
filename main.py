from utils import get_data, read_data, draw_histogram, draw_ratio
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
import seaborn as sns
from sklearn.cross_decomposition import CCA


# GRT DATA
def pre_work():
    read_data('data/附件2 慢性病及相关因素流调数据.xlsx')
    data = get_data()
    data.get_dataframe()


# PROBLEM-1-DRAW PICS
def problem_1():
    # ratio pic
    data = get_data()
    draw_ratio(data.evaluate_ratio)
    # histogram pics
    df = pd.read_csv("docs/processed_data.csv")
    draw_histogram(df, "qty_f_veg", [x for x in range(30)], "pics/fresh_vegtables.png")
    draw_histogram(df, "num_day_foods", 15, "pics/num_day_foods.png")
    draw_histogram(df, "qty_f_fruits", [x for x in range(16)], "pics/quantity_fresh_fruits.png")
    draw_histogram(df, "qty_d_prods", [x for x in range(11)], "pics/dairy_products.png")
    draw_histogram(df, "qty_cereal", [x for x in range(6)], "pics/quantity_cereal.png")
    draw_histogram(df, "qty_lpfem", [x for x in range(25)], "pics/quantity_lpfem.png")
    draw_histogram(df, "salt", [x for x in range(30)], "pics/salt.png")
    draw_histogram(df, "wine", [x for x in range(10)], "pics/wine.png")
    draw_histogram(df, "qty_beverage", [x for x in np.arange(0,1.2,0.05)], "pics/quantity_beverage.png")


# PROBLEM-2-CCA
def problem_2():
    df = pd.read_csv("docs/processed_data.csv")
    df = df.fillna(0)
    data = df.iloc[:,np.r_[12:28]]
    X = df.iloc[:,np.r_[12:23]]
    Y = df.iloc[:,np.r_[23:28]]
    scaler = StandardScaler() 
    X_sc = scaler.fit_transform(X) #scale data
    Y_sc = scaler.fit_transform(Y) 

    corr_coeff = data.corr()
    plt.figure(figsize = (15, 20))
    sns.heatmap(corr_coeff, cmap='coolwarm', annot=True, linewidths=1, vmin=-1)
    plt.savefig("pics/corr_analysis.png")

    n_comp = 2
    cca = CCA(n_components=n_comp)
    cca.fit(X_sc, Y_sc)
    X_c, Y_c = cca.transform(X_sc, Y_sc)

    comp_corr = [np.corrcoef(X_c[:, i], Y_c[:, i])[1][0] for i in range(n_comp)]
    plt.figure(figsize = (5, 5))
    plt.bar(['CC1', 'CC2'], comp_corr, color='lightgrey', width = 0.8, edgecolor='k')
    plt.savefig("pics/bar.png")

    coef_df = pd.DataFrame(np.round(cca.coef_, 2), columns = [Y.columns])
    coef_df.index = X.columns
    plt.figure(figsize = (10, 15))
    sns.heatmap(coef_df, cmap='coolwarm', annot=True, linewidths=1, vmin=-1)
    plt.xlabel("Basic Info")
    plt.savefig("pics/CCA.png")


if __name__ == '__main__':
    pre_work()
    problem_1()
    problem_2()

