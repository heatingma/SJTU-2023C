from data_process import get_data, read_data
from draw import draw_histogram, draw_ratio, draw_cca, draw_corr
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
    draw_ratio(data.evaluate_ratio)
    # histogram pics
    df = pd.read_csv("docs/processed_data.csv")
    draw_histogram(df, "qty_f_veg", [x for x in range(0, 30, 2)], "pics/fresh_vegtables.png", standard=[6, 30])
    draw_histogram(df, "num_day_foods", [x for x in range(0, 20, 2)], "pics/num_day_foods.png", standard=[12, 20])
    draw_histogram(df, "qty_f_fruits", [x for x in np.arange(0, 8, 0.5)], "pics/quantity_fresh_fruits.png", standard=[4, 7])
    draw_histogram(df, "qty_d_prods", [x for x in np.arange(0, 8, 0.5)], "pics/dairy_products.png", standard=[4, 10])
    draw_histogram(df, "qty_cereal", [x for x in np.arange(0, 5, 0.5)], "pics/quantity_cereal.png", standard=[1, 3])
    draw_histogram(df, "qty_lpfem", [x for x in range(0, 15, 1)], "pics/quantity_lpfem.png", standard=[2.4, 4])
    draw_histogram(df, "qty_oil", [x for x in range(0, 150, 10)], "pics/quantity_oil.png", standard=[25, 30])
    draw_histogram(df, "qty_beans", [x for x in np.arange(0, 1.2, 0.05)], "pics/quantity_beans.png", standard=[0.6, 1])
    draw_histogram(df, "qty_salt", [x for x in range(0, 30, 2)], "pics/quantity_salt.png", standard=[0, 5])
    draw_histogram(df, "qty_wine", [x for x in np.arange(0, 50, 5)], "pics/quantity_wine.png", standard=[0, 15])
    draw_histogram(df, "qty_beverage", [x for x in np.arange(0, 1.2, 0.05)], "pics/quantity_beverage.png", standard=[0, 1])
    draw_histogram(df, "ratio_at_home", [x for x in np.arange(0, 1, 0.1)], "pics/ratio_at_home.png", standard=[0.5, 1])

# PROBLEM-2-CCA
def problem_2():
    df = pd.read_csv("docs/processed_data.csv")
    df = df.fillna(0)
    data = df.iloc[:,np.r_[16:36]]
    X1 = data.iloc[:, np.r_[0:12]]
    X2 = data.iloc[:, np.r_[12:15]]
    Y = data.iloc[:, np.r_[15:20]]
        
    draw_corr(data.iloc[:, np.r_[0:12, 15:20]], "pics/corr_analysis_1.png")
    draw_corr(data.iloc[:, np.r_[12:15, 15:20]], "pics/corr_analysis_2.png")
    draw_cca(X1, Y, "pics/CCA_1.png")
    draw_cca(X2, Y, "pics/CCA_2.png", figsize=(12,6))

if __name__ == '__main__':
    pre_work()
    # problem_1()
    # problem_2()

