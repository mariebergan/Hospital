import matplotlib.pyplot as plt
import numpy as np
from collections import Counter
import random

a = np.zeros((5, 5), dtype = float)
n = 3
for sims in range(n):
    simArr = np.ones((5, 5), dtype = float)
    for i in range(5):
        for j in range(5):
            a[i, j] += simArr[i, j]
    
for i in range(5):
    for j in range(5):
        a[i, j] /= n
        

print(a)

