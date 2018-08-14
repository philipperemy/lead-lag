import numpy as np

raw = open('scripts/lag.txt', 'r').read().strip().split('\n')
a = [float(c.split(' ')[1]) for c in raw]
b = [float(c.split(' ')[0]) for c in raw]

import matplotlib.pyplot as plt

m = int(len(a) // 2)

arr_a = np.array(a)
before = np.sum(np.square(arr_a[:m]))
after = np.sum(np.square(arr_a[m:]))
print('Before= ', before)
print('After= ', after)
print('LLR=', after / before)

plt.scatter(b, a)
plt.show()
