import pandas as pd
from time import time

list = []
for type in ['ddos', 'normal']:
    i = 1
    start = time()
    data = pd.read_csv(f'datasets/csv/{type}_6x5_120_{i}.csv')
    print(f'{i} time to load data: ', time() - start, 's')
    print(f'size: {data.shape}')
    data['label'] = 1 if type == 'ddos' else 0
    list.append(data)

final = pd.concat(list, ignore_index=True)
final.to_csv(f'6x5_120_{i}.csv', index=False)
print('data size: ', final.shape)
