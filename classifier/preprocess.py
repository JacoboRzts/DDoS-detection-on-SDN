import pandas as pd
from time import time

list = []
for type in ['ddos', 'norm']:
    for i in range(1, 6):
        # Read the file
        data = pd.read_csv(f'datasets/v3/{type}_6x5_50k_{i}.csv')
        # label the file
        data['label'] = 1 if type == 'ddos' else 0
        list.append(data)

# Join the files into one
final = pd.concat(list, ignore_index=True)

# Save as CSv
final.to_csv('datasets/v3/6x5_500k.csv', index=False)
