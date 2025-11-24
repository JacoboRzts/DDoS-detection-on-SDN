from dataclasses import Field
import pandas as pd
from time import time
from sklearn.preprocessing import LabelEncoder

start = time()
data = pd.read_csv('datasets/6x5_120.csv')
print('time to load data: ', time() - start)
print(data)

print('data size: ', data.shape)
for idx, row in data.iterrows():
    for col, name in zip(row, data.columns):
        print(f'{name:>24} {col:<24} {type(col)}')
    break
