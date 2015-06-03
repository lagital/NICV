from random import *
from matplotlib import *
import matplotlib.pyplot as plt

"""
test = []
bins = []
for i in range(5002):
    test.append(uniform(0.0, 0.9))
    bins.append(i)
bins.append(5002)
"""
"""
plt.hist([0, 4, 6, 5, 7], bins=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12])
#plt.hist(test, bins=bins)
"""
test = []
for i in range(5001):
    test.append(uniform(0.0, 0.2)+uniform(0.0, 0.2)+uniform(0.0, 0.3))
test.append(1.0)

plt.bar(range(0, 5002), test, color='g')
plt.ylabel('NICV')
plt.xlabel('samples')
plt.colors()
plt.show()