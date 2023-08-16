import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.cross_decomposition import CCA
from sklearn.preprocessing import StandardScaler
import xgboost as xgb
import shap


def ratio(data, tilte="Evaluating Indicator", x_lable="", 
               y_label="Ratio",fig_name="pics/evaluate_ratio.png"):
    plt.rcParams.update({'font.size': 12})
    plt.figure(figsize=(14, 10))
    data = pd.DataFrame(data[:, 1:].astype(float), index=data[:, 0], columns=['False', 'True'])
    data['name'] = data.index
    bottom_plot = sns.barplot(x='name', y='True', data=data, color="#0000A3")
    sns.barplot(x='name', y='False', data=data, color="#FF0000", bottom=data['True'])
    topbar = plt.Rectangle((0, 0), 1, 1, fc="#FF0000", edgecolor='none')
    bottombar = plt.Rectangle((0, 0), 1, 1, fc='#0000A3', edgecolor='none')
    l = plt.legend([bottombar, topbar], ['standard', 'nonstandard'], loc=1, ncol = 2, prop={'size':8})
    l.draw_frame(False)
    sns.despine(left=True)
    bottom_plot.set_ylabel(y_label)
    bottom_plot.set_xlabel(x_lable)
    bottom_plot.set_xticklabels(data.name, rotation=20, fontsize='small')
    plt.ylim(0, 1.1)
    plt.title(tilte)
    plt.savefig(fig_name)
    
    
def histogram(data, x, bins, fig_name, figsize=(14,10), font_size=12, 
                   stat='probability',color = '#008080', standard: list=None):
    sns.set(rc = {'figure.figsize':figsize})
    plt.rcParams.update({'font.size': font_size})
    sns.displot(data=data, x=x, bins=bins, stat=stat, color=color)
    if standard is not None:
        for value in standard:
            plt.axvline(x=value, color='red')
    plt.savefig(fig_name)
    
def corr(data, save_path, figsize = (15, 20)):
    corr_coeff = data.corr()
    plt.figure(figsize=figsize)
    sns.heatmap(corr_coeff, cmap='coolwarm', annot=True, linewidths=1, vmin=-1)
    plt.savefig(save_path)

    
def cca(X, Y, save_path, figsize = (10, 15), x_label="Basic Info"):
    scaler = StandardScaler() 
    X_sc = scaler.fit_transform(X) #scale data
    Y_sc = scaler.fit_transform(Y) 
    cca = CCA(n_components=2)
    cca.fit(X_sc, Y_sc)
    coef_df = pd.DataFrame(np.round(cca.coef_, 2), columns = [Y.columns])
    coef_df.index = X.columns
    plt.figure(figsize=figsize)
    sns.heatmap(coef_df, cmap='coolwarm', annot=True, linewidths=1, vmin=-1)
    plt.xlabel(x_label)
    plt.savefig(save_path)


def xgboost_shap(X: pd.DataFrame, Y:pd.DataFrame, save_path):
    # normalize
    scaler = StandardScaler()
    X_normalized = X.copy()
    X_normalized[X.columns] = scaler.fit_transform(X)

    # train the xgboot model
    X_train, X_test, y_train, y_test = train_test_split(X_normalized, Y, test_size=0.2, random_state=42)
    model = xgb.XGBRegressor()
    model.fit(X_train, y_train)

    # use shap to explain
    explainer = shap.TreeExplainer(model)
    shap_values = explainer.shap_values(X_test)
    
    # form the pics
    shap.summary_plot(shap_values, X_test, show=False)
    plt.gcf().savefig('{}_{}.png'.format(save_path, 1), bbox_inches='tight')
    plt.clf()
    shap.summary_plot(shap_values, X_test, show=False, plot_type="bar",)
    plt.gcf().savefig('{}_{}.png'.format(save_path, 2), bbox_inches='tight')   
    plt.clf()