import pandas as pd
from time import time
from numpy.random import shuffle
from sklearn.preprocessing import LabelEncoder
import matplotlib.pyplot as plt
import seaborn as sns


# Load the datasets and preprocess all the columns.
# return x features and classes both as numpy arrays.
def load(size=-1):
    data = pd.read_csv('datasets/6x5_120_1.csv')
    for col in ['eth.src', 'eth.dst', 'ip.src', 'ip.dst', 'tcp.flags', 'ip.id']:
        data[col] = LabelEncoder().fit(data[col]).transform(data[col])
    data = data.fillna(0)
    x = data.iloc[:, 2:-1].values
    y = data['label'].to_numpy()
    shuffle(x)
    shuffle(y)
    return x[:size], y[:size]


def show_distribution(column='ip.dst'):
    data = pd.read_csv('datasets/6x5_120.csv')
    if not column in data.columns:
        return
    sns.boxplot(data=data, x=column, y='label')
    plt.show()


def show_columns():
    data = pd.read_csv('datasets/6x5_120.csv')
    for idx, row in data.iterrows():
        for col, name in zip(row, data.columns):
            print(f'{name:>20} {col:<20} {type(col)}')
        break


if __name__ == "__main__":
    # start = time()
    # x, y = load()
    # print(time() - start)
    # show_distribution('ip.src')
