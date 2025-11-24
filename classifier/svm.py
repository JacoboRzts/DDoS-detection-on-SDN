from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, confusion_matrix
from sklearn.svm import SVC
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import data
from time import time

print('Loading data', end='\t')
start = time()
x, y = data.load(1000)
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=8)
print(time() - start)

model = SVC(kernel='linear', gamma='auto', C=0.1)

start = time()
print('Training', end='\t')
model.fit(x_train, y_train)
print(time() - start)
print('Predicting', end='\t')
start = time()
y_pred = model.predict(x_test)
print(time() - start)

print("\nResults")
print('Score\t', accuracy_score(y_test, y_pred))
print('Matrix')
names = ['Normal', 'DDoS']
matrix = pd.DataFrame(confusion_matrix(y_test, y_pred), index=names, columns=names)
print(matrix)


sns.heatmap(matrix, annot=False, cmap="crest")
plt.show()
