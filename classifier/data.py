import pandas as pd
from sklearn.preprocessing import LabelEncoder

FILENAME = 'datasets/v3/6x5_500k.csv'

# Load the datasets and preprocess all the columns.
# return x features and classes both as numpy arrays.
def load():
    data = pd.read_csv(FILENAME)
    for col in ['eth.src', 'eth.dst', 'ip.src', 'ip.dst', 'tcp.flags']:
        data[col] = LabelEncoder().fit(data[col]).transform(data[col])
    data = data.fillna(0)
    x = data.iloc[:, 2:-1].values
    y = data['label'].to_numpy()
    return x, y


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
