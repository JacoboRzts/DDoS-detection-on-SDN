from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, confusion_matrix
from sklearn.tree import DecisionTreeClassifier
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import data
from time import time

print('Process\t  Time (s)')
print('Load ', end='\t  ')
start = time()
x, y = data.load()
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.8)
print(time() - start)

tree = DecisionTreeClassifier()

start = time()
print('Train', end='\t  ')
tree = tree.fit(x_train, y_train)
print(time() - start)
print('Predict', end='\t  ')
y_pred = tree.predict(x_test)
print(time() - start)

print("\nResults")
print('Score\t', accuracy_score(y_test, y_pred))
print('Matrix')
names = ['Normal', 'DDoS']
matrix = pd.DataFrame(confusion_matrix(y_test, y_pred), index=names, columns=names)
print(matrix)


sns.heatmap(matrix, annot=False, cmap="crest")
plt.show()
