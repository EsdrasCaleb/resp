import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

df = pd.read_csv('../../sql.csv')
fig, ax = plt.subplots()
boxplot = df.boxplot(ax=ax,column=['peso_fonte'])  
plt.show()
