import matplotlib.pyplot as plt
import pandas as pd

DIR = 'datasets/v3/'

ddos = pd.read_csv(DIR+'size_ddos.csv')
norm = pd.read_csv(DIR+'size_norm.csv')

norm['label'] = 0
ddos['label'] = 1

# final = pd.concat([norm, ddos], ignore_index=True)

plt.figure(figsize=(10, 6))

# Graficar cada DataFrame con su propio color
plt.bar(ddos.index, ddos.iloc[:, 0], label='DDoS', color='coral', alpha=0.7)
plt.bar(norm.index, norm.iloc[:, 0], label='Normal', color='lightblue', alpha=0.7)

plt.xlabel('TCP Flows')
plt.ylabel('Data size (bits)')
plt.legend()
plt.grid(axis='y', alpha=0.3)
plt.show()
