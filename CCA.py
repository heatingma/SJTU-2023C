import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from sklearn.datasets import load_iris
from sklearn.cross_decomposition import CCA
from sklearn.preprocessing import StandardScaler
df = pd.read_csv("docs/metrics_1.csv")
df = df.fillna(0)

data =df.iloc[:,np.r_[1:16]]
X = df.iloc[:,np.r_[1:7, 12:16]]
Y = df.iloc[:,np.r_[7:12]]
scaler = StandardScaler() 
X_sc = scaler.fit_transform(X) #scale data
Y_sc = scaler.fit_transform(Y) 

corr_coeff = data.corr()
plt.figure(figsize = (15, 20))
sns.heatmap(corr_coeff, cmap='coolwarm', annot=True, linewidths=1, vmin=-1)
plt.savefig("pics/CCA/corr_analysis.png")

n_comp = 2
cca = CCA(n_components=n_comp)
cca.fit(X_sc, Y_sc)
X_c, Y_c = cca.transform(X_sc, Y_sc)
print(np.corrcoef(X_c[:, 1], Y_c[:, 1])[0, 1]) #输出相关系数
print(cca.coef_)


comp_corr = [np.corrcoef(X_c[:, i], Y_c[:, i])[1][0] for i in range(n_comp)]
plt.figure(figsize = (5, 5))
plt.bar(['CC1', 'CC2'], comp_corr, color='lightgrey', width = 0.8, edgecolor='k')
plt.savefig("pics/CCA/bar.png")

coef_df = pd.DataFrame(np.round(cca.coef_, 2), columns = [Y.columns])
coef_df.index = X.columns
plt.figure(figsize = (10, 15))
sns.heatmap(coef_df, cmap='coolwarm', annot=True, linewidths=1, vmin=-1)
plt.savefig("pics/CCA/CCA.png")
   