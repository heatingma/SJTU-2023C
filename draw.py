import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
import matplotlib as mpl
import seaborn as sns
df = pd.read_csv("docs/metrics.csv")
df = df.fillna(0)
sns.set(rc = {'figure.figsize':(14,10)})
plt.rcParams.update({'font.size': 12})
plot = sns.displot(data = df, x = "fresh_vegetables", bins=[x for x in range(30)],stat='probability',color = '#008080')
plt.savefig("pics/fresh_vegtables.png")

sns.set(rc = {'figure.figsize':(14,10)})
plt.rcParams.update({'font.size': 12})
plot = sns.displot(data = df, x = "food_diversity", bins=15,stat='probability',color = '#008080')
plt.savefig("pics/food_diversity.png")

sns.set(rc = {'figure.figsize':(14,10)})
plt.rcParams.update({'font.size': 12})
plot = sns.displot(data = df, x = "fresh_fruits",  bins=[x for x in range(16)],stat='probability',color = '#008080')
plt.savefig("pics/fresh_fruits.png")

sns.set(rc = {'figure.figsize':(14,10)})
plt.rcParams.update({'font.size': 12})
plot = sns.displot(data = df, x = "dairy_products", bins=[x for x in range(11)],stat='probability',color = '#008080')
plt.savefig("pics/dairy_products.png")

sns.set(rc = {'figure.figsize':(14,10)})
plt.rcParams.update({'font.size': 12})
plot = sns.displot(data = df, x = "cereal", bins=[x for x in range(6)],stat='probability',color = '#008080')
plt.savefig("pics/cereal.png")

sns.set(rc = {'figure.figsize':(14,10)})
plt.rcParams.update({'font.size': 12})
plot = sns.displot(data = df, x = "lpfem", bins=[x for x in range(25)],stat='probability',color = '#008080')
plt.savefig("pics/lpfem.png")

sns.set(rc = {'figure.figsize':(14,10)})
plt.rcParams.update({'font.size': 12})
plot = sns.displot(data = df, x = "light_salt", bins=[x for x in range(30)],stat='probability',color = '#008080')
plt.savefig("pics/light_salt.png")

sns.set(rc = {'figure.figsize':(14,10)})
plt.rcParams.update({'font.size': 12})
plot = sns.displot(data = df, x = "light_wine", bins=[x for x in range(10)],stat='probability',color = '#008080')
plt.savefig("pics/light_wine.png")

sns.set(rc = {'figure.figsize':(14,10)})
plt.rcParams.update({'font.size': 12})
plot = sns.displot(data = df, x = "beverage_quantity", bins=[x for x in np.arange(0,1.2,0.05)],stat='probability',color = '#008080')
plt.savefig("pics/beverage_quantity.png")