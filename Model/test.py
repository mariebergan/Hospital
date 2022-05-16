import matplotlib.pyplot as plt
import numpy as np
from collections import Counter
import random

attrs = {}

for node in range(10):
    attrs[node] = {}

for node in attrs:
    if node < 5:
        attrs[node]['present'] = True
    else:    
        attrs[node]['present'] = False

print(attrs)
    
